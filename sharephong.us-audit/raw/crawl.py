import re,json,html,random,time,urllib.request,ssl,collections
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
s=open('sitemap.xml').read(); locs=re.findall(r'<loc>(.*?)</loc>',s)
groups=collections.defaultdict(list)
for u in locs:
    p=[x for x in u.replace('https://sharephong.us','').split('/') if x]
    groups[(p[0] if p else '')+('/'+p[1] if p and p[0]=='en' and len(p)>1 else '')+':'+str(len(p))].append(u)
random.seed(7); sample=[]
for k,v in groups.items(): sample+= v if len(v)<=20 else random.sample(v,max(20,len(v)//8))
extra=['https://sharephong.us/properties/does-not-exist-xyz','https://sharephong.us/search/san-jose','https://sharephong.us/about/','https://sharephong.us/search/not-a-city-xyz/']
sample+=extra
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
op=urllib.request.build_opener(NoRedir)
def get(u):
    t=time.time()
    try:
        r=op.open(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40); code=r.status; body=r.read().decode('utf-8','ignore'); hdr=dict(r.headers)
    except urllib.error.HTTPError as e:
        code=e.code; body=e.read().decode('utf-8','ignore'); hdr=dict(e.headers)
    except Exception as e: return {'url':u,'error':str(e)}
    dt=time.time()-t
    def f(p): return re.findall(p,body,re.I|re.S)
    txt=re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S); txt=html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',txt)))
    return {'url':u,'code':code,'loc':hdr.get('Location'),'t':round(dt,2),'size':len(body),
      'title':(f(r'<title[^>]*>(.*?)</title>') or [None])[0],
      'desc':(f(r'<meta name="description" content="([^"]*)"') or [None])[0],
      'canonical':f(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"'),
      'robots':f(r'<meta name="robots" content="([^"]*)"'),
      'hreflang':f(r'hreflang="([^"]*)"'),
      'lang':(f(r'<html[^>]*lang="([^"]*)"') or [None])[0],
      'h1':[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in f(r'<h1[^>]*>(.*?)</h1>')],
      'h2n':len(f(r'<h2[\s>]')),'jsonld':[x[:300] for x in f(r'application/ld\+json[^>]*>(.*?)</script>')],
      'imgs':len(f(r'<img ')),'img_noalt':len([i for i in f(r'<img[^>]*>') if not re.search(r'alt="[^"]+"',i)]),
      'words':len(txt.split()),'links':len(f(r'<a [^>]*href=')),'ogimg':(f(r'og:image" content="([^"]*)"') or [None])[0],
      'text':txt[:600]}
res=list(ThreadPoolExecutor(5).map(get,sample))
json.dump(res,open('crawl.json','w'),ensure_ascii=False,indent=1)
print(len(res))
