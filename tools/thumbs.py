import json,sys,io,base64,urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'data','services.json')
dst=sys.argv[2] if len(sys.argv)>2 else os.path.join(ROOT,'data','thumbs.json')
d=json.load(open(src)); out={}
def go(s):
    try:
        b=urllib.request.urlopen(urllib.request.Request(s['image_url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((440,440))
        w,h=im.size; t=min(w,int(h*1.0)) 
        bio=io.BytesIO(); im.save(bio,'WEBP',quality=58)
        return s['id'],'data:image/webp;base64,'+base64.b64encode(bio.getvalue()).decode()
    except Exception as e:
        print('fail',s['id'],e); return s['id'],None
with ThreadPoolExecutor(8) as ex:
    for k,v in ex.map(go,d['services']):
        if v: out[k]=v
json.dump(out,open(dst,'w'))
print(len(out), sum(len(v) for v in out.values())//1024,'KB')
