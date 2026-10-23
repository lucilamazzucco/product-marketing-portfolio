#!/usr/bin/env python3
"""Discover official crypto information for PayPal UK, bunq EU, N26 EU.

Standard library only. Scoped link discovery; does not crawl entire sites.
Best effort: seed pages survive failed discovery. No bypassing access restrictions.
Run AFTER collect_revolut.py and BEFORE run.py.
"""
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
from urllib.request import Request, urlopen
import json
import re
import time

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / 'agent' / 'sources.json'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)

COMPANIES = {
 'PayPal': {
  'market':'United Kingdom — verify buying restrictions',
  'role':'Integrated-finance benchmark (UK)',
  'hosts':{'www.paypal.com','paypal.com','pep.paypal.com'},
  'seeds':[
   ('Positioning','https://www.paypal.com/uk/digital-wallet/manage-money/crypto'),
   ('Onboarding','https://www.paypal.com/uk/cshelp/article/how-do-i-buy-cryptocurrency-on-paypal-help567'),
   ('Capabilities','https://www.paypal.com/uk/cshelp/article/what-can-i-do-with-crypto-on-paypal-help893'),
   ('Fees','https://www.paypal.com/uk/webapps/mpp/digital-wallet/paypal-consumer-fees'),
   ('Availability','https://www.paypal.com/uk/cshelp/article/why-is-my-cryptocurrency-sale-on-hold%E2%80%AF-help886'),
   ('Risks','https://www.paypal.com/uk/cshelp/article/what-to-know-before-buying-crypto-help1292'),
   ('Education','https://www.paypal.com/uk/cshelp/article/paypals-guide-to-cryptocurrency-in-the-uk-help1293'),
   ('Terms','https://www.paypal.com/uk/legalhub/paypal/cryptocurrencies-tnc'),
   ('Price & protection','https://www.paypal.com/uk/cshelp/article/crypto-on-paypal-buying-and-purchase-protection-faqs-help573'),
  ],
 },
 'bunq': {
  'market':'Eligible European markets — not UK direct alternative',
  'role':'Integrated-banking benchmark (EU)',
  'hosts':{'help.bunq.com','www.bunq.com','bunq.com'},
  'seeds':[
   ('Overview','https://help.bunq.com/articles/bunq-crypto'),
   ('Features','https://help.bunq.com/articles/crypto-faq'),
   ('Fees','https://help.bunq.com/articles/how-do-the-fees-and-spread-work-in-bunq-crypto'),
   ('Staking','https://help.bunq.com/articles/crypto-staking'),
   ('Lifecycle','https://help.bunq.com/articles/never-miss-your-crypto-move'),
  ],
 },
 'N26': {
  'market':'Eligible European markets — not UK direct alternative',
  'role':'Integrated-banking benchmark (EU)',
  'hosts':{'support.n26.com','n26.com','www.n26.com'},
  'seeds':[
   ('Features / onboarding','https://support.n26.com/en-eu/app-and-features/app/how-n26-crypto-works'),
  ],
 }
}
CRYPTO = re.compile(r'crypto|cryptocurrenc|bitcoin|btc|ethereum|staking|digital.asset',re.I)
SKIP = re.compile(r'login|sign.?in|account/login|privacy|cookie|contact|jobs|careers|sitemap|facebook|instagram|twitter|linkedin|youtube', re.I)

class AnchorParser(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.href=None; self.text=[]
 def handle_starttag(self, tag, attrs):
  if tag=='a' and self.href is None: self.href=dict(attrs).get('href'); self.text=[]
 def handle_data(self, data):
  if self.href is not None: self.text.append(data)
 def handle_endtag(self, tag):
  if tag=='a' and self.href is not None:
   title=' '.join(' '.join(self.text).split())
   if self.href: self.links.append((title[:140],self.href))
   self.href=None; self.text=[]

def clean(url, hosts):
 p=urlsplit(url)
 if p.scheme!='https' or p.netloc.lower() not in hosts: return None
 if SKIP.search(p.path): return None
 # Preserve encoded path (including PayPal article URLs), discard tracking and fragments.
 return urlunsplit(('https',p.netloc.lower(),p.path.rstrip('/') or '/', '', ''))

def relevant(company, title, url):
 p=urlsplit(url).path
 if company=='PayPal' and not p.startswith('/uk/'): return False
 if company=='bunq' and p.startswith('/es-es/'): return False
 if company=='N26' and '/en-eu/' not in p and not p.startswith('/en-eu/'): return False
 return bool(CRYPTO.search(unquote(p)) or CRYPTO.search(title))

def fetch_links(url):
 req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; IndependentPMMResearch/1.0)','Accept':'text/html'})
 with urlopen(req,timeout=15) as resp:
  if 'html' not in resp.headers.get('Content-Type','').lower(): return []
  raw=resp.read(1_000_001)
  if len(raw)>1_000_000: raise ValueError('Page larger than 1MB')
  charset=resp.headers.get_content_charset() or 'utf-8'
  effective=resp.geturl()
 parser=AnchorParser(); parser.feed(raw.decode(charset,errors='replace'))
 return [(title,urljoin(effective,href)) for title,href in parser.links]

