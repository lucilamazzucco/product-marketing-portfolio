# Crypto intelligence — source coverage

Monitoring run: **2026-10-26 09:58 UTC**

> A successful GitHub workflow does not guarantee that all sources were readable. Candidate URLs are not verified coverage.

| Company | Candidate URLs | Attempted | Fresh reads | Cached | Deferred | Failed | Changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Revolut | 14 | 14 | 10 | 0 | 3 | 1 | 2 |
| PayPal | 12 | 12 | 10 | 0 | 0 | 2 | 1 |
| bunq | 16 | 16 | 16 | 0 | 0 | 0 | 0 |
| N26 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| Coinbase | 4 | 4 | 0 | 0 | 0 | 4 | 0 |

**Revolut category-index failures:** 9

## Interpretation

- Fresh reads were fetched this run. Cached snapshots are prior successful reads and **not** fresh verification.
- After a persistent Firecrawl 429, remaining pages may be deferred until the next run.
- HTTP 403 is an access restriction. Do not circumvent it or describe a blocked page as analysed.
- Product claims from unavailable sources require a separate, authorized manual review.
- A changed page is only a text-change signal, not proof of a feature launch.
- EU-only benchmarks (bunq/N26) are not direct substitutes for UK availability.
- Revolut X belongs to an advanced trading journey, outside the primary crypto-curious scope.

## Revolut: failed sources (up to 12)

- [Revolut | Crypto staking](https://help.revolut.com/help/wealth/cryptocurrencies/crypto-staking/): fetch failed: Firecrawl HTTP 429
- [Revolut | Crypto legal terms](https://www.revolut.com/legal/cryptocurrency-terms/): deferred: Firecrawl HTTP 429
- [Revolut | Revolut X: separate advanced product](https://help.revolut.com/help/wealth/cryptocurrencies/crypto-exchange/): deferred: Firecrawl HTTP 429
- [Revolut | Crypto account onboarding requirements](https://help.revolut.com/help/wealth/cryptocurrencies/more-about-cryptocurrencies/cryptocurrencies-onboarding/what-does-the-new-crypto-onboarding-flow-consist-of/): deferred: Firecrawl HTTP 429

## PayPal: failed sources (up to 12)

- [PayPal | Terms](https://www.paypal.com/uk/legalhub/paypal/cryptocurrencies-tnc): fetch failed: ValueError
- [PayPal | Legal](https://www.paypal.com/uk/webapps/mpp/ua/cryptocurrencies-tnc): fetch failed: ValueError

## Coinbase: failed sources (up to 12)

- [Coinbase | UK positioning](https://help.coinbase.com/en-gb/coinbase/getting-started/getting-started-with-coinbase/what-is-coinbase): fetch failed: HTTPError
- [Coinbase | UK onboarding and FCA requirements](https://help.coinbase.com/en-gb/coinbase/getting-started/getting-started-with-coinbase/fca-financial-promo-changes): fetch failed: HTTPError
- [Coinbase | UK fees and spreads](https://help.coinbase.com/en-gb/coinbase/trading-and-funding/pricing-and-fees/fees): fetch failed: HTTPError
- [Coinbase | Account creation](https://help.coinbase.com/en-gb/coinbase/getting-started/getting-started-with-coinbase/create-a-coinbase-account): fetch failed: HTTPError
