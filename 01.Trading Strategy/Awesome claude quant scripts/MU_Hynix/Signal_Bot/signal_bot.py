#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
signal_bot.py
=============
MU x SK하이닉스 매수/매도 시그널 봇.

기본 전략(리드-래그 모멘텀 A + 스프레드 평균회귀 B) 신호와
추가 전략 7종을 한 번에 계산해 signals.json 으로 출력한다.
index.html(정적 웹뷰)이 이 JSON을 읽어 대시보드로 렌더링한다.

사용
----
    python signal_bot.py --years 3 --outdir .
    python signal_bot.py --mock --outdir .      # 네트워크 없이 로직 검증

면책: 연구·교육용 보조 지표이며 투자 권유가 아니다. 모든 신호는 참고용이고
실제 투자에는 상당한 리스크가 따른다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint

warnings.filterwarnings("ignore")

TRADING_DAYS = 252

# 핵심 페어 + 보조 종목(추가 전략용). 보조 종목은 실패해도 봇이 계속 동작한다.
CORE_TICKERS = {"MU": "MU", "HYNIX_KRW": "000660.KS", "USDKRW": "KRW=X"}
AUX_TICKERS = {"SAMSUNG_KRW": "005930.KS", "HANMI_KRW": "042700.KS"}


# --------------------------------------------------------------------------- #
# 데이터
# --------------------------------------------------------------------------- #
def _download(tk: str, years: int) -> pd.Series | None:
    import yfinance as yf
    df = yf.download(tk, period=f"{years}y", auto_adjust=True, progress=False)
    if df is None or df.empty:
        return None
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close


def load_prices(years: int) -> tuple[pd.DataFrame, dict]:
    series, meta = {}, {}
    for name, tk in CORE_TICKERS.items():
        s = _download(tk, years)
        if s is None:
            raise RuntimeError(f"핵심 데이터를 받지 못했습니다: {tk}")
        series[name] = s
    for name, tk in AUX_TICKERS.items():
        s = _download(tk, years)
        if s is not None:
            series[name] = s
            meta[name] = True
        else:
            meta[name] = False
    px = pd.concat(series, axis=1)
    px.columns = list(series.keys())
    px = px.dropna(subset=list(CORE_TICKERS.keys()))
    if len(px) < 120:
        raise RuntimeError(f"공통 거래일이 너무 적습니다: {len(px)}일")
    return px, meta


def make_mock(years: int = 3, seed: int = 7) -> tuple[pd.DataFrame, dict]:
    """검증용 합성 데이터. MU가 하루 선행하는 구조 주입."""
    rng = np.random.default_rng(seed)
    n = years * TRADING_DAYS
    idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n)
    common = rng.normal(0, 0.018, n)
    mu_ret = 0.0004 + 0.9 * common + rng.normal(0, 0.012, n)
    hy_ret = 0.0002 + 0.55 * common + rng.normal(0, 0.013, n)
    hy_ret[1:] += 0.35 * mu_ret[:-1]
    ss_ret = 0.0002 + 0.45 * common + rng.normal(0, 0.012, n)
    hm_ret = 0.0003 + 0.40 * common + rng.normal(0, 0.020, n)
    hm_ret[1:] += 0.25 * hy_ret[:-1]            # 메모리 -> 장비 시차
    fx_ret = rng.normal(0, 0.004, n)
    px = pd.DataFrame({
        "MU": 80 * np.exp(np.cumsum(mu_ret)),
        "HYNIX_KRW": 90000 * np.exp(np.cumsum(hy_ret)),
        "USDKRW": 1330 * np.exp(np.cumsum(fx_ret)),
        "SAMSUNG_KRW": 70000 * np.exp(np.cumsum(ss_ret)),
        "HANMI_KRW": 100000 * np.exp(np.cumsum(hm_ret)),
    }, index=idx)
    return px, {"SAMSUNG_KRW": True, "HANMI_KRW": True}


