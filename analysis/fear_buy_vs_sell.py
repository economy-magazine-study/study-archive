#!/usr/bin/env python3
"""공포에 산 케이스 vs 공포에 판 케이스 — 주요 5종목 개별.
규칙: 공포 = VIX>=25 진입 ~ VIX<20 회복 구간.
 · 공포매수(역발상): 공포구간에만 보유(사고-팔고), 평소 현금
 · 공포매도(패닉/회피): 공포구간엔 현금(팔고), 평소 보유
두 전략의 보유구간을 합치면 1년 buy&hold. (배당·세금·수수료 제외)
"""
import csv, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import numpy as np, glob
for f in glob.glob("/usr/share/fonts/truetype/korean/*.*"):
    font_manager.fontManager.addfont(f); rcParams["font.family"]=font_manager.FontProperties(fname=f).get_name()
rcParams["axes.unicode_minus"]=False

def load(p):
    rows=list(csv.DictReader(open(p))); cols={c:[] for c in rows[0] if c!='date'}; ds=[]
    for r in rows:
        ds.append(dt.date.fromisoformat(r['date']))
        for c in cols: cols[c].append(float(r[c]) if r[c] else None)
    return ds,cols
idx_d,idx=load('analysis/data/indices_1y.csv')
st_d,st=load('analysis/data/stocks_price_1y.csv')
VIX=[(d,v) for d,v in zip(idx_d,idx['VIX (공포지수)']) if v is not None]
NAMED=["삼성전자","SK하이닉스","HD한국조선해양","한화에어로스페이스","현대차"]

def windows(buy=25,sell=20):
    pos=False;prev=None;w=[];e=None
    for d,v in VIX:
        if not pos and prev is not None and v>=buy and prev<buy: pos=True;e=d
        elif pos and v<sell: w.append((e,d));pos=False
        prev=v
    if pos: w.append((e,VIX[-1][0]))
    return w
W=windows()
fear=W
calm=[(st_d[0],W[0][0])]+[(W[i][1],W[i+1][0]) for i in range(len(W)-1)]+[(W[-1][1],st_d[-1])]

def px(n,t):
    for d,v in zip(st_d,st[n]):
        if d>=t and v is not None: return v
def compound(n,segs):
    tot=1.0
    for a,b in segs: tot*=px(n,b)/px(n,a)
    return (tot-1)*100

B={n:compound(n,fear) for n in NAMED}   # 공포매수(공포구간만)
C={n:compound(n,calm) for n in NAMED}   # 공포매도(평소만)
BH={n:(px(n,st_d[-1])/px(n,st_d[0])-1)*100 for n in NAMED}
B['바스켓']=np.mean([B[n] for n in NAMED]); C['바스켓']=np.mean([C[n] for n in NAMED]); BH['바스켓']=np.mean([BH[n] for n in NAMED])
COLS=NAMED+['바스켓']

# CSV
with open('analysis/data/fear_buy_vs_sell.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['종목','공포매수(공포구간만)%','공포매도(평소만)%','1년보유%'])
    for n in COLS: w.writerow([n,f"{B[n]:.1f}",f"{C[n]:.1f}",f"{BH[n]:.1f}"])

print("공포구간:",[(str(a),str(b)) for a,b in fear])
print(f"\n{'종목':<16}{'공포매수':>10}{'공포매도':>10}{'1년보유':>10}")
for n in COLS:
    print(f"{n:<16}{B[n]:>9.1f}%{C[n]:>9.1f}%{BH[n]:>9.1f}%")

# ---- Chart: 두 패널 (스케일 차이 큼) ----
y=np.arange(len(COLS))
fig,(axL,axR)=plt.subplots(1,2,figsize=(13.5,6))
# 좌: 공포매수
valsB=[B[n] for n in COLS]
barsB=axL.barh(y,valsB,color=["#c0392b" if v>=0 else "#7f8c8d" for v in valsB])
axL.set_yticks(y); axL.set_yticklabels(COLS); axL.invert_yaxis()
axL.axvline(0,color="black",lw=.8)
for b,v in zip(barsB,valsB): axL.text(v,b.get_y()+b.get_height()/2,f" {v:+.1f}%",va="center",fontsize=9)
axL.set_title("① 공포에 산 케이스 (역발상)\nVIX≥25 매수 → VIX<20 매도, 공포구간만 보유")
axL.set_xlabel("수익률(%)"); axL.grid(axis="x",alpha=.3)
# 우: 공포매도 vs 1년보유
valsC=[C[n] for n in COLS]; valsBH=[BH[n] for n in COLS]
h=0.38
axR.barh(y-h/2,valsC,height=h,color="#27ae60",label="공포매도(공포 회피·평소 보유)")
axR.barh(y+h/2,valsBH,height=h,color="#95a5a6",label="1년 내내 보유(참고)")
axR.set_yticks(y); axR.set_yticklabels(COLS); axR.invert_yaxis()
for yi,v in zip(y-h/2,valsC): axR.text(v,yi,f" {v:+.0f}%",va="center",fontsize=8)
for yi,v in zip(y+h/2,valsBH): axR.text(v,yi,f" {v:+.0f}%",va="center",fontsize=8,color="#555")
axR.set_title("② 공포에 판 케이스 (회피)\nVIX≥25 매도 → VIX<20 매수, 평소만 보유")
axR.set_xlabel("수익률(%)"); axR.grid(axis="x",alpha=.3); axR.legend(fontsize=8,loc="lower right")
fig.suptitle("공포에 산 케이스 vs 공포에 판 케이스 — 주요 5종목 (2025-06~2026-06)",fontsize=14,y=1.02)
plt.tight_layout(); plt.savefig("analysis/charts/80_fear_buy_vs_sell.png",dpi=130,bbox_inches="tight"); plt.close()
print("\nsaved: 80_fear_buy_vs_sell.png, fear_buy_vs_sell.csv")
