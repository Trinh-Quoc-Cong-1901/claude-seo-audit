import re,json,html,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
urls=[l.strip() for l in open('urls.txt') if l.strip()]
urls=list(dict.fromkeys(urls))+['https://taichinh-thanglong.com/khong-ton-tai-xyz/','https://taichinh-thanglong.com/?s=chung+minh']
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
op=urllib.request.build_opener(NR)
def get(u):
    t=time.time()
    try: r=op.open(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40); code=r.status; b=r.read().decode('utf-8','ignore'); h=dict(r.headers)
    except urllib.error.HTTPError as e: code=e.code; b=e.read().decode('utf-8','ignore'); h=dict(e.headers)
    except Exception as e: return {'url':u,'error':str(e)}
    f=lambda p: re.findall(p,b,re.I|re.S)
    main=b
    txt=re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>','',b,flags=re.S|re.I)
    txt=html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',txt))).strip()
    imgs=f(r'<img\b[^>]*>')
    return {'url':u,'code':code,'loc':h.get('Location'),'t':round(time.time()-t,2),'size':len(b),
     'title':html.unescape((f(r'<title[^>]*>(.*?)</title>') or [''])[0]).strip(),
     'desc':html.unescape((f(r'<meta name="description" content="([^"]*)"') or [None])[0] or '') or None,
     'canonical':f(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)'),
     'robots':f(r'<meta name=["\']robots["\'] content=["\']([^"\']*)'),
     'h1':[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in f(r'<h1[^>]*>(.*?)</h1>')],
     'h2n':len(f(r'<h2[\s>]')),
     'jsonld_types':re.findall(r'"@type":"([^"]+)"',' '.join(f(r'<script type="application/ld\+json"[^>]*>(.*?)</script>'))),
     'words':len(txt.split()),'imgs':len(imgs),'noalt':sum(1 for i in imgs if not re.search(r'alt="[^"]+"',i)),
     'http_links':len(f(r'(?:href|src)="http://taichinh-thanglong\.com')),
     'og':bool(f(r'property="og:title"')),'lang':(f(r'<html[^>]*lang="([^"]*)"') or [None])[0]}
with ThreadPoolExecutor(8) as ex: res=list(ex.map(get,urls))
json.dump(res,open('crawl.json','w'),ensure_ascii=False,indent=1)
print(len(res))
