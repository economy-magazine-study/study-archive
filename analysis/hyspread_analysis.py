#!/usr/bin/env python3
"""HY 스프레드(=HYG ETF 프록시, 가격↓=스프레드↑=신용공포) 신호 기반 백테스트.
신용공포 신호: HYG가 롤링피크 대비 -2% 이상 하락(스프레드 확대) → 진입.
※ 실제 ICE BofA HY OAS(FRED)는 egress 차단으로 HYG ETF를 방향성 프록시로 사용.
"""
import csv, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import numpy as np, glob
for f in glob.glob("/usr/share/fonts/truetype/korean/*.*"):
    font_manager.fontManager.addfont(f); rcParams["font.family"]=font_manager.FontProperties(fname=f).get_name()
rcParams["axes.unicode_minus"]=False

def load(path):
    rows=list(csv.DictReader(open(path)))
    cols={c:[] for c in rows[0] if c!="date"}; dates=[]
    for r in rows:
        dates.append(dt.date.fromisoformat(r["date"]))
        for c in cols: cols[c].append(float(r[c]) if r[c] else None)
    return dates, cols

idx_dates, idx = load("analysis/data/indices_1y.csv")
st_dates, st = load("analysis/data/stocks_price_1y.csv")
KOSPI={d:v for d,v in zip(idx_dates, idx["KOSPI"]) if v}
TODAY=st_dates[-1]
NAMED=["삼성전자","SK하이닉스","HD한국조선해양","한화에어로스페이스","현대차"]

# HYG 시계열 + 롤링 낙폭(=스프레드 확대 프록시)
hyg=[(d,v) for d,v in zip(idx_dates, idx["HYG ETF (HY스프레드 프록시)"]) if v]
peak=hyg[0][1]; ddseries=[]
for d,v in hyg:
    peak=max(peak,v); ddseries.append((d,(v/peak-1)*100))
DD=dict(ddseries)
THR=-2.0  # 신용공포 임계치 (HYG 낙폭 -2%)

# 신호 에피소드(10일 이상 간격이면 별도 이벤트), 진입=첫 돌파일, 에피소드 최대낙폭 기록
episodes=[]; prev=0; last=None; cur=None
for d,dd in ddseries:
    if dd<=THR and prev>THR:
        if cur and (d-cur['entry']).days<=10:
            pass
        else:
            cur={'entry':d,'maxdd':dd}; episodes.append(cur)
    if dd<=THR and cur: cur['maxdd']=min(cur['maxdd'],dd)
    prev=dd
# 10일내 인접 에피소드 병합
merged=[]
for e in episodes:
    if merged and (e['entry']-merged[-1]['entry']).days<=12:
        merged[-1]['maxdd']=min(merged[-1]['maxdd'],e['maxdd'])
    else: merged.append(e)
episodes=merged

def price_after(name,t):
    for d,v in zip(st_dates,st[name]):
        if d>=t and v is not None: return v,d
    return None,None
def kospi_after(t):
    for d in idx_dates:
        if d>=t and KOSPI.get(d): return KOSPI[d]
    return None

print("HY스프레드(HYG프록시) 신용공포 신호(낙폭<=-2%) 에피소드:")
for e in episodes:
    p0,bd=price_after(NAMED[0],e['entry'])
    held=(TODAY-(bd or e['entry'])).days
    print(f"  진입 {e['entry']}  에피소드최대낙폭 {e['maxdd']:.2f}%  보유 {held}일")

# 매트릭스
mat=[]; bask=[]; kosp=[]; held_days=[]
for e in episodes:
    bd0=None; row=[]
    for n in NAMED:
        p0,bd=price_after(n,e['entry']);
        if bd0 is None: bd0=bd
        row.append((st[n][-1]/p0-1)*100 if p0 else np.nan)
    mat.append(row)
    bask.append(np.nanmean(row))
    k0=kospi_after(e['entry']); kosp.append((KOSPI[TODAY]/k0-1)*100 if k0 else np.nan)
    held_days.append((TODAY-bd0).days)
