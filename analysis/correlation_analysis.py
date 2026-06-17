#!/usr/bin/env python3
"""VIX(공포지수) vs HY스프레드(HYG ETF 프록시) 상관관계 분석.
주의: HYG는 가격이라 스프레드와 역방향(HYG↓=스프레드↑). 분석 후 부호를 스프레드 기준으로 환산해 해석.
데이터: analysis/data/indices_1y.csv (Yahoo Finance, 2025-06-16~2026-06-16)
"""
import csv, datetime as dt
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import glob
for f in glob.glob("/usr/share/fonts/truetype/korean/*.*"):
    font_manager.fontManager.addfont(f); rcParams["font.family"]=font_manager.FontProperties(fname=f).get_name()
rcParams["axes.unicode_minus"]=False

rows=list(csv.DictReader(open('analysis/data/indices_1y.csv')))
data={}
for r in rows:
    d=dt.date.fromisoformat(r['date'])
    v=r['VIX (공포지수)']; h=r['HYG ETF (HY스프레드 프록시)']
    if v and h: data[d]=(float(v),float(h))
dates=sorted(data)
vix=np.array([data[d][0] for d in dates])
hyg=np.array([data[d][1] for d in dates])
n=len(dates)
print(f"공통 거래일: {n}  ({dates[0]}~{dates[-1]})")

def pearson(a,b): return float(np.corrcoef(a,b)[0,1])
def spearman(a,b):
    ra=np.argsort(np.argsort(a)); rb=np.argsort(np.argsort(b))
    return pearson(ra.astype(float),rb.astype(float))

# 스프레드 프록시(방향 일치): 스프레드↑일수록 값↑ → HYG를 음수화한 표준화 지표
spread_px = -(hyg)  # 부호만 뒤집어 '스프레드 방향'

# 1) 수준(level) 상관
print("\n[수준 상관] VIX vs HYG가격")
print(f"  Pearson : {pearson(vix,hyg):+.3f}")
print(f"  Spearman: {spearman(vix,hyg):+.3f}")
print(f"  → 스프레드 기준 환산(VIX vs HY스프레드): Pearson {pearson(vix,spread_px):+.3f} (부호반전)")

# 2) 일간 변화(change) 상관 — 추세에 의한 허위상관 제거
dvix=np.diff(vix); dhyg=np.diff(hyg)
print("\n[일간 변화 상관] ΔVIX vs ΔHYG")
print(f"  Pearson : {pearson(dvix,dhyg):+.3f}")
print(f"  → 스프레드 기준: ΔVIX vs Δ스프레드 {pearson(dvix,-dhyg):+.3f}")

# 3) 리드-래그 교차상관 (ΔVIX(t) vs ΔHYG(t+lag))
print("\n[리드-래그] ΔVIX(t) vs Δ스프레드(t+lag)  (lag>0 = VIX가 선행)")
best=(0,0)
for lag in range(-5,6):
    if lag>=0: a=dvix[:len(dvix)-lag]; b=(-dhyg)[lag:]
    else: a=dvix[-lag:]; b=(-dhyg)[:len(dhyg)+lag]
    c=pearson(a,b)
    mark=" *" if abs(c)>abs(best[1]) else ""
    if abs(c)>abs(best[1]): best=(lag,c)
    print(f"  lag {lag:+d}일: {c:+.3f}{mark}")
print(f"  최강 상관 lag={best[0]:+d}일 ({best[1]:+.3f})")

# 4) 롤링 30일 상관 (스프레드 기준)
win=30
roll_dates=[]; roll=[]
for i in range(win,n):
    roll_dates.append(dates[i])
    roll.append(pearson(vix[i-win:i], spread_px[i-win:i]))

# ---- Chart 1: 듀얼축 + 롤링상관 ----
fig,(ax1,ax3)=plt.subplots(2,1,figsize=(12,7.5),sharex=True,gridspec_kw={'height_ratios':[2,1]})
ax1.plot(dates,vix,color="#2c3e50",lw=1.3,label="VIX (공포지수, 좌)")
ax1.set_ylabel("VIX",color="#2c3e50"); ax1.tick_params(axis='y',labelcolor="#2c3e50")
ax2=ax1.twinx()
ax2.plot(dates,hyg,color="#16a085",lw=1.3,label="HYG (HY스프레드 프록시, 우·역축)")
ax2.set_ylabel("HYG (USD)",color="#16a085"); ax2.tick_params(axis='y',labelcolor="#16a085")
ax2.invert_yaxis()  # 역축 → HYG역축=스프레드방향, VIX와 같은 방향으로 보임
ax1.set_title(f"VIX vs HY스프레드 프록시 — 수준 상관(스프레드기준) Pearson {pearson(vix,spread_px):+.2f}\n(HYG 우축 반전 = 스프레드 방향; 두 선이 함께 움직이면 양의 상관)")
ax1.grid(alpha=.3)
l1,la1=ax1.get_legend_handles_labels(); l2,la2=ax2.get_legend_handles_labels()
ax1.legend(l1+l2,la1+la2,fontsize=8,loc="upper left")
ax3.plot(roll_dates,roll,color="#c0392b",lw=1.3)
ax3.axhline(0,color="black",lw=.6); ax3.axhline(np.mean(roll),color="gray",ls="--",lw=.8,label=f"평균 {np.mean(roll):+.2f}")
ax3.fill_between(roll_dates,roll,0,where=[r>0 for r in roll],color="#c0392b",alpha=.2)
ax3.set_ylabel("30일 롤링상관"); ax3.set_ylim(-1,1); ax3.legend(fontsize=8); ax3.grid(alpha=.3)
ax3.set_title("VIX vs HY스프레드 30일 롤링 상관계수 (양수=함께 공포)",fontsize=10)
plt.tight_layout(); plt.savefig("analysis/charts/60_corr_timeseries.png",dpi=130); plt.close()

# ---- Chart 2: 산점도 (수준 + 변화) ----
fig,(axa,axb)=plt.subplots(1,2,figsize=(13,5.5))
sc=axa.scatter(vix,hyg,c=[d.toordinal() for d in dates],cmap="viridis",s=14)
axa.set_xlabel("VIX"); axa.set_ylabel("HYG (USD)")
z=np.polyfit(vix,hyg,1); xs=np.array([vix.min(),vix.max()])
axa.plot(xs,z[0]*xs+z[1],color="red",lw=1.2)
axa.set_title(f"수준 산점도  Pearson(VIX,HYG)={pearson(vix,hyg):+.2f}\n(우하향=VIX↑일때 HYG↓=스프레드↑)")
axa.grid(alpha=.3)
cb=plt.colorbar(sc,ax=axa,fraction=.045); cb.set_label("시간순")
axb.scatter(dvix,dhyg,s=12,alpha=.5,color="#8e44ad")
zz=np.polyfit(dvix,dhyg,1); xs2=np.array([dvix.min(),dvix.max()])
axb.plot(xs2,zz[0]*xs2+zz[1],color="red",lw=1.2)
axb.axhline(0,color="gray",lw=.5); axb.axvline(0,color="gray",lw=.5)
axb.set_xlabel("ΔVIX (일간변화)"); axb.set_ylabel("ΔHYG (일간변화)")
axb.set_title(f"일간변화 산점도  Pearson(ΔVIX,ΔHYG)={pearson(dvix,dhyg):+.2f}")
axb.grid(alpha=.3)
plt.tight_layout(); plt.savefig("analysis/charts/61_corr_scatter.png",dpi=130); plt.close()
print("\nsaved: 60_corr_timeseries.png, 61_corr_scatter.png")
