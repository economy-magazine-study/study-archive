#!/usr/bin/env python3
"""기사 취지 충실판: '공포에 사서 VIX 정상화 시 매도' 왕복매매 백테스트.
매수: VIX가 임계(buy_thr) 상향돌파한 종가 / 매도: 이후 VIX<sell_thr 첫 종가.
한 번에 한 포지션, 매도 후 다음 공포까지 현금. (배당·세금·수수료 제외, 동일가중)
"""
import csv, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import glob
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
VIX=[(d,v) for d,v in zip(idx_dates, idx["VIX (공포지수)"]) if v is not None]
NAMED=["삼성전자","SK하이닉스","HD한국조선해양","한화에어로스페이스","현대차"]

def px(name, target):           # target 이후 첫 유효 종가
    for d,v in zip(st_dates, st[name]):
        if d>=target and v is not None: return d,v
    return None,None

def find_trades(buy_thr, sell_thr):
    pos=False; tr=[]; prev=None; entry=None
    for d,v in VIX:
        if not pos and prev is not None and v>=buy_thr and prev<buy_thr:
            pos=True; entry=(d,v)
        elif pos and v<sell_thr:
            tr.append([entry,(d,v,False)]); pos=False
        prev=v
    if pos: tr.append([entry,(VIX[-1][0],VIX[-1][1],True)])  # 미청산→종료일 청산
    return tr

def run(buy_thr, sell_thr, tag):
    trades=find_trades(buy_thr,sell_thr)
    print(f"\n{'='*70}\n전략: 매수 VIX≥{buy_thr} → 매도 VIX<{sell_thr}   ({tag})\n{'='*70}")
    chain=1.0; rows_out=[]
    for (bd0,bv),(sd0,sv,open_end) in trades:
        per=[]; det=[]
        for n in NAMED:
            _,bp=px(n,bd0); _,sp=px(n,sd0)
            per.append(sp/bp); det.append((n,bp,sp,sp/bp-1))
        bask=sum(per)/len(per)-1
        chain*=(1+bask)
        held=(sd0-bd0).days
        rows_out.append((bd0,sd0,held,bask,det,open_end))
        print(f"\n[매수 {bd0} VIX{bv:.0f}] → [매도 {sd0} VIX{sv:.0f}] {held}일"+(" *종료일강제청산*" if open_end else ""))
        for n,bp,sp,r in det:
            print(f"    {n:<16}{bp:>11,.0f} → {sp:>11,.0f}  {r*100:+7.1f}%")
        print(f"    └ 바스켓: {bask*100:+.1f}%")
    print(f"\n▶ 왕복매매 {len(trades)}회 연속 복리 누적: {(chain-1)*100:+.1f}%  (나머지 기간은 현금)")
    return rows_out, (chain-1)*100

res25,tot25=run(25,20,"공포확산 매수")
res30,tot30=run(30,20,"극도공포 매수")

# 벤치마크: 1년 buy&hold 바스켓
bh=[]
for n in NAMED:
    _,bp=px(n,st_dates[0]); _,sp=px(n,st_dates[-1]); bh.append(sp/bp)
bh_ret=(sum(bh)/len(bh)-1)*100
print(f"\n{'#'*70}\n[벤치] 1년 buy&hold 바스켓: {bh_ret:+.1f}%")
print(f"[벤치] VIX≥25 신호 후 6/16까지 보유(첫신호): 174.4%  ← 이전 분석(반등매도 안함)")

# ---- CSV ----
with open("analysis/data/vix_roundtrip_trades.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["전략","매수일","매도일","보유일","바스켓수익률%"]+NAMED)
    for tagname,res in [("매수25매도20",res25),("매수30매도20",res30)]:
        for bd,sd,held,bask,det,oe in res:
            w.writerow([tagname,bd,sd,held,f"{bask*100:.1f}"]+[f"{r*100:.1f}" for _,_,_,r in det])

# ---- Chart: VIX + 매수/매도 표시 ----
fig,ax=plt.subplots(figsize=(12,5.5))
ax.plot([d for d,_ in VIX],[v for _,v in VIX],color="#2c3e50",lw=1.2,zorder=1)
ax.axhline(25,color="orange",ls="--",lw=1,label="매수 임계 VIX 25")
ax.axhline(20,color="green",ls="--",lw=1,label="매도 임계 VIX 20")
for bd,sd,held,bask,det,oe in res25:
    bv=dict(VIX)[bd]; sv=dict(VIX)[sd]
    ax.scatter([bd],[bv],color="red",marker="^",s=120,zorder=3)
    ax.scatter([sd],[sv],color="green",marker="v",s=120,zorder=3)
    ax.annotate(f"{bask*100:+.0f}%",xy=(sd,sv),xytext=(0,12),textcoords="offset points",
                ha="center",fontsize=9,color="#c0392b",fontweight="bold")
ax.scatter([],[],color="red",marker="^",s=80,label="매수(공포)")
ax.scatter([],[],color="green",marker="v",s=80,label="매도(정상화)")
ax.set_title(f"'공포에 매수 → VIX 정상화 시 매도' 왕복매매 (매수≥25/매도<20)\n3회 매매 누적 {tot25:+.0f}% · vs 1년 보유 {bh_ret:+.0f}%")
ax.set_ylabel("VIX"); ax.legend(fontsize=8,ncol=2); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("analysis/charts/70_vix_roundtrip.png",dpi=130); plt.close()
print("\nsaved: 70_vix_roundtrip.png, vix_roundtrip_trades.csv")
