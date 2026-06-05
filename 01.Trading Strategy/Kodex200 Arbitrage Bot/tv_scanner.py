#!/usr/bin/env python3
"""
tv_scanner.py
=============
TradingView '한국 주식 스크리너'가 내부적으로 호출하는 공개 스캐너 엔드포인트
(https://scanner.tradingview.com/korea/scan)에서 빅2 + KOSPI200 추종 ETF의
스냅샷(현재가/등락률/거래량)을 받아 상관 추적용 시계열로 적재한다.

  ⚠️ ToS 주의: TradingView 약관은 자동 스크래핑/재배포를 제한한다. 이 스크립트는
     '저빈도 스냅샷(수 초~분 간격) 수집·연구용'으로만 쓰고, 고빈도 폴링이나
     실시간 자동매매 트리거로 사용하지 말 것. 실시간/주문 시세는 증권사 API(KIS/토스)로
     받는 것이 라이선스·지연 양쪽에서 올바른 설계다. (verify_leadlag 와 역할 분담)

용도: 라이브 시세 소스가 아니라, 빅2와 ETF의 '스냅샷 등락률 상관'을 가볍게 추적하거나
      verify_leadlag.py 입력(ticks.csv)을 증권사 키 없이 만들고 싶을 때의 폴백.

실행:
  python tv_scanner.py                 # 1회 스냅샷 출력
  python tv_scanner.py --watch 30 --out tv_ticks.csv   # 30초 간격 수집 → CSV
"""
import argparse
import csv
import json
import os
import time
import urllib.request

ENDPOINT = "https://scanner.tradingview.com/korea/scan"

# instruments.js 와 동일 유니버스.
SYMBOLS = [
    ("KRX:005930", "삼성전자"),
    ("KRX:000660", "SK하이닉스"),
    ("KRX:069500", "KODEX 200"),
    ("KRX:102110", "TIGER 200"),
    ("KRX:122630", "KODEX 레버리지"),
    ("KRX:114800", "KODEX 인버스"),
    ("KRX:252670", "KODEX 200선물인버스2X"),
]
COLUMNS = ["close", "change", "volume"]


def fetch_snapshot():
    body = {
        "symbols": {"tickers": [s for s, _ in SYMBOLS], "query": {"types": []}},
        "columns": COLUMNS,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (research snapshot; low-frequency)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    rows = {}
    for item in payload.get("data", []):
        code = item["s"].split(":")[-1]
        d = item.get("d", [])
        rows[code] = dict(zip(COLUMNS, d))
    return rows


def print_snapshot(rows):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] TradingView 스냅샷")
    print(f"{'종목':<22}{'현재가':>12}{'등락률':>9}{'거래량':>14}")
    print("-" * 58)
    for ticker, name in SYMBOLS:
        code = ticker.split(":")[-1]
        r = rows.get(code)
        if not r:
            print(f"{name:<22}{'(no data)':>12}")
            continue
        close = r.get("close")
        chg = r.get("change")
        vol = r.get("volume")
        close_s = f"{close:,.0f}" if isinstance(close, (int, float)) else str(close)
        chg_s = f"{chg:+.2f}%" if isinstance(chg, (int, float)) else str(chg)
        vol_s = f"{vol:,.0f}" if isinstance(vol, (int, float)) else str(vol)
        print(f"{name:<22}{close_s:>12}{chg_s:>9}{vol_s:>14}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", type=int, default=0, help="N초 간격 반복 수집(0=1회)")
    ap.add_argument("--out", default=None, help="ticks.csv 호환 CSV로 적재(ts,code,price)")
    args = ap.parse_args()

    writer = None
    fh = None
    if args.out:
        new = not os.path.exists(args.out)
        fh = open(args.out, "a", newline="")
        writer = csv.writer(fh)
        if new:
            writer.writerow(["ts", "code", "price"])

    try:
        while True:
            try:
                rows = fetch_snapshot()
            except Exception as e:  # noqa: BLE001
                print(f"스냅샷 실패(엔드포인트 변경/차단 가능): {e}")
                print("→ ToS 준수 차원에서 재시도를 자제하고, 증권사 API 폴백을 권장.")
                if args.watch <= 0:
                    break
                time.sleep(args.watch)
                continue

            print_snapshot(rows)
            if writer:
                ts_ms = int(time.time() * 1000)
                for ticker, _ in SYMBOLS:
                    code = ticker.split(":")[-1]
                    r = rows.get(code)
                    if r and isinstance(r.get("close"), (int, float)):
                        writer.writerow([ts_ms, code, r["close"]])
                fh.flush()
            if args.watch <= 0:
                break
            time.sleep(args.watch)
    finally:
        if fh:
            fh.close()


if __name__ == "__main__":
    main()
