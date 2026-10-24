#!/usr/bin/env python3
"""Report source discovery and successful HTTP extraction separately by brand."""
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
SOURCES = ROOT / 'agent' / 'sources.json'

BRANDS = ['Revolut', 'PayPal', 'bunq', 'N26', 'Coinbase']

def brand(url):
    domain = urlsplit(url).hostname or ''
    if domain == 'revolut.com' or domain.endswith('.revolut.com'):
        return 'Revolut'
    if domain == 'paypal.com' or domain.endswith('.paypal.com'):
        return 'PayPal'
    if domain == 'bunq.com' or domain.endswith('.bunq.com'):
        return 'bunq'
    if domain == 'n26.com' or domain.endswith('.n26.com'):
        return 'N26'
    if domain == 'coinbase.com' or domain.endswith('.coinbase.com'):
        return 'Coinbase'
    return 'Other'

def load_json(file, default):
    try:
        return json.loads(file.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default

def main():
    sources = load_json(SOURCES, [])
    last = load_json(REPORTS / 'latest.json', {})
    records = last.get('sources', [])
    by_url = {r.get('url'): r for r in records}
    counts = {}
    for company in BRANDS + ['Other']:
        selected = [s for s in sources if brand(s.get('url', '')) == company]
        checked = [by_url[s['url']] for s in selected if s.get('url') in by_url]
        successful = [r for r in checked if r.get('status') in ('first snapshot','changed','unchanged')]
        cached = [r for r in checked if r.get('status') == 'cached snapshot']
        deferred = [r for r in checked if r.get('status', '').startswith('deferred:')]
        failures = [r for r in checked if r.get('status', '').startswith('fetch failed')]
        counts[company] = {
            'candidate_urls':len(selected),
            'attempted':len(checked),
            'read_successfully':len(successful),
            'cached_snapshots':len(cached),
            'deferred':len(deferred),
            'failed':len(failures),
            'not_attempted':len(selected)-len(checked),
            'changed':sum(r.get('status')=='changed' for r in successful),
            'failed_examples':[{'name':r.get('name'),'url':r.get('url'),'status':r.get('status')} for r in (failures+deferred)[:12]],
        }
    revolt = load_json(REPORTS / 'revolut-discovery-status.json', {})
    competitor = load_json(REPORTS / 'competitor-source-catalog.json', {})
    discover_fail = len(revolt.get('failed_indexes', []))
    report = {
        'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),
        'monitor_run_at':last.get('checked_at'),
        'scope':'Revolut Crypto main app, UK; Revolut X is separate-product context',
        'discovery':{'revolut_failed_indexes':discover_fail,'revolut_newly_discovered':revolt.get('discovered'),
                     'competitor_catalog_generated':bool(competitor)},
        'companies':counts,
    }
    (REPORTS / 'source-coverage.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines = ['# Crypto intelligence — source coverage', '', f"Monitoring run: **{last.get('checked_at','unknown')}**", '',
        '> A successful GitHub workflow does not guarantee that all sources were readable. Candidate URLs are not verified coverage.', '',
        '| Company | Candidate URLs | Attempted | Fresh reads | Cached | Deferred | Failed | Changed |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for company in BRANDS+['Other']:
        c=counts[company]
        if company=='Other' and not c['candidate_urls']: continue
        lines.append(f"| {company} | {c['candidate_urls']} | {c['attempted']} | {c['read_successfully']} | {c['cached_snapshots']} | {c['deferred']} | {c['failed']} | {c['changed']} |")
    lines += ['', f'**Revolut category-index failures:** {discover_fail}', '',
       '## Interpretation', '',
       '- Fresh reads were fetched this run. Cached snapshots are prior successful reads and **not** fresh verification.',
       '- After a persistent Firecrawl 429, remaining pages may be deferred until the next run.',
       '- HTTP 403 is an access restriction. Do not circumvent it or describe a blocked page as analysed.',
       '- Product claims from unavailable sources require a separate, authorized manual review.',
       '- A changed page is only a text-change signal, not proof of a feature launch.',
       '- EU-only benchmarks (bunq/N26) are not direct substitutes for UK availability.',
       '- Revolut X belongs to an advanced trading journey, outside the primary crypto-curious scope.', '']
    for company in BRANDS:
        failed=counts[company]['failed_examples']
        if failed:
            lines += [f'## {company}: failed sources (up to 12)', '']
            for item in failed:
                lines.append(f"- [{item['name']}]({item['url']}): {item['status']}")
            lines.append('')
    (REPORTS/'source-coverage.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Coverage:', ' / '.join(f"{name} {counts[name]['read_successfully']}/{counts[name]['candidate_urls']}" for name in BRANDS))

if __name__=='__main__':
    main()
