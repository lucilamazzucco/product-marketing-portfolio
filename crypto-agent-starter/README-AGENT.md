# Crypto Competitive Intelligence — Agent V1

A reproducible **public-source monitoring workflow** for an independent Product Marketing portfolio. It focuses on the main Revolut Crypto app and comparable integrated-finance products. Revolut X is out of scope except as contextual product discovery.

## What's real in V1

- GitHub Actions runs weekly (Monday 09:17 UTC) or manually.
- Fetches 4 official public help pages (Revolut UK, PayPal UK, bunq EU, N26 EU).
- Takes a dated text snapshot and compares changes with the previous successful read.
- Writes `reports/latest-brief.md` with source links, market labels, and status.
- Writes `reports/latest.json` for a future site dashboard.
- **Optional:** if you configure `OPENAI_API_KEY` as a GitHub Actions repository secret, the workflow calls an LLM to draft PMM research hypotheses. This is not enabled by default and incurs API costs.

## Important limitations

- A text change may just be a website update, not a product launch. **Human verification is required.**
- This is monitoring with an optional AI-analysis step; it is *not* an autonomous browsing agent or an AI chatbot.
- Some sites may block automated access; failures are reported instead of fabricating results.
- Public website copy is not internal product information, and UK/EU availability differs.
- Do not use a ChatGPT subscription as an API key. API access, if used, is a separate billed product.
- The public `snapshots.json` contains extracted text from official websites. Review rights/terms before publishing extensive extracts; for a public portfolio, you may prefer making the snapshot private and publishing only short citations and source links. The brief uses only excerpts when a source changes.

## Installation (from the ZIP)

1. Open your GitHub repository and choose **Add file → Upload files**.
2. Upload **the contents of the unzipped folder**, preserving paths `agent/run.py`, `agent/sources.json`, `.github/workflows/crypto-intelligence.yml` and `reports/`. **GitHub's web uploader can make nested folders tricky**. An easy alternative: use VS Code to copy the unpacked folders into a local cloned repository and commit/push; or manually create each path using **Add file → Create new file**, typing the path in the filename field. The `.github/workflows` folder is essential for the Actions tab.
3. Go to **Actions → Crypto Competitive Intelligence → Run workflow**.
4. After it finishes, open `reports/latest-brief.md`. First run is the baseline.
5. Future weekly runs will report changed or unchanged pages, without claiming product changes automatically.

## Optional AI upgrade

Under GitHub repository **Settings → Secrets and variables → Actions → New repository secret**, add `OPENAI_API_KEY` only when ready. **Never paste a key into HTML, JavaScript or a repository file.** The optional model is configurable via the workflow and may need adjustment for API account access.

## Future web integration

A later update to `index.html` can fetch `reports/latest.json` and render a read-only status dashboard, with links to the source-backed report. Avoid presenting drafts as established facts or verified outcomes.