def to_features(px: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=px.index)
    out["MU"] = px["MU"]
    out["HYNIX_KRW"] = px["HYNIX_KRW"]
    out["USDKRW"] = px["USDKRW"]
    out["HYNIX_USD"] = px["HYNIX_KRW"] / px["USDKRW"]
    out["lMU"] = np.log(out["MU"])
    out["lHY"] = np.log(out["HYNIX_USD"])
    out["rMU"] = out["lMU"].diff()
    out["rHY"] = out["lHY"].diff()
    out["rFX"] = np.log(out["USDKRW"]).diff()
    if "SAMSUNG_KRW" in px:
        out["SAMSUNG_USD"] = px["SAMSUNG_KRW"] / px["USDKRW"]
        out["rSS"] = np.log(out["SAMSUNG_USD"]).diff()
    if "HANMI_KRW" in px:
        out["HANMI_USD"] = px["HANMI_KRW"] / px["USDKRW"]
        out["rHM"] = np.log(out["HANMI_USD"]).diff()
    return out.dropna(subset=["rMU", "rHY", "rFX"])


# --------------------------------------------------------------------------- #
# 통계 헬퍼
# --------------------------------------------------------------------------- #
def leadlag(d: pd.DataFrame, a: str, b: str, k: int) -> tuple[float, float, int]:
    """corr(a[t-k], b[t]). k>0 이면 a가 b를 k일 선행."""
    pair = pd.concat([d[a].shift(k), d[b]], axis=1).dropna()
    if len(pair) < 30:
        return 0.0, 1.0, len(pair)
    r, p = stats.pearsonr(pair.iloc[:, 0], pair.iloc[:, 1])
    return float(r), float(p), len(pair)


def cointegration(d: pd.DataFrame):
    X = sm.add_constant(d["lMU"])
    ols = sm.OLS(d["lHY"], X).fit()
    const, beta = float(ols.params["const"]), float(ols.params["lMU"])
    adf_p = float(adfuller(ols.resid, autolag="AIC")[1])
    eg_p = float(coint(d["lHY"], d["lMU"])[1])
    valid = (adf_p < 0.05) or (eg_p < 0.05)
    return const, beta, adf_p, eg_p, valid


def zscore(d, beta, const, window=60) -> pd.Series:
    spread = d["lHY"] - (const + beta * d["lMU"])
    return (spread - spread.rolling(window).mean()) / spread.rolling(window).std()


def realized_vol(ret: pd.Series, window=20) -> float:
    r = ret.dropna().tail(window)
    return float(r.std() * np.sqrt(TRADING_DAYS)) if len(r) else 0.0


# --------------------------------------------------------------------------- #
# 시그널 계산
# --------------------------------------------------------------------------- #
def sig(action, conf, detail, extra=None):
    out = {"action": action, "confidence": conf, "detail": detail}
    if extra:
        out.update(extra)
    return out


