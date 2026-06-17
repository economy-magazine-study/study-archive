#!/usr/bin/env python3
"""박세익 대표의 '공포의 중심에서 매수' 역발상 전략 백테스트 (실데이터).
- 신호: VIX>=30 (강) / VIX>=25 (경고)  ※ 실제 30돌파일 = 2026-03-27
- 코어 바스켓을 동일가중 보유했을 때 시나리오별 결과 비교.
데이터: analysis/data/*.csv (Yahoo Finance, 2025-06-16~2026-06-16)
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
    cols={c:[] for c in rows[0] if c!="date"}
    dates=[]
    for r in rows:
        dates.append(dt.date.fromisoformat(r["date"]))
        for c in cols:
            cols[c].append(float(r[c]) if r[c] else None)
    return dates, cols

idx_dates, idx = load("analysis/data/indices_1y.csv")
st_dates, st = load("analysis/data/stocks_price_1y.csv")

VIX = dict(zip(idx_dates, idx["VIX (공포지수)"]))
KOSPI = {d:v for d,v in zip(idx_dates, idx["KOSPI"]) if v}

# ---- 바스켓 정의 ----
NAMED = ["삼성전자","SK하이닉스","HD한국조선해양","한화에어로스페이스","현대차"]  # 기사 직접 언급
ALL15 = list(st.keys())

def price_on_or_after(name, target):
    """target 이후 첫 유효 가격과 그 날짜."""
    for d, v in zip(st_dates, st[name]):
        if d >= target and v is not None:
            return d, v
    return None, None

def basket_value_series(names, buy_date):
    """buy_date 매수 시 동일가중 바스켓 가치(매수일=100) 시계열."""
    base = {}
    for n in names:
        d, p = price_on_or_after(n, buy_date)
        base[n] = p
    series = []
    for i, d in enumerate(st_dates):
        if d < buy_date: continue
        vals = []
        for n in names:
            p = st[n][i]
            if p is not None and base[n]:
                vals.append(p / base[n])
        if vals:
            series.append((d, sum(vals)/len(vals)*100))
    return series

def ret_pct(names, buy_date, end_date=None):
    s = basket_value_series(names, buy_date)
    if not s: return None
    end = s[-1][1] if end_date is None else next(v for d,v in s if d>=end_date)
    return end - 100  # since base=100

# ---- 주요 날짜 ----
SIG30 = dt.date(2026,3,27)              # VIX 30 돌파 (강신호)
# VIX>=25 첫 날
SIG25 = next(d for d in idx_dates if VIX.get(d) and VIX[d]>=25)
TODAY = st_dates[-1]
YEAR_AGO = st_dates[0]
# 직전 고점(폭락 전 최악의 매수 타이밍): 2026-01-01~3-27 사이 바스켓 최고일
pre = [(d, sum(st[n][i]/[p for dd,p in [price_on_or_after(n,YEAR_AGO)]][0] for n in NAMED if st[n][i])/len(NAMED))
       for i,d in enumerate(st_dates) if dt.date(2026,1,1)<=d<=SIG30]
PEAK = max(pre, key=lambda x:x[1])[0]
# 바스켓 저점 (2026-02~04)
lo = [(d, sum((st[n][i] or 1e18) for n in NAMED)) for i,d in enumerate(st_dates) if dt.date(2026,2,1)<=d<=dt.date(2026,4,30)]

print(f"VIX25 첫신호: {SIG25} | VIX30 강신호: {SIG30} | 폭락전 고점: {PEAK} | 오늘: {TODAY}")

# ---- 시나리오 수익률 ----
def kospi_ret(buy):
    bd = next(d for d in idx_dates if d>=buy and KOSPI.get(d))
    return (KOSPI[TODAY]/KOSPI[bd]-1)*100, bd

scen = []
for label, names in [("기사 언급 5종목", NAMED), ("확장 테마 15종목", ALL15)]:
    scen.append((f"① 공포매수 VIX≥30 ({SIG30})·{label}", ret_pct(names, SIG30)))
    scen.append((f"② 경고매수 VIX≥25 ({SIG25})·{label}", ret_pct(names, SIG25)))
    scen.append((f"③ 폭락前 고점매수 ({PEAK})·{label}", ret_pct(names, PEAK)))
    scen.append((f"④ 1년전 매수후보유·{label}", ret_pct(names, YEAR_AGO)))

kr30,_=kospi_ret(SIG30); kr_year,_=kospi_ret(YEAR_AGO)
print("\n=== 시나리오별 수익률 (→2026-06-16) ===")
for l,r in scen:
    print(f"  {l}: {r:+.1f}%")
print(f"  [벤치] KOSPI VIX≥30매수: {kr30:+.1f}% | KOSPI 1년보유: {kr_year:+.1f}%")

# ---- 3월 공포국면 정밀 분석: 저점/분할매수 ----
def basket_price_index(names, i):
    """i번째 거래일의 동일가중 바스켓 지수(1년전=100)."""
    base=[price_on_or_after(n,YEAR_AGO)[1] for n in names]
    vals=[st[n][i]/b for n,b in zip(names,base) if st[n][i] and b]
    return sum(vals)/len(vals)*100 if vals else None

# 3월 공포국면 바스켓 저점 (2026-02-27 ~ 2026-04-30)
march = [(d, basket_price_index(NAMED,i)) for i,d in enumerate(st_dates)
         if dt.date(2026,2,27)<=d<=dt.date(2026,4,30)]
BOTTOM = min(march, key=lambda x:x[1])[0]

# 분할매수: 폭락 구간(고점~저점)을 4등분한 날짜에 동일금액 4회
span=[d for d in st_dates if PEAK<=d<=BOTTOM]
tranche_dates=[span[round(k*(len(span)-1)/3)] for k in range(4)]
def split_buy_ret(names):
    # 각 트란치 동일금액 → 최종가치 = 평균(현재가/매수가)
    rs=[]
    for bd in tranche_dates:
        r=ret_pct(names,bd)
        if r is not None: rs.append(1+r/100)
    return (sum(rs)/len(rs)-1)*100 if rs else None

# 패닉셀: 1년전 매수했다가 VIX≥30(3/27)에 전량 매도 → 이후 현금
def panic_sell_ret(names):
    s=basket_value_series(names, YEAR_AGO)
    return next(v for d,v in s if d>=SIG30)-100   # 매도시점까지 수익, 이후 0

print(f"\n3월 공포국면: 고점 {PEAK} → 저점 {BOTTOM}")
print(f"분할매수일: {tranche_dates}")
print(f"  분할매수(5종목): {split_buy_ret(NAMED):+.1f}%  vs 고점일괄 {ret_pct(NAMED,PEAK):+.1f}%  vs 저점일괄 {ret_pct(NAMED,BOTTOM):+.1f}%")
print(f"  패닉셀(5종목, 3/27 전량매도후 현금): {panic_sell_ret(NAMED):+.1f}%  vs 보유지속 {ret_pct(NAMED,YEAR_AGO):+.1f}%")

# ---- Chart 1: 바스켓 가치 추이 (1년전=100) + 신호일 ----
plt.figure(figsize=(12,5.5))
for names,lab,col in [(NAMED,"기사 언급 5종목 바스켓","#c0392b"),(ALL15,"확장 테마 15종목 바스켓","#2980b9")]:
    s=basket_value_series(names, YEAR_AGO)
    plt.plot([d for d,_ in s],[v for _,v in s],label=lab,color=col,lw=1.8)
# KOSPI rebased
kd=[d for d in idx_dates if KOSPI.get(d)]; kb=KOSPI[kd[0]]
plt.plot(kd,[KOSPI[d]/kb*100 for d in kd],label="KOSPI",color="gray",lw=1.2,ls="--")
plt.axvline(SIG25,color="orange",ls=":",lw=1.2); plt.text(SIG25,plt.ylim()[1]*0.97,"VIX≥25",rotation=90,va="top",fontsize=8,color="orange")
plt.axvline(SIG30,color="red",ls=":",lw=1.4); plt.text(SIG30,plt.ylim()[1]*0.97,"VIX≥30 강신호",rotation=90,va="top",fontsize=8,color="red")
plt.axhline(100,color="black",lw=.6,alpha=.4)
plt.title("역발상 코어 바스켓 vs KOSPI — 1년전(2025-06-16)=100")
plt.ylabel("지수(=100)"); plt.legend(); plt.grid(alpha=.3); plt.tight_layout()
plt.savefig("analysis/charts/30_backtest_value.png",dpi=130); plt.close()

# ---- Chart 2: '현금을 들고 있다가 3월 공포에 매수' — 매수 타이밍 비교 (모두 3월 투입) ----
items=[
    ("폭락前 고점 일괄매수\n(2/27·최악 타이밍)", ret_pct(NAMED,PEAK), "#e67e22"),
    ("분할매수\n(고점→저점 4회 분할)", split_buy_ret(NAMED), "#d35400"),
    ("VIX≥30 신호 일괄매수\n(3/27·공포의 정점)", ret_pct(NAMED,SIG30), "#c0392b"),
    ("[벤치] KOSPI\n(3/27 매수후보유)", kr30, "#34495e"),
    ("저점 일괄매수\n(3/31 바닥·사후적 이상치)", ret_pct(NAMED,BOTTOM), "#16a085"),
]
items.sort(key=lambda x:x[1])
plt.figure(figsize=(11.5,6))
bars=plt.barh([l for l,_,_ in items],[v for _,v,_ in items],color=[c for _,_,c in items])
for b,(_,v,_) in zip(bars,items):
    plt.text(b.get_width(),b.get_y()+b.get_height()/2,f" {v:+.1f}%",va="center",fontsize=10)
plt.axvline(0,color="black",lw=.8)
plt.title("[현금 → 3월 공포국면에 매수] 타이밍별 수익률 → 2026-06-16\n(기사 언급 5종목 동일가중·배당제외)")
plt.xlabel("수익률(%)"); plt.grid(axis="x",alpha=.3); plt.tight_layout()
plt.savefig("analysis/charts/31_backtest_timing.png",dpi=130); plt.close()

# ---- Chart 3: '이미 보유 중' — 공포에 팔았나 vs 버텼나 (모두 1년전 매수 기준) ----
items2=[
    ("공포에 매도(패닉셀)\n3/27 전량매도→현금", panic_sell_ret(NAMED), "#c0392b"),
    ("[벤치] KOSPI 1년보유", kr_year, "#34495e"),
    ("끝까지 보유(역발상)\n1년전 매수후 계속보유", ret_pct(NAMED,YEAR_AGO), "#27ae60"),
]
items2.sort(key=lambda x:x[1])
plt.figure(figsize=(11.5,4.2))
bars=plt.barh([l for l,_,_ in items2],[v for _,v,_ in items2],color=[c for _,_,c in items2])
for b,(_,v,_) in zip(bars,items2):
    plt.text(b.get_width(),b.get_y()+b.get_height()/2,f" {v:+.1f}%",va="center",fontsize=10)
plt.axvline(0,color="black",lw=.8)
gap=ret_pct(NAMED,YEAR_AGO)-panic_sell_ret(NAMED)
plt.title(f"[이미 보유 중] 3월 공포에 팔았다면? — 끝까지 보유 대비 {gap:.0f}%p 기회손실\n(기사 언급 5종목 동일가중·1년전=0% 기준)")
plt.xlabel("수익률(%)"); plt.grid(axis="x",alpha=.3); plt.tight_layout()
plt.savefig("analysis/charts/32_backtest_panic.png",dpi=130); plt.close()
print("\ncharts saved: 30_backtest_value.png, 31_backtest_timing.png, 32_backtest_panic.png")
