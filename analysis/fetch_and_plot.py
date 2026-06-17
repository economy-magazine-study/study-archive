#!/usr/bin/env python3
"""한경 BUSINESS 역발상 투자 기사 관련 지표/지수 및 종목 데이터 수집 + 그래프.
데이터 소스: Yahoo Finance (chart + quoteSummary). HY 스프레드는 FRED 차단으로 HYG ETF 프록시 사용.
"""
import json, time, csv, datetime as dt
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
S = requests.Session(); S.headers.update(UA)

# ---- Yahoo crumb 인증 ----
def get_crumb():
    S.get("https://fc.yahoo.com", timeout=15)
    try:
        S.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15)
    except Exception: pass
    c = S.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15).text
    return c.strip()

CRUMB = get_crumb()
print("crumb:", CRUMB)

def chart(symbol, rng="1y", interval="1d"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={rng}&interval={interval}"
    for _ in range(4):
        try:
            r = S.get(url, timeout=20)
            if r.status_code == 200:
                res = r.json()["chart"]["result"][0]
                ts = res["timestamp"]
                close = res["indicators"]["quote"][0]["close"]
                dates, vals = [], []
                for t, c in zip(ts, close):
                    if c is not None:
                        dates.append(dt.datetime.utcfromtimestamp(t).date())
                        vals.append(c)
                return dates, vals
        except Exception as e:
            print("  retry", symbol, e)
        time.sleep(2)
    print("  FAILED", symbol)
    return [], []

def fundamentals(code6):
    """stockanalysis.com 통계 페이지에서 후행 PER/PBR 추출 (Yahoo는 KR 펀더멘털 미제공)."""
    url = f"https://stockanalysis.com/quote/krx/{code6}/statistics/__data.json"
    for _ in range(3):
        try:
            r = S.get(url, timeout=20, headers={"Referer": "https://stockanalysis.com/"})
            if r.status_code != 200:
                time.sleep(1); continue
            d = r.json()
            node = [n for n in d["nodes"] if isinstance(n, dict)
                    and isinstance(n.get("data"), list)][-1]
            data = node["data"]
            res = lambda i: data[i] if isinstance(i, int) and 0 <= i < len(data) else i
            pe = pb = None
            for obj in data:
                if isinstance(obj, dict) and "ratios" in obj:
                    blk = res(obj["ratios"])
                    for ri in res(blk["data"]):
                        row = res(ri)
                        if isinstance(row, dict):
                            rid = res(row.get("id"))
                            val = res(row.get("hover")) or res(row.get("value"))
                            if rid == "pe" and val not in (None, "n/a"):
                                pe = float(str(val).replace(",", ""))
                            elif rid == "pb" and val not in (None, "n/a"):
                                pb = float(str(val).replace(",", ""))
                    break
            return pe, pb
        except Exception as e:
            print("  fund err", code6, e); time.sleep(1)
    print("  fund FAILED", code6)
    return None, None

INDICES = {
    "^KS11": "KOSPI",
    "^VIX": "VIX (공포지수)",
    "HYG": "HYG ETF (HY스프레드 프록시)",
}
THEMES = {
    "반도체": {"005930.KS": "삼성전자", "000660.KS": "SK하이닉스"},
    "조선": {"009540.KS": "HD한국조선해양", "042660.KS": "한화오션", "010140.KS": "삼성중공업"},
    "전력인프라": {"267260.KS": "HD현대일렉트릭", "298040.KS": "효성중공업",
               "010120.KS": "LS ELECTRIC", "001440.KS": "대한전선"},
    "방산": {"012450.KS": "한화에어로스페이스", "064350.KS": "현대로템",
            "079550.KS": "LIG넥스원", "047810.KS": "한국항공우주"},
    "피지컬AI/완성차": {"005380.KS": "현대차"},
}

# ---- 한글 폰트 ----
def setup_font():
    import glob
    cands = glob.glob("/usr/share/fonts/truetype/korean/*.*") + \
            glob.glob("/usr/share/fonts/**/*Nanum*.*", recursive=True) + \
            glob.glob("/usr/share/fonts/**/*Noto*.*", recursive=True)
    for f in cands:
        try:
            font_manager.fontManager.addfont(f)
            name = font_manager.FontProperties(fname=f).get_name()
            rcParams["font.family"] = name
            print("font:", name, f)
            return True
        except Exception: pass
    print("WARN: no CJK font found")
    return False

HAS_FONT = setup_font()
rcParams["axes.unicode_minus"] = False

def save_series_csv(path, series_dict):
    # series_dict: name -> (dates, vals)
    all_dates = sorted({d for dates, _ in series_dict.values() for d in dates})
    idx = {name: dict(zip(dates, vals)) for name, (dates, vals) in series_dict.items()}
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date"] + list(series_dict.keys()))
        for d in all_dates:
            w.writerow([d.isoformat()] + [idx[n].get(d, "") for n in series_dict])

if __name__ == "__main__":
    CH = "analysis/charts"; DA = "analysis/data"
    today = dt.date.today().isoformat()

    # ===== 1) 지수/지표 수집 =====
    print("== indices ==")
    idx_series = {}
    for sym, name in INDICES.items():
        d, v = chart(sym)
        if v:
            idx_series[name] = (d, v)
            print(f"  {name}: {len(v)} pts, last={v[-1]:.2f} ({d[-1]})")
    save_series_csv(f"{DA}/indices_1y.csv", idx_series)

    # ===== 2) 종목 가격 수집 =====
    print("== stocks ==")
    stock_series = {}     # name -> (dates, vals)
    fund = {}             # name -> (pe, pb, price)
    sym2name = {}
    for theme, members in THEMES.items():
        for sym, name in members.items():
            sym2name[sym] = name
            d, v = chart(sym)
            price = v[-1] if v else None
            if v:
                stock_series[name] = (d, v)
            pe, pb = fundamentals(sym.split(".")[0])
            fund[name] = (pe, pb, price)
            print(f"  [{theme}] {name}: px={price} PER={pe} PBR={pb}")
            time.sleep(0.3)
    save_series_csv(f"{DA}/stocks_price_1y.csv", stock_series)
    with open(f"{DA}/fundamentals.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["company", "PER", "PBR", "price_KRW"])
        for n, (pe, pb, pr) in fund.items():
            w.writerow([n, pe, pb, pr])

    # ===== Chart A: KOSPI =====
    if "KOSPI" in idx_series:
        d, v = idx_series["KOSPI"]
        plt.figure(figsize=(11, 4.5))
        plt.plot(d, v, color="#c0392b", lw=1.6)
        plt.title(f"KOSPI 지수 — 최근 1년 (~{d[-1]})")
        plt.ylabel("지수"); plt.grid(alpha=.3); plt.tight_layout()
        plt.savefig(f"{CH}/01_kospi.png", dpi=130); plt.close()

    # ===== Chart B: VIX with thresholds =====
    if "VIX (공포지수)" in idx_series:
        d, v = idx_series["VIX (공포지수)"]
        plt.figure(figsize=(11, 4.5))
        plt.plot(d, v, color="#2c3e50", lw=1.4)
        plt.axhline(25, color="orange", ls="--", lw=1, label="25 (공포 확산)")
        plt.axhline(30, color="red", ls="--", lw=1, label="30 (극도 공포·역발상 매수)")
        plt.title(f"VIX 공포지수 — 최근 1년 (~{d[-1]})")
        plt.ylabel("VIX"); plt.legend(); plt.grid(alpha=.3); plt.tight_layout()
        plt.savefig(f"{CH}/02_vix.png", dpi=130); plt.close()

    # ===== Chart C: HY proxy (HYG) =====
    if "HYG ETF (HY스프레드 프록시)" in idx_series:
        d, v = idx_series["HYG ETF (HY스프레드 프록시)"]
        plt.figure(figsize=(11, 4.5))
        plt.plot(d, v, color="#16a085", lw=1.4)
        plt.title(f"HYG 하이일드 ETF — 최근 1년 (HY스프레드 프록시, 가격↑=스프레드↓ 안정) (~{d[-1]})")
        plt.ylabel("USD"); plt.grid(alpha=.3); plt.tight_layout()
        plt.savefig(f"{CH}/03_hyg.png", dpi=130); plt.close()

    # ===== Chart D: per-theme rebased stock prices (100 = 1년전) =====
    for i, (theme, members) in enumerate(THEMES.items(), 1):
        names = [n for n in members.values() if n in stock_series]
        if not names: continue
        plt.figure(figsize=(11, 4.8))
        for n in names:
            d, v = stock_series[n]
            base = v[0]
            reb = [x / base * 100 for x in v]
            plt.plot(d, reb, lw=1.5, label=f"{n} ({v[-1]:,.0f}원)")
        plt.axhline(100, color="gray", ls=":", lw=1)
        plt.title(f"[{theme}] 주가 추이 — 1년전=100 기준 리베이스")
        plt.ylabel("리베이스 지수(=100)"); plt.legend(fontsize=8); plt.grid(alpha=.3)
        safe = theme.replace("/", "-")
        plt.tight_layout(); plt.savefig(f"{CH}/1{i}_theme_{safe}.png", dpi=130); plt.close()

    # ===== Chart E: PER / PBR bar charts =====
    comp = [n for n in fund if fund[n][0] is not None]
    if comp:
        comp_sorted = sorted(comp, key=lambda n: fund[n][0])
        pes = [fund[n][0] for n in comp_sorted]
        plt.figure(figsize=(11, 5))
        bars = plt.barh(comp_sorted, pes, color="#2980b9")
        for b, p in zip(bars, pes):
            plt.text(b.get_width(), b.get_y()+b.get_height()/2, f" {p:.1f}", va="center", fontsize=8)
        plt.title(f"종목별 PER (후행, {today} 기준 · 출처 stockanalysis.com)")
        plt.xlabel("PER(배)"); plt.grid(axis="x", alpha=.3); plt.tight_layout()
        plt.savefig(f"{CH}/20_per.png", dpi=130); plt.close()

    compb = [n for n in fund if fund[n][1] is not None]
    if compb:
        compb_sorted = sorted(compb, key=lambda n: fund[n][1])
        pbs = [fund[n][1] for n in compb_sorted]
        plt.figure(figsize=(11, 5))
        bars = plt.barh(compb_sorted, pbs, color="#8e44ad")
        for b, p in zip(bars, pbs):
            plt.text(b.get_width(), b.get_y()+b.get_height()/2, f" {p:.2f}", va="center", fontsize=8)
        plt.title(f"종목별 PBR ({today} 기준 · 출처 stockanalysis.com)")
        plt.xlabel("PBR(배)"); plt.grid(axis="x", alpha=.3); plt.tight_layout()
        plt.savefig(f"{CH}/21_pbr.png", dpi=130); plt.close()

    print("DONE. charts in", CH)