def compute_core(d: pd.DataFrame):
    """기본 전략 A(리드-래그 모멘텀) + B(스프레드 평균회귀)."""
    mu_thr = float(d["rMU"].std())
    mu_last = float(d["rMU"].iloc[-1])

    # 리드-래그 교차상관표 (-3 ~ +3, MU 선행)
    ll_table = []
    for k in range(-3, 4):
        r, p, n = leadlag(d, "rMU", "rHY", k)
        ll_table.append({"lag_MU_lead": k, "corr": round(r, 4),
                         "p": round(p, 4), "n": n,
                         "sig5pct": p < 0.05})
    r1, p1, _ = leadlag(d, "rMU", "rHY", 1)

    # 신호 A: MU 직전일 ±1σ 초과 + +1일 상관 유의
    a_valid = p1 < 0.05
    if not a_valid:
        sigA = sig("HOLD", "low", "+1일 리드-래그 상관 비유의 — 모멘텀 신호 비활성")
    elif mu_last >= mu_thr:
        sigA = sig("BUY", "high" if mu_last >= 2 * mu_thr else "med",
                   f"MU 전일 +{mu_last*100:.2f}% (>+1σ) → 하이닉스 익일 매수",
                   {"mu_last_ret": round(mu_last, 4), "threshold": round(mu_thr, 4)})
    elif mu_last <= -mu_thr:
        sigA = sig("SELL", "high" if mu_last <= -2 * mu_thr else "med",
                   f"MU 전일 {mu_last*100:.2f}% (<-1σ) → 하이닉스 익일 매도/축소",
                   {"mu_last_ret": round(mu_last, 4), "threshold": round(mu_thr, 4)})
    else:
        sigA = sig("HOLD", "low",
                   f"MU 전일 {mu_last*100:.2f}% (|r|<1σ) → 트리거 미발생",
                   {"mu_last_ret": round(mu_last, 4), "threshold": round(mu_thr, 4)})

    # 공적분 + z + 신호 B
    const, beta, adf_p, eg_p, valid = cointegration(d)
    z = zscore(d, beta, const, 60)
    z_last = float(z.iloc[-1]) if not np.isnan(z.iloc[-1]) else 0.0
    if not valid:
        sigB = sig("HOLD", "low", "공적분 비유효 — 평균회귀 신호 비활성")
    elif z_last > 3 or z_last < -3:
        sigB = sig("NO-ENTRY", "low", f"z={z_last:.2f} (|z|>3) → 진입 금지/손절")
    elif z_last > 2:
        sigB = sig("SELL-SPREAD", "high" if z_last > 2.5 else "med",
                   f"z={z_last:.2f} (>+2) → 하이닉스 매도 + MU 매수")
    elif z_last < -2:
        sigB = sig("BUY-SPREAD", "high" if z_last < -2.5 else "med",
                   f"z={z_last:.2f} (<-2) → 하이닉스 매수 + MU 매도")
    elif abs(z_last) < 0.5:
        sigB = sig("FLAT", "low", f"z={z_last:.2f} (|z|<0.5) → 청산/관망")
    else:
        sigB = sig("HOLD", "low", f"z={z_last:.2f} → 진입 구간 아님")

    return {
        "mu_threshold_1sigma": round(mu_thr, 4),
        "mu_last_ret": round(mu_last, 4),
        "leadlag_table": ll_table,
        "leadlag_plus1": {"corr": round(r1, 4), "p": round(p1, 4)},
        "signal_A": sigA,
        "cointegration": {"beta": round(beta, 4), "adf_p": round(adf_p, 4),
                          "eg_p": round(eg_p, 4), "valid": valid},
        "z_last": round(z_last, 3),
        "signal_B": sigB,
    }, z


