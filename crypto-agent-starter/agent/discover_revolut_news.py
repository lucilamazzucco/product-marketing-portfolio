#!/usr/bin/env python3
"""Discover potentially relevant Revolut announcements through a public RSS index.

This is a DISCOVERY fallback, not a way around Revolut's HTTP 403 restrictions.
A feed headline is NOT verification of an official article's contents.
"""
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
QUERIES = [
    'site:revolut.com/news/ crypto Revolut',
    'site:help.revolut.com/help/wealth/cryptocurrencies/ crypto',
]
MAX_ITEMS = 20

def discover(query):
    url = "https://news.google.com/rss/search?" + urlencode({
        "q": query, "hl": "en-GB", "gl": "GB", "ceid": "GB:en"
    })
    req = Request(url, headers={
        "User-Agent": "PMMResearchPortfolio/1.0 (independent research)",
        "Accept": "application/rss+xml,application/xml,text/xml",
    })
    with urlopen(req, timeout=25) as response:
        data = response.read(1_000_001)
        if len(data) > 1_000_000:
            raise ValueError("RSS feed exceeded size limit")
    root = ET.fromstring(data)
    results = []
    for item in root.findall("./channel/item")[:MAX_ITEMS]:
        results.append({
            "title": (item.findtext("title") or "").strip(),
            "indexed_url": (item.findtext("link") or "").strip(),
            "published": (item.findtext("pubDate") or "").strip(),
            "query": query,
            "verification": "Unverified index hit; official-page contents not fetched",
        })
    return results

def main():
    found, errors = {}, []
    for query in QUERIES:
        try:
            for item in discover(query):
                link = item["indexed_url"]
                if link and link not in found:
                    found[link] = item
            print("Discovery search OK:", query)
        except Exception as exc:
            errors.append({"query": query, "error": type(exc).__name__ + ": " + str(exc)[:150]})
            print("Discovery search unavailable:", query, type(exc).__name__)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    report = {
        "run_at": now,
        "method": "Public third-party RSS news index (not an official Revolut API)",
        "status": "discovery-only; not content verification",
        "items": list(found.values()),
        "errors": errors,
    }
    (REPORTS / "revolut-news-discovery.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Revolut Crypto — indexed announcement discovery", "",
        f"Checked: {now}", "",
        "> This is a supplementary discovery feed, not a verified reading of Revolut content.",
        "> Links may point to Google News redirects, be outdated, or lead to unrelated results.",
        "> Confirm any finding on an official Revolut page before using it in PMM recommendations.",
        "",
    ]
    for item in found.values():
        title = item["title"].replace("[", "(").replace("]", ")")
        lines.append(f"- [{title}]({item['indexed_url']}) — {item['published']} — **unverified**")
    if not found:
        lines.append("No discoverable results returned; this does NOT imply no Revolut updates.")
    if errors:
        lines += ["", "## Fetch errors", ""]
        for err in errors:
            lines.append(f"- {err['query']}: {err['error']}")
    (REPORTS / "revolut-news-discovery.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Indexed announcement candidates:", len(found), "| Feed errors:", len(errors))

if __name__ == "__main__":
    main()
