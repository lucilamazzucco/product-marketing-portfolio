#!/usr/bin/env python3
"""Preserve a curated Revolut UK seed catalog if link discovery returns HTTP 403.

Only add candidate source URLs, never assert that they were fetched successfully.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / 'agent' / 'sources.json'
SEEDS = [
    ('Help centre: crypto home', 'discovery', 'https://help.revolut.com/help/crypto/'),
    ('Crypto account onboarding requirements', 'onboarding', 'https://help.revolut.com/help/wealth/cryptocurrencies/more-about-cryptocurrencies/cryptocurrencies-onboarding/what-does-the-new-crypto-onboarding-flow-consist-of/'),
    ('Crypto product overview', 'positioning', 'https://www.revolut.com/crypto/'),
    ('Buy crypto overview', 'positioning', 'https://www.revolut.com/crypto/buy-crypto/'),
    ('Crypto: getting started and trading', 'onboarding', 'https://help.revolut.com/help/wealth/cryptocurrencies/crypto-overview/'),
    ('Crypto features', 'features', 'https://help.revolut.com/help/wealth/cryptocurrencies/more-about-cryptocurrencies/'),
    ('Crypto trading fees', 'fees', 'https://help.revolut.com/help/wealth/cryptocurrencies/getting-cryptocurrency-exposure/how-much-does-it-cost-to-buy-or-sell-cryptocurrency/'),
    ('Crypto safety', 'risks', 'https://help.revolut.com/help/wealth/cryptocurrencies/understanding-revolut-cryptocurrency/crypto-safety/'),
    ('Crypto deposits', 'transfers', 'https://help.revolut.com/help/wealth/cryptocurrencies/transferring-cryptocurrencies/depositing-cryptocurrencies/'),
    ('Crypto withdrawals', 'transfers', 'https://help.revolut.com/help/wealth/cryptocurrencies/crypto-withdraw-deposit/'),
    ('Crypto staking', 'staking', 'https://help.revolut.com/help/wealth/cryptocurrencies/crypto-staking/'),
    ('Crypto legal terms', 'terms', 'https://www.revolut.com/legal/cryptocurrency-terms/'),
    ('Revolut X: separate advanced product', 'advanced-context', 'https://help.revolut.com/help/wealth/cryptocurrencies/crypto-exchange/'),
]

def main():
    sources = json.loads(CFG.read_text(encoding='utf-8'))
    by_url = {x['url']: x for x in sources}
    added = 0
    for title, theme, url in SEEDS:
        if url in by_url:
            continue
        entry = {
            'name': 'Revolut | ' + title,
            'url': url,
            'market': 'United Kingdom',
            'role': 'Context only: Revolut X' if theme == 'advanced-context' else 'Focus: Revolut Crypto main app',
            'theme': theme,
            'origin': 'curated candidate; availability and relevance unverified',
        }
        sources.append(entry)
        by_url[url] = entry
        added += 1
    CFG.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Preserved Revolut curated URLs: {len(SEEDS)}, newly added: {added}. Reachability is NOT implied.')

if __name__ == '__main__':
    main()
