import json,os,sys,urllib.request,urllib.error,time
B=os.environ.get('SGT_API_BASE','https://sandbox.saigontourist.me')+'/channel/v1'
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','services.json')
def req(path,data=None,tok=None):
    h={'Accept':'application/json','Content-Type':'application/json'}
    if tok: h['Authorization']='Bearer '+tok
    r=urllib.request.Request(B+path,data=json.dumps(data).encode() if data else None,headers=h)
    for i in range(4):
        try:
            with urllib.request.urlopen(r,timeout=60) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2**i+1); continue
            print(path,e.code,e.read()[:300]); raise
t=req('/auth/token',{'client_id':os.environ['SGT_CLIENT_ID'],'client_secret':os.environ['SGT_CLIENT_SECRET']})
tok=t['access_token']; print('token ok',t.get('scopes'),t.get('environment'))
filters=req('/services/filters',tok=tok)['data']
items=[];p=1
while True:
    r=req(f'/services?per_page=100&page={p}',tok=tok); items+=r['data']
    print('page',p,r['meta'])
    if p>=r['meta']['last_page']: break
    p+=1
details=[]
for s in items:
    try: details.append(req(f"/services/{s['id']}",tok=tok)['data'])
    except Exception as e: print('fail',s['id'],e)
json.dump({'fetched_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'filters':filters,'services':details},open(out,'w'),ensure_ascii=False)
print('services',len(items),'details',len(details))