mat=np.array(mat)

with open("analysis/data/hyspread_signal_returns.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["HY공포_신호일","에피소드최대낙폭%","보유일"]+NAMED+["5종목바스켓","KOSPI"])
    for i,e in enumerate(episodes):
        w.writerow([e['entry'],f"{e['maxdd']:.2f}",held_days[i]]+[f"{x:.1f}" for x in mat[i]]+[f"{bask[i]:.1f}",f"{kosp[i]:.1f}"])

print("\n=== HY공포 신호일 → 2026-06-16 수익률(%) ===")
for i,e in enumerate(episodes):
    print(f"{e['entry']} (낙폭{e['maxdd']:.1f}%,{held_days[i]}일)  "+" ".join(f"{n[:4]}{mat[i][j]:6.1f}" for j,n in enumerate(NAMED))+f"  바스켓{bask[i]:6.1f}  KOSPI{kosp[i]:6.1f}")

# ---- Chart 1: HYG 가격 + 낙폭(스프레드확대) + 신호 ----
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(12,7),sharex=True,gridspec_kw={'height_ratios':[2,1]})
ax1.plot([d for d,_ in hyg],[v for _,v in hyg],color="#16a085",lw=1.5)
ax1.set_title("HY 스프레드 프록시(HYG ETF) — 가격↓ = 스프레드↑ = 신용공포")
ax1.set_ylabel("HYG (USD)"); ax1.grid(alpha=.3)
ax2.fill_between([d for d,_ in ddseries],[dd for _,dd in ddseries],0,color="#c0392b",alpha=.5)
ax2.axhline(THR,color="red",ls="--",lw=1,label=f"신용공포 임계 {THR}%")
ax2.set_ylabel("롤링피크대비 낙폭(%)"); ax2.legend(fontsize=8); ax2.grid(alpha=.3)
for e in episodes:
    for ax in (ax1,ax2): ax.axvline(e['entry'],color="darkred",ls=":",lw=1)
ax1.annotate(f"최대 신용공포\n{min(ddseries,key=lambda x:x[1])[0]} ({min(dd for _,dd in ddseries):.1f}%)",
    xy=(min(ddseries,key=lambda x:x[1])[0], min(v for _,v in hyg)),
    xytext=(0.62,0.2),textcoords="axes fraction",fontsize=9,color="darkred",
    arrowprops=dict(arrowstyle="->",color="darkred"))
plt.tight_layout(); plt.savefig("analysis/charts/50_hyspread.png",dpi=130); plt.close()

# ---- Chart 2: 히트맵 ----
full=np.column_stack([mat,np.array(bask),np.array(kosp)])
cols_all=NAMED+["5종목\n바스켓","KOSPI"]
fig,ax=plt.subplots(figsize=(11,1.2+0.7*len(episodes)))
im=ax.imshow(full,cmap="RdYlGn",aspect="auto",vmin=-10,vmax=200)
ax.set_xticks(range(len(cols_all))); ax.set_xticklabels(cols_all,fontsize=9)
ax.set_yticks(range(len(episodes))); ax.set_yticklabels([f"{e['entry']}\n(낙폭{e['maxdd']:.1f}%·{held_days[i]}일)" for i,e in enumerate(episodes)],fontsize=8)
for i in range(full.shape[0]):
    for j in range(full.shape[1]):
        ax.text(j,i,f"{full[i,j]:.0f}%",ha="center",va="center",fontsize=8)
ax.axvline(len(NAMED)-0.5,color="white",lw=2)
ax.set_title("HY스프레드(HYG프록시) 신용공포 신호 × 종목별 수익률 (신호일→2026-06-16)")
plt.colorbar(im,label="수익률(%)",fraction=0.04)
plt.tight_layout(); plt.savefig("analysis/charts/51_hyspread_heatmap.png",dpi=130); plt.close()
print("\nsaved: 50_hyspread.png, 51_hyspread_heatmap.png, hyspread_signal_returns.csv")
