#!/usr/bin/env python3
"""SK하이닉스(000660.KS) 시세 수집기 (의존성 없음, 야후 파이낸스 차트 API).

사용법:
    python3 scripts/fetch_quote.py [출력경로=docs/quote.json]

현재가·등락과 최근 2거래일 일봉(시가/고가/저가/종가/거래량)을 JSON으로 저장한다.
GitHub Actions(quote.yml)가 장중 주기 실행해 Pages에 배포하고,
아침 리포트 루틴은 전일 상세 시세 표를 채우는 데 사용한다.
실패 시 비정상 종료해 기존 quote.json을 덮어쓰지 않는다.
"""
import json
import sys
import time
import urllib.request

URL = ("https://query1.finance.yahoo.com/v8/finance/chart/000660.KS"
       "?range=5d&interval=1d")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/quote.json"
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)

    result = data["chart"]["result"][0]
    meta = result["meta"]
    ts = result.get("timestamp") or []
    q = result["indicators"]["quote"][0]

    days = []
    for i, t in enumerate(ts):
        if q["close"][i] is None:
            continue
        days.append({
            "date": time.strftime("%Y-%m-%d", time.gmtime(t + 9 * 3600)),  # KST
            "open": q["open"][i], "high": q["high"][i], "low": q["low"][i],
            "close": q["close"][i], "volume": q["volume"][i],
        })

    price = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    if not price or not days:
        sys.exit("오류: 시세 데이터 없음")

    payload = {
        "symbol": "000660.KS",
        "price": price,
        "previousClose": prev,
        "change": round(price - prev) if prev else None,
        "changePercent": round((price - prev) / prev * 100, 2) if prev else None,
        "marketTime": time.strftime("%Y-%m-%d %H:%M KST",
                                    time.gmtime(meta.get("regularMarketTime", 0) + 9 * 3600)),
        "fetchedAt": time.strftime("%Y-%m-%d %H:%M KST", time.gmtime(time.time() + 9 * 3600)),
        "days": days[-2:],  # [전일, 당일] 또는 [전전일, 전일]
    }
    with open(out, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"저장: {out} — 현재가 {price:,.0f} ({payload['changePercent']}%), 일봉 {len(days)}개")


if __name__ == "__main__":
    main()
