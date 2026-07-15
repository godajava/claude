#!/usr/bin/env python3
"""SK하이닉스 리포트 웹 페이지 빌더.

사용법:
    python3 scripts/build_web.py <YYYY-MM-DD>

scripts/report_template.html에 당일 다크 차트 SVG를 인라인하고 두 버전을 생성한다:
  - reports/sk-hynix/latest.html  : Claude Artifact용 (CSP가 외부 스크립트를
    차단하므로 TradingView 위젯 제외)
  - docs/index.html               : GitHub Pages용 (TradingView 실시간 위젯 포함)
"""
import sys
import os

MARKERS = {
    "__PRICE_TREND__": "price_trend.svg",
    "__TREND3M__": "three_month_trend.svg",
    "__QUARTERLY__": "quarterly_earnings.svg",
    "__HBM__": "hbm_share.svg",
    "__TARGETS__": "target_prices.svg",
}

# TradingView 임베드 위젯 (다크 테마, KRX:000660).
# 데이터는 거래소 정책에 따라 실시간 또는 수분 지연으로 제공된다.
LIVE_WIDGETS = """<section>
<h2><span class="no">LIVE</span>실시간 시세 <small style="font-size:12px;font-weight:500;color:var(--muted)">TradingView 제공 · 거래소 정책에 따라 수분 지연될 수 있음</small></h2>
<div class="tradingview-widget-container" style="margin-bottom:14px">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
  {"symbol":"KRX:000660","width":"100%","locale":"kr","colorTheme":"dark","isTransparent":true}
  </script>
</div>
<div class="tradingview-widget-container" style="height:460px">
  <div class="tradingview-widget-container__widget" style="height:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {"symbol":"KRX:000660","interval":"5","timezone":"Asia/Seoul","theme":"dark","style":"1","locale":"kr","allow_symbol_change":false,"hide_top_toolbar":false,"save_image":false,"width":"100%","height":460}
  </script>
</div>
</section>
"""


def build(date):
    tpl = open("scripts/report_template.html").read()
    dark_dir = f"reports/sk-hynix/assets/{date}/dark/"
    for marker, fn in MARKERS.items():
        path = dark_dir + fn
        if marker in tpl:
            if not os.path.exists(path):
                sys.exit(f"오류: {path} 없음 — 먼저 hynix_charts.py --dark 실행 필요")
            tpl = tpl.replace(marker, open(path).read())

    artifact = tpl.replace("__LIVE_WIDGETS__", "")
    open("reports/sk-hynix/latest.html", "w").write(artifact)
    print(f"생성: reports/sk-hynix/latest.html ({len(artifact):,} bytes, 위젯 제외)")

    os.makedirs("docs", exist_ok=True)
    pages = tpl.replace("__LIVE_WIDGETS__", LIVE_WIDGETS)
    open("docs/index.html", "w").write(
        "<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<meta name=\"robots\" content=\"noindex\">"
        "</head><body>" + pages + "</body></html>"
    )
    print(f"생성: docs/index.html ({len(pages):,} bytes, 위젯 포함)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