def compute_strategies(d: pd.DataFrame, core: dict, z: pd.Series, meta: dict):
    """추가 전략 7종."""
    strategies = []
    z_last = core["z_last"]
    mu_last = core["mu_last_ret"]
    mu_thr = core["mu_threshold_1sigma"]

    # 1. 3사 확장 페어 (MU · 하이닉스 · 삼성) — 디커플링 탐지
    if "rSS" in d:
        c_hy_ss, p_hy_ss, _ = leadlag(d, "rSS", "rHY", 0)
        # 최근 20일 하이닉스-삼성 상대강도
        rel = (d["rHY"] - d["rSS"]).tail(20).mean() * 100
        if abs(rel) > 0.15:
            act = "HYNIX>SAMSUNG (하이닉스 상대강세, HBM 독자재료 가능)" if rel > 0 \
                  else "SAMSUNG>HYNIX (삼성 상대강세)"
            conf = "med"
        else:
            act = "동조 (3사 동행)"
            conf = "low"
        strategies.append({
            "id": 1, "name": "3사 확장 페어 (MU·하이닉스·삼성)",
            "action": act, "confidence": conf,
            "detail": f"하이닉스-삼성 동시상관 {c_hy_ss:.2f}, 최근20일 상대강도 {rel:+.2f}%/일. "
                      f"하이닉스 단독 강세는 HBM 디커플링 신호로 MU 선행논리 약화.",
            "value": {"corr_hy_ss": round(c_hy_ss, 3), "rel_strength_20d_pct": round(rel, 3)},
        })
    else:
        strategies.append({"id": 1, "name": "3사 확장 페어 (MU·하이닉스·삼성)",
                           "action": "N/A", "confidence": "low",
                           "detail": "삼성전자 데이터 미수신 — 전략 비활성.", "value": {}})

    # 2. 장비·소재 공급망 스프레드 (메모리 -> 한미반도체 시차)
    if "rHM" in d:
        r_hm, p_hm, _ = leadlag(d, "rHY", "rHM", 1)   # 하이닉스(t-1) -> 한미(t)
        if p_hm < 0.05 and r_hm > 0.1:
            mom = "BUY" if mu_last >= mu_thr else ("SELL" if mu_last <= -mu_thr else "HOLD")
            act = f"공급망 전파 유효 → 한미반도체 {mom}"
            conf = "med"
        else:
            act = "공급망 시차 비유의 — 관망"
            conf = "low"
        strategies.append({
            "id": 2, "name": "장비·소재 공급망 스프레드 (→한미반도체)",
            "action": act, "confidence": conf,
            "detail": f"하이닉스(t-1)->한미(t) 시차상관 {r_hm:.2f} (p={p_hm:.3f}). "
                      f"메모리 강세가 장비주로 1일 전파되는지 점검.",
            "value": {"leadlag_corr": round(r_hm, 3), "p": round(p_hm, 3)},
        })
    else:
        strategies.append({"id": 2, "name": "장비·소재 공급망 스프레드 (→한미반도체)",
                           "action": "N/A", "confidence": "low",
                           "detail": "한미반도체 데이터 미수신 — 전략 비활성.", "value": {}})

    # 3. 환율 오버레이 (USD/KRW 조건부)
    fx_chg = float(d["rFX"].iloc[-1]) * 100
    fx_vol = realized_vol(d["rFX"], 20)
    if abs(fx_chg) > 1.5:
        act = f"환율 급변({fx_chg:+.2f}%) → 신호 A 신뢰도 하향"
        conf = "high"
    elif fx_chg < -0.3:
        act = "원화 강세 → 하이닉스 외국인 수급 우호 (가중 +)"
        conf = "med"
    elif fx_chg > 0.3:
        act = "원화 약세 → 하이닉스 외국인 수급 비우호 (가중 -)"
        conf = "med"
    else:
        act = "환율 안정 — 중립"
        conf = "low"
    strategies.append({
        "id": 3, "name": "환율 오버레이 (USD/KRW 조건부)",
        "action": act, "confidence": conf,
        "detail": f"전일 USD/KRW 변동 {fx_chg:+.2f}%, 20일 환율변동성 {fx_vol*100:.1f}%. "
                  f"±1.5% 초과 시 모멘텀 신호 신뢰도를 낮춘다.",
        "value": {"fx_last_chg_pct": round(fx_chg, 3), "fx_vol_ann_pct": round(fx_vol*100, 2)},
    })

    # 4. 변동성 타겟팅 / 포지션 사이징
    hy_vol = realized_vol(d["rHY"], 20)
    target_vol = 0.30
    size_mult = float(np.clip(target_vol / hy_vol, 0.2, 1.5)) if hy_vol > 0 else 1.0
    strategies.append({
        "id": 4, "name": "변동성 타겟팅 / 포지션 사이징",
        "action": f"포지션 배수 x{size_mult:.2f} (목표변동성 30%)",
        "confidence": "med" if size_mult < 0.8 else "low",
        "detail": f"하이닉스 20일 실현변동성 {hy_vol*100:.1f}%. 고정비중 대신 역가중으로 "
                  f"강세장 막바지 급락 리스크 완화. 배수<1이면 비중 축소 권고.",
        "value": {"realized_vol_pct": round(hy_vol*100, 2), "size_multiplier": round(size_mult, 2)},
    })

    # 5. 이벤트 드리븐 오버레이 (실적 캘린더 게이트)
    try:
        import yfinance as yf
        cal = yf.Ticker("MU").calendar
        ed = None
        if isinstance(cal, dict) and cal.get("Earnings Date"):
            ed = pd.Timestamp(cal["Earnings Date"][0])
        elif hasattr(cal, "loc") and "Earnings Date" in getattr(cal, "index", []):
            ed = pd.Timestamp(cal.loc["Earnings Date"][0])
    except Exception:
        ed = None
    if ed is not None:
        days_to = (ed.normalize() - d.index[-1].normalize()).days
        if abs(days_to) <= 3:
            act = f"MU 실적 임박(D{days_to:+d}) → 진입 차단(게이트 OFF)"
            conf = "high"
        else:
            act = f"MU 실적까지 {days_to}일 → 게이트 ON (신호 유효)"
            conf = "low"
        detail = f"다음 MU 실적 추정일 {ed.date()}. ±3거래일 구간은 신규 진입 금지."
    else:
        act = "실적일 미확인 — 수동 확인 권장"
        conf = "low"
        detail = "MU 실적 캘린더 미수신. 실적·메모리가격 발표·엔비디아 이벤트를 수동 게이트로."
    strategies.append({
        "id": 5, "name": "이벤트 드리븐 오버레이 (실적 게이트)",
        "action": act, "confidence": conf, "detail": detail,
        "value": {"mu_earnings_date": str(ed.date()) if ed is not None else None},
    })

    # 6. 레짐 스위칭 (60일선 기준)
    mu_ma = d["lMU"].rolling(60).mean().iloc[-1]
    hy_ma = d["lHY"].rolling(60).mean().iloc[-1]
    mu_above = d["lMU"].iloc[-1] > mu_ma
    hy_above = d["lHY"].iloc[-1] > hy_ma
    if mu_above and hy_above:
        regime, weight = "추세장 (둘 다 60일선 위)", "모멘텀 가중 ↑ / 평균회귀 ↓"
        conf = "med"
    elif (not mu_above) and (not hy_above):
        regime, weight = "약세장 (둘 다 60일선 아래)", "방어/현금 비중 ↑"
        conf = "med"
    else:
        regime, weight = "혼조 (엇갈림)", "평균회귀 가중 ↑"
        conf = "low"
    strategies.append({
        "id": 6, "name": "레짐 스위칭 모델 (60일선)",
        "action": f"{regime} → {weight}", "confidence": conf,
        "detail": "둘 다 60일선 위면 추세추종(신호 A 비중↑), 엇갈리면 평균회귀(신호 B 비중↑), "
                  "둘 다 아래면 방어. 국면별로 두 신호의 비중을 동적 배분.",
        "value": {"mu_above_ma60": bool(mu_above), "hy_above_ma60": bool(hy_above)},
    })

    # 7. 옵션 기반 표현 (공매도 제약 우회)
    if mu_last <= -mu_thr:
        opt = "하이닉스 풋 스프레드 (하방 베팅, 공매도 대체)"
        conf = "med"
    elif z_last < -2:
        opt = "하이닉스 콜 스프레드 (저평가 반등 베팅)"
        conf = "med"
    elif z_last > 2:
        opt = "하이닉스 콜 매도/풋 스프레드 (고평가 되돌림)"
        conf = "med"
    else:
        opt = "옵션 액션 없음 (방향성 트리거 미발생)"
        conf = "low"
    strategies.append({
        "id": 7, "name": "옵션 기반 표현 (공매도 제약 우회)",
        "action": opt, "confidence": conf,
        "detail": "한국 시장의 공매도·대차 제약과 업틱룰을 우회해 방향성 신호를 옵션 스프레드로 "
                  "표현. MU 하락 시그널은 풋, 저평가 반등은 콜로 변환.",
        "value": {},
    })

    return strategies


