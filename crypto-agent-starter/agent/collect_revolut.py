#!/usr/bin/env python3
"""Discover UK Revolut Crypto help-center pages from category indexes.

Uses Python standard library. No scraping of logged-in pages or circumvention of blocks.
Run immediately before the existing agent/run.py workflow step.
"""
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from pathlib import Path
import datetime as dt
import json
import re
import time

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / 'agent' / 'sources.json'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)
BASE = 'https://help.revolut.com'
INDEXES = [
 ('Home / Crypto', '/help/crypto/'),
 ('Crypto staking', '/help/wealth/cryptocurrencies/crypto-staking/'),
 ('Crypto deposits', '/help/wealth/cryptocurrencies/transferring-cryptocurrencies/depositing-cryptocurrencies/'),
 ('Crypto withdrawals', '/help/wealth/cryptocurrencies/crypto-withdraw-deposit/'),
 ('Crypto trading', '/help/wealth/cryptocurrencies/crypto-overview/'),
 ('Revolut X', '/help/wealth/cryptocurrencies/crypto-exchange/'),
 ('Crypto safety', '/help/wealth/cryptocurrencies/understanding-revolut-cryptocurrency/crypto-safety/'),
 ('Revolut Ramp', '/help/wealth/revolut-ramp/'),
 ('More crypto features', '/help/wealth/cryptocurrencies/more-about-cryptocurrencies/'),
]
ALLOWED_PREFIXES = ('/help/wealth/cryptocurrencies/', '/help/wealth/revolut-ramp/', '/help/crypto/')
MAX_LINKS = 170

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.bits=[]; self.depth=0
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self.href is None:
            self.href=dict(attrs).get('href'); self.bits=[]; self.depth=1
        elif self.href is not None: self.depth+=1
    def handle_data(self, data):
        if self.href is not None: self.bits.append(data)
    def handle_endtag(self, tag):
        if self.href is not None:
            self.depth-=1
            if tag=='a' or self.depth<=0:
                title=' '.join(' '.join(self.bits).split())
                if self.href and title: self.links.append((title,self.href))
                self.href=None; self.bits=[]; self.depth=0

def canonical(href, origin=BASE):
    u=urlsplit(urljoin(origin,href))
    if u.scheme!='https' or u.netloc.lower()!='help.revolut.com': return None
    if not u.path.startswith(ALLOWED_PREFIXES): return None
    path=re.sub('/+', '/', u.path)
    if not path.endswith('/'): path+='/'
    return urlunsplit(('https','help.revolut.com',path,'',''))

def get_links(url):
    req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; PMMResearchPortfolio/1.0)', 'Accept':'text/html'})
    with urlopen(req,timeout=25) as r:
        if 'html' not in (r.headers.get('Content-Type','').lower()): raise ValueError('Not HTML')
        data=r.read(2_000_001)
        if len(data)>2_000_000: raise ValueError('HTML exceeds 2 MB limit')
        charset=r.headers.get_content_charset() or 'utf-8'
        origin=r.geturl()
    p=Links(); p.feed(data.decode(charset,errors='replace'))
    return [(name, u) for name, href in p.links if (u:=canonical(href,origin))]

def main():
    existing=json.loads(CFG.read_text(encoding='utf-8'))
    competitors=[s for s in existing if 'revolut.com' not in urlsplit(s.get('url','')).netloc]
    found={}; failed=[]
    for section, path in INDEXES:
        url=BASE+path
        found.setdefault(url,{'title':section,'section':section})
        try:
            links=get_links(url)
            for title, link in links:
                if len(found)>=MAX_LINKS: break
                found.setdefault(link,{'title':title[:180],'section':section})
            print(section, 'discovered',len(links),'links')
        except Exception as exc:
            failed.append({'section':section,'url':url,'error':type(exc).__name__+': '+str(exc)[:160]})
            print(section,'FAILED',type(exc).__name__)
        time.sleep(0.35)
    if not any(u not in {BASE+path for _,path in INDEXES} for u in found):
        print('No article links discovered; refusing to replace existing sources.')
        (REPORTS/'revolut-discovery-status.json').write_text(json.dumps({'failed_indexes':failed,'discovered':0},indent=2)+'\n')
        return
    source_list=[]
    for url, info in found.items():
        section=info['section']
        scope='separate-product-context' if section in ('Revolut X','Revolut Ramp') else 'main-app-or-support'
        source_list.append({'name':'Revolut / '+info['title'],'market':'United Kingdom','role':'Focus: main-app crypto' if scope=='main-app-or-support' else 'Context only: separate product','url':url})
    merged=source_list+competitors
    CFG.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    date=dt.datetime.now(dt.timezone.utc).isoformat()
    (REPORTS/'revolut-source-catalog.json').write_text(json.dumps({'discovered_at':date,'source_index':BASE+'/help/crypto/','total_revolut_urls':len(source_list),'failed_indexes':failed,'pages':[{'url':url,**info} for url,info in found.items()]},indent=2,ensure_ascii=False)+'\n')
    lines=['# Revolut Crypto — UK help centre source catalog','',f'Indexed: {date}',f'Discovered URLs: **{len(source_list)}**','', 'This is a discovery catalog, not proof every article was successfully fetched. Revolut X and Ramp are kept as separate-product context.','']
    bysection={}
    for url,info in found.items(): bysection.setdefault(info['section'],[]).append((info['title'],url))
    for section, entries in bysection.items():
        lines += ['## '+section,'']
        for name,url in entries: lines.append(f'- [{name.replace("[", "(").replace("]", ")")}]({url})')
        lines.append('')
    if failed:
        lines += ['## Index pages not fetched','']
        for x in failed: lines.append(f'- {x["section"]}: {x["error"]}')
    (REPORTS/'revolut-source-catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Total Revolut source URLs:',len(source_list),'Other competitors:',len(competitors))

if __name__=='__main__': main()
