#!/usr/bin/env python3
"""Выгрузка SEO-данных Ангел-Дент из API Яндекс.Вебмастера и Метрики.

Токен НЕ хранится в репозитории. Скрипт читает его из переменной окружения
YANDEX_WEBMASTER_TOKEN (OAuth-токен с правами webmaster:hostinfo + metrika:read).
Как получить токен и куда его положить — см. scripts/README-yandex-api.md.

Запуск:
    YANDEX_WEBMASTER_TOKEN=xxxx python3 scripts/yandex-webmaster.py

Скрипт не деплоится (scripts/ исключён из rsync).
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error

WM_API = "https://api.webmaster.yandex.net/v4"
MT_API = "https://api-metrika.yandex.net/stat/v1/data"
METRIKA_COUNTER = "109369174"  # счётчик Метрики Ангел-Дент


def _token():
    t = os.environ.get("YANDEX_WEBMASTER_TOKEN", "").strip()
    if not t:
        sys.exit("Нет токена: задайте YANDEX_WEBMASTER_TOKEN (см. scripts/README-yandex-api.md).")
    return t


def _get(url):
    req = urllib.request.Request(url, headers={"Authorization": "OAuth " + _token()})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode("utf-8", "replace")[:400]}
    except Exception as e:
        return {"_error": str(e)}


def user_id():
    d = _get(f"{WM_API}/user/")
    if "user_id" not in d:
        sys.exit(f"Не удалось получить user_id: {d}")
    return str(d["user_id"])


def hosts(uid):
    d = _get(f"{WM_API}/user/{uid}/hosts/")
    return d.get("hosts", []) if isinstance(d, dict) else []


def host_report(uid, host_id):
    q = urllib.parse.quote(host_id, safe="")
    base = f"{WM_API}/user/{uid}/hosts/{q}"
    s = _get(f"{base}/summary/")
    print(f"  ИКС (SQI):            {s.get('sqi', '—')}")
    print(f"  Страниц в поиске:     {s.get('searchable_pages_count', '—')}")
    print(f"  Исключено страниц:    {s.get('excluded_pages_count', '—')}")
    diag = _get(f"{base}/diagnostics/")
    active = [(k, v.get("severity")) for k, v in (diag.get("problems", {}) or {}).items()
              if v.get("state") not in (None, "ABSENT", "NONE")]
    print(f"  Активные проблемы:    {active if active else 'нет'}")
    params = urllib.parse.urlencode({"order_by": "TOTAL_SHOWS",
        "query_indicator": ["TOTAL_SHOWS", "TOTAL_CLICKS", "AVG_SHOW_POSITION"], "limit": 30}, doseq=True)
    d = _get(f"{base}/search-queries/popular/?{params}")
    rows = d.get("queries", []) if isinstance(d, dict) else []
    print(f"\n  ТОП-{len(rows)} запросов (показы / клики / поз.показа):")
    print(f"  {'запрос':<52}{'пок':>6}{'клик':>6}{'поз':>7}")
    for qrow in rows:
        ind = qrow.get("indicators", {})
        sh = int(ind.get("TOTAL_SHOWS") or 0); cl = int(ind.get("TOTAL_CLICKS") or 0)
        ap = ind.get("AVG_SHOW_POSITION"); ap = f"{ap:.1f}" if ap else "—"
        print(f"  {qrow.get('query_text', '')[:51]:<52}{sh:>6}{cl:>6}{ap:>7}")


def metrika():
    def stat(params):
        return _get(MT_API + "?" + urllib.parse.urlencode(params))
    print("\n===== МЕТРИКА (счётчик %s, 30 дней) =====" % METRIKA_COUNTER)
    d = stat({"ids": METRIKA_COUNTER, "metrics": "ym:s:visits,ym:s:bounceRate,ym:s:avgVisitDurationSeconds",
              "dimensions": "ym:s:lastsignTrafficSource", "date1": "30daysAgo", "date2": "today", "limit": 20})
    if "_http_error" in d or "_error" in d:
        print("  Метрика недоступна:", d); return
    print(f"  {'источник':<26}{'визиты':>7}{'отказы':>8}{'ср.время':>10}")
    for r in d.get("data", []):
        m = r["metrics"]
        print(f"  {r['dimensions'][0]['name'][:25]:<26}{int(m[0]):>7}{m[1]:>7.0f}%{m[2]:>8.0f}с")
    print(f"  ИТОГО визитов: {int(d.get('totals', [0])[0])}")
    d2 = stat({"ids": METRIKA_COUNTER, "metrics": "ym:s:visits", "dimensions": "ym:s:startURLPathFull",
               "filters": "ym:s:lastsignTrafficSource=='organic'", "date1": "30daysAgo", "date2": "today", "limit": 12})
    if isinstance(d2, dict) and d2.get("data"):
        print("\n  Топ страниц входа из ПОИСКА:")
        for r in d2["data"]:
            print(f"    {int(r['metrics'][0]):>4}  {r['dimensions'][0]['name'][:64]}")


def main():
    uid = user_id(); print(f"user_id: {uid}")
    for h in hosts(uid):
        print("\n===== %s =====" % h.get("ascii_host_url", h.get("host_id")))
        print(f"  подтверждён: {h.get('verified')}")
        host_report(uid, h["host_id"])
    metrika(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
