#!/usr/bin/env python3
"""VIX>=25 모든 신호일 × 박세익 대표 지목 주요 5종목 개별 수익률 매트릭스 + 히트맵.
신호일→2026-06-16 수익률. 데이터: analysis/data/*.csv (Yahoo Finance)
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
VIX=dict(zip(idx_dates, idx["VIX (공포지수)"]))
KOSPI={d:v for d,v in zip(idx_dates, idx["KOSPI"]) if v}
TODAY=st_dates[-1]

NAMED=["삼성전자","SK하이닉스","HD한국조선해양","한화에어로스페이스","현대차"]

def price_after(name, target):
    for d,v in zip(st_dates, st[name]):
        if d>=target and v is not None: return v
    return None
def kospi_after(target):
    for d in idx_dates:
        if d>=target and KOSPI.get(d): return KOSPI[d]
    return None

# VIX>=25 진입 에피소드
episodes=[]; prev=0; cur=None
for d in idx_dates:
    v=VIX[d]
    if v is None: continue
    if v>=25 and prev<25: cur={'entry':d,'peak':v}; episodes.append(cur)
    elif v>=25 and cur: cur['peak']=max(cur['peak'],v)
    prev=v

# 매트릭스: 행=신호, 열=종목 / 신호일→오늘 수익률(%)
mat=[]
labels=[]
for e in episodes:
    bd=e['entry']
    labels.append(f"{bd}\n(VIX최고 {e['peak']:.0f})")
    row=[]
    for n in NAMED:
        p0=price_after(n,bd); p1=st[n][-1]
        row.append((p1/p0-1)*100 if p0 else np.nan)
    mat.append(row)
mat=np.array(mat)

# KOSPI / 바스켓 열 추가
kosp=[]; bask=[]
for e in episodes:
    bd=e['entry']
    k0=kospi_after(bd); kosp.append((KOSPI[TODAY]/k0-1)*100 if k0 else np.nan)
    rets=[(st[n][-1]/price_after(n,bd)-1)*100 for n in NAMED if price_after(n,bd)]
    bask.append(np.mean(rets))

# ---- CSV ----
with open("analysis/data/vix25_signal_returns.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["VIX25_신호일","에피소드내_VIX최고"]+NAMED+["5종목바스켓","KOSPI"])
    for i,e in enumerate(episodes):
        w.writerow([e['entry'],f"{e['peak']:.1f}"]+[f"{x:.1f}" for x in mat[i]]+[f"{bask[i]:.1f}",f"{kosp[i]:.1f}"])

print("=== VIX≥25 신호일 → 2026-06-16 수익률(%) ===")
hdr="신호일       VIX  "+" ".join(f"{n[:5]:>7}" for n in NAMED)+"  바스켓   KOSPI"
print(hdr)
for i,e in enumerate(episodes):
    print(f"{e['entry']} {e['peak']:4.0f}  "+" ".join(f"{mat[i][j]:7.1f}" for j in range(len(NAMED)))+f"  {bask[i]:6.1f}  {kosp[i]:6.1f}")
print("-"*len(hdr))
print(f"평균        {'':4} "+" ".join(f"{np.nanmean(mat[:,j]):7.1f}" for j in range(len(NAMED)))+f"  {np.mean(bask):6.1f}  {np.mean(kosp):6.1f}")

# ---- 히트맵 (전체 매트릭스: 종목 + 바스켓 + KOSPI) ----
full=np.column_stack([mat, np.array(bask), np.array(kosp)])
cols_all=NAMED+["5종목\n바스켓","KOSPI"]
fig,ax=plt.subplots(figsize=(11,6.5))
im=ax.imshow(full, cmap="RdYlGn", aspect="auto", vmin=-10, vmax=200)
ax.set_xticks(range(len(cols_all))); ax.set_xticklabels(cols_all, fontsize=9)
ax.set_yticks(range(len(episodes))); ax.set_yticklabels([f"{e['entry']} (VIX {e['peak']:.0f})" for e in episodes], fontsize=9)
for i in range(full.shape[0]):
    for j in range(full.shape[1]):
        ax.text(j,i,f"{full[i,j]:.0f}%",ha="center",va="center",fontsize=8,
                color="black")
# KOSPI 열 구분선
ax.axvline(len(NAMED)-0.5,color="white",lw=2)
ax.set_title("VIX≥25 신호일별 · 종목별 수익률 (신호일→2026-06-16, %)\n박세익 대표 지목 주요 5종목 · 동일가중바스켓 · KOSPI")
plt.colorbar(im,label="수익률(%)",fraction=0.04)
plt.tight_layout(); plt.savefig("analysis/charts/40_vix25_heatmap.png",dpi=130); plt.close()

# ---- 종목별 '모든 VIX≥25 신호 평균 수익률' 막대 ----
avg=[np.nanmean(mat[:,j]) for j in range(len(NAMED))]+[np.mean(bask),np.mean(kosp)]
order=np.argsort(avg)
plt.figure(figsize=(11,5.5))
colors=["#2980b9"]*len(NAMED)+["#c0392b","#7f8c8d"]
names_all=NAMED+["5종목바스켓","KOSPI"]
bars=plt.barh([names_all[i] for i in order],[avg[i] for i in order],color=[colors[i] for i in order])
for b,i in zip(bars,order):
    plt.text(b.get_width(),b.get_y()+b.get_height()/2,f" {avg[i]:+.1f}%",va="center",fontsize=9)
plt.title("7회 VIX≥25 신호 '평균' 수익률 (각 신호일→2026-06-16, 동일가중 단순평균)")
plt.xlabel("평균 수익률(%)"); plt.grid(axis="x",alpha=.3); plt.tight_layout()
plt.savefig("analysis/charts/41_vix25_avg.png",dpi=130); plt.close()
print("\nsaved: 40_vix25_heatmap.png, 41_vix25_avg.png, vix25_signal_returns.csv")