def theme(title,url):
 v=(title+' '+unquote(url)).lower()
 for name, terms in [('availability','available availability pause restrictions eligible country'),('fees','fee spread cost price pricing'),('onboarding','start buy purchase verification eligibility'),('risks','risk protection safe security safeguarding'),('lifecycle','alert notification recurring watchlist'),('staking','staking stake'),('terms','legal terms conditions')]:
  if any(term in v for term in terms.split()): return name
 return 'features-and-education'

def discover(company, cfg):
 entries={}; failed=[]
 def add(label,url,origin):
  normalized=clean(url,cfg['hosts'])
  if not normalized: return None
  if normalized not in entries:
   entries[normalized]={'title':label or 'Crypto information','url':normalized,'origin':origin,'theme':theme(label,normalized)}
  return normalized
 for label,url in cfg['seeds']: add(label,url,'curated official seed')
 # Crawl a small, controlled set of relevant source pages, up to two levels.
 # Link discovery is NOT a claim of comprehensive site coverage.
 queue=deque((url,0) for _,url in cfg['seeds']); seen=set()
 max_pages=12 if company=='PayPal' else 10
 max_sources=65 if company=='PayPal' else 45
 while queue and len(seen)<max_pages and len(entries)<max_sources:
  current, depth=queue.popleft()
  if current in seen: continue
  seen.add(current)
  try:
   candidates=fetch_links(current)
   for title,link in candidates:
    target=clean(link,cfg['hosts'])
    if not target or not relevant(company,title,target): continue
    if target not in entries and len(entries)>=max_sources: break
    add(title,target,'discovered link — verify relevance')
    if depth==0 and target not in seen: queue.append((target,1))
  except Exception as exc:
   failed.append({'url':current,'error':type(exc).__name__+': '+str(exc)[:100]})
  time.sleep(.20)
 return entries,failed

def main():
 sources=json.loads(CFG.read_text(encoding='utf-8'))
 # Keep Revolut pages and all unmatched prior sources.
 def belongs(item):
  host=urlsplit(item.get('url','')).netloc.lower()
  return any(host in cfg['hosts'] for cfg in COMPANIES.values())
 preserved=[s for s in sources if not belongs(s)]
 catalog={'collected_at':datetime.now(timezone.utc).isoformat(),'method':'curated official pages + scoped link discovery; discovery is not proof of accessible pages','companies':{}}
 merged=list(preserved)
 for name,cfg in COMPANIES.items():
  pages,failed=discover(name,cfg)
  catalog['companies'][name]={'market':cfg['market'],'pages':list(pages.values()),'failed_discovery_fetches':failed}
  for page in pages.values():
   merged.append({'name':name+' | '+page['title'],'market':cfg['market'],'role':cfg['role'],'theme':page['theme'],'url':page['url']})
  print(name, 'candidate pages:',len(pages),'discovery fetches failed:',len(failed))
 # Dedupe all companies by URL preserving first entry.
 merged=list({s['url']:s for s in reversed(merged)}.values())[::-1]
 CFG.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (REPORTS/'competitor-source-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# Competitor crypto research source catalog','',f"Collected: {catalog['collected_at']}",'','Sources are *candidates*, not confirmation they can all be fetched or are current. Links discovered on-page require human relevance review.','']
 for name,c in catalog['companies'].items():
  lines += [f"## {name} — {len(c['pages'])} candidate pages",'',f"Market: {c['market']}",'']
  for page in c['pages']: lines.append(f"- **{page['theme']}** · [{page['title'].replace('[','(').replace(']',')')}]({page['url']}) — {page['origin']}")
  if c['failed_discovery_fetches']: lines += ['',f"Discovery failures: {len(c['failed_discovery_fetches'])} (see JSON catalog)"]
  lines.append('')
 (REPORTS/'competitor-source-catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('Total configured sources:',len(merged))

if __name__=='__main__': main()
