#!/usr/bin/env python3
"""Track recent Revolut Crypto indexed announcements (discovery only).

Public Google News RSS is a third-party index. Headlines are not validated
official-page content, and cannot establish whether a product changed.
"""
import datetime as dt
import json
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
SEEN_FILE = REPORTS / "revolut-news-seen.json"
WINDOW_DAYS = 30
MAX_ITEMS = 35
QUERIES = [
    'site:revolut.com/news/ crypto when:30d',
    'site:help.revolut.com/help/wealth/cryptocurrencies/ when:30d',
]
TOPICS = {
    "Pricing & fees": ("fee", "spread", "pricing", "commission", "exchange rate"),
    "Onboarding & eligibility": ("onboard", "verification", "knowledge test", "eligible", "suitability"),
    "Education & risks": ("learn", "education", "risk", "protect", "scam", "security"),
    "Features & transfers": ("crypto", "bitcoin", "token", "wallet", "staking", "withdraw", "deposit", "trade", "transfer", "stablecoin"),
    "Regulatory & availability": ("licence", "license", "regulat", "approval", "authorisation", "authorization", "restriction"),
}
KEYWORDS = tuple(dict.fromkeys(word for words in TOPICS.values() for word in words))
EXCLUDE = ("revolut x", "revolut ramp")
def normalized_title(title):
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"\s+-\s+revolut\s*$", "", title, flags=re.I).lower()).strip()

def classification(title):
    lower = title.lower()
    if any(word in lower for word in EXCLUDE):
        return "Advanced product context"
    if not any(word in lower for word in KEYWORDS):
        return None
    for topic, words in TOPICS.items():
        if any(word in lower for word in words):
            return topic
    return "Other crypto"

def feed(query):
    url = "https://news.google.com/rss/search?" + urlencode({
        "q": query, "hl": "en-GB", "gl": "GB", "ceid": "GB:en"
    })
    req = Request(url, headers={
        "User-Agent": "PMMResearchPortfolio/1.0 (independent research)",
        "Accept": "application/rss+xml,application/xml,text/xml",
    })
    with urlopen(req, timeout=25) as response:
        raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("RSS feed exceeded 1 MB")
    return ET.fromstring(raw).findall("./channel/item")[:MAX_ITEMS]

def main():
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=WINDOW_DAYS)
    try:
        seen = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
        if not isinstance(seen, dict):
            seen = {}
    except (OSError, ValueError):
        seen = {}
    candidates, errors = {}, []
    for query in QUERIES:
        try:
            for entry in feed(query):
                title = (entry.findtext("title") or "").strip()
                link = (entry.findtext("link") or "").strip()
                published = (entry.findtext("pubDate") or "").strip()
                if not title or not link or not published:
                    continue
                try:
                    timestamp = parsedate_to_datetime(published).astimezone(dt.timezone.utc)
                except (TypeError, ValueError):
                    continue
                if timestamp < cutoff or timestamp > now + dt.timedelta(days=1):
                    continue
                topic = classification(title)
                if topic is None:
                    continue
                key = normalized_title(title)
                if not key:
                    continue
                candidates.setdefault(key, {
                    "title": title,
                    "indexed_url": link,
                    "published": timestamp.isoformat(),
                    "topic": topic,
                    "journey_scope": "Revolut X: context only" if topic == "Advanced product context" else "Revolut Crypto: candidate",
                    "verification": "UNVERIFIED: index headline only; official article not fetched",
                    "is_new": key not in seen,
                })
            print("Indexed discovery query processed:", query)
        except Exception as exc:
            errors.append({"query": query, "error": type(exc).__name__ + ": " + str(exc)[:150]})
            print("RSS query unavailable:", query, type(exc).__name__)
    selected = sorted(candidates.values(), key=lambda x: x["published"], reverse=True)
    for key, item in candidates.items():
        seen.setdefault(key, now.isoformat())
    # Retain recent history to avoid repeating an indexed headline across weekly runs.
    prune = now - dt.timedelta(days=120)
    seen = {key: value for key, value in seen.items()
            if isinstance(value, str) and _recent(value, prune)}
    SEEN_FILE.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {
        "checked_at": now.isoformat(),
        "window_days": WINDOW_DAYS,
        "method": "Public third-party Google News RSS; not an official Revolut API",
        "verified_official_articles": 0,
        "candidate_count": len(selected),
        "new_candidate_count": sum(i["is_new"] for i in selected),
        "advanced_context_count": sum(i["topic"] == "Advanced product context" for i in selected),
        "items": selected,
        "errors": errors,
    }
    (REPORTS / "revolut-news-discovery.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Revolut Crypto — indexed announcement discovery", "",
        f"Checked: **{now.isoformat()}** · Lookback: **{WINDOW_DAYS} days**", "",
        "> Discovery only. These are third-party index headlines, NOT validated Revolut updates.",
        "> A page listed here has not been read from Revolut; dates are index publication dates.",
        "> Manual verification of the official page, UK applicability and claims is required.", "",
        f"**Recent relevant candidates:** {len(selected)} · **New this run:** {summary['new_candidate_count']}",
        f" · **Official articles verified:** 0", "",
    ]
    if not selected:
        lines.append("No qualifying indexed headlines were returned. This does NOT establish that Revolut made no changes.")
    for item in selected:
        title = item["title"].replace("[", "(").replace("]", ")")
        label = "NEW" if item["is_new"] else "seen before"
        lines += [
            f"- [{title}]({item['indexed_url']})",
            f"  - {item['published'][:10]} · {item['topic']} · {item['journey_scope']} · {label} · **unverified**",
        ]
    if errors:
        lines += ["", "## Feed errors", ""]
        lines.extend(f"- {e['query']}: {e['error']}" for e in errors)
    (REPORTS / "revolut-news-discovery.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Recent candidates:", len(selected), "New:", summary["new_candidate_count"],
          "RSS errors:", len(errors))

def _recent(iso, cutoff):
    try:
        return dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc) >= cutoff
    except (TypeError, ValueError):
        return False

if __name__ == "__main__":
    main()