def build_recommendation(core: dict, strategies: list) -> dict:
    """기본 신호 A/B를 종합한 한 줄 요약."""
    a, b = core["signal_A"]["action"], core["signal_B"]["action"]
    parts = []
    if a in ("BUY", "SELL"):
        parts.append(f"모멘텀(A): 하이닉스 {a}")
    if b in ("BUY-SPREAD", "SELL-SPREAD"):
        parts.append(f"평균회귀(B): {b}")
    if not parts:
        headline = "관망 — 기본 트리거 미발생"
        bias = "NEUTRAL"
    else:
        headline = " / ".join(parts)
        bias = "LONG" if ("BUY" in a or b == "BUY-SPREAD") else "SHORT"
    # 레짐/환율 경고
    warns = []
    for s in strategies:
        if s["id"] == 3 and "하향" in s["action"]:
            warns.append("환율 급변으로 모멘텀 신뢰도 하향")
        if s["id"] == 5 and "차단" in s["action"]:
            warns.append("MU 실적 임박 — 신규 진입 차단")
        if s["id"] == 6 and "약세장" in s["action"]:
            warns.append("약세 레짐 — 방어 우선")
    return {"headline": headline, "bias": bias, "warnings": warns}


# --------------------------------------------------------------------------- #
def parse_args():
    ap = argparse.ArgumentParser(description="MU x SK하이닉스 시그널 봇")
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--outdir", type=str, default=".")
    ap.add_argument("--mock", action="store_true")
    return ap.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    if args.mock:
        px, meta = make_mock(args.years)
        source = "MOCK"
    else:
        px, meta = load_prices(args.years)
        source = "yfinance"
    d = to_features(px)

    core, z = compute_core(d)
    strategies = compute_strategies(d, core, z, meta)
    rec = build_recommendation(core, strategies)

    out = {
        "schema": "mu_hynix_signal_bot/1",
        "source": source,
        "generated_at": str(pd.Timestamp.utcnow().tz_localize(None)) + " UTC",
        "sample": {"start": str(d.index[0].date()),
                   "end": str(d.index[-1].date()), "days": int(len(d))},
        "prices": {
            "MU_usd": round(float(d["MU"].iloc[-1]), 2),
            "HYNIX_krw": round(float(d["HYNIX_KRW"].iloc[-1]), 0),
            "HYNIX_usd": round(float(d["HYNIX_USD"].iloc[-1]), 2),
            "USDKRW": round(float(d["USDKRW"].iloc[-1]), 2),
        },
        "core": core,
        "strategies": strategies,
        "recommendation": rec,
        "disclaimer": "연구·교육용 보조 지표이며 투자 권유가 아니다. 모든 신호는 참고용이고 "
                      "인샘플 특성과 레짐 의존성으로 실제 투자에는 상당한 리스크가 따른다.",
    }

    path = os.path.join(args.outdir, "signals.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # file:// 로 index.html 을 직접 열어도 데이터가 보이도록 JS 래퍼도 출력
    # (브라우저가 로컬 fetch(json)을 차단하기 때문)
    path_js = os.path.join(args.outdir, "signals.js")
    with open(path_js, "w", encoding="utf-8") as f:
        f.write("window.SIGNALS = " + json.dumps(out, ensure_ascii=False) + ";\n")

    # 콘솔 요약
    print(f"[signal_bot] source={source}  sample={out['sample']['start']}~{out['sample']['end']} "
          f"({out['sample']['days']}일)")
    print(f"[core] A={core['signal_A']['action']}  B={core['signal_B']['action']}  "
          f"z={core['z_last']}  +1일상관={core['leadlag_plus1']['corr']}")
    print(f"[reco] {rec['bias']} — {rec['headline']}")
    for s in strategies:
        print(f"  ({s['id']}) {s['name']}: {s['action']}")
    print(f"[out] {path}")


if __name__ == "__main__":
    sys.exit(main())
