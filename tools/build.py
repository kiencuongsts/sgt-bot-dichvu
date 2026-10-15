import json,re,sys,html
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
d=json.load(open(ROOT+'data/services.json')); th=json.load(open(ROOT+'data/thumbs.json'))
def clean(h):
    if not h: return ''
    h=re.sub(r'\s(class|style|data-[\w-]+)="[^"]*"','',h)
    h=re.sub(r'<p>\s*</p>','',h); h=re.sub(r'</?span>','',h)
    h=re.sub(r'\s+',' ',h).strip()
    return h
def text(h):
    t=re.sub(r'<li>','\n- ',h or ''); t=re.sub(r'<(br|/p|/h\d|/li)[^>]*>','\n',t)
    t=html.unescape(re.sub(r'<[^>]+>','',t)); return re.sub(r'\n\s*\n+','\n',t).strip()
S=[];KB=[]
for s in d['services']:
    c=s['content']
    tt=[{'id':t['id'],'name':t['name'].strip(),'sd':t['short_description'],'days':t['duration_days'],'lead':t['booking_lead_time'],
         'exp':t['expiry_date'],'dates':t['available_dates'],
         'p':[{'id':p['id'],'name':re.sub(r'\s+',' ',p['name']).strip(),'sd':p['short_description'],'price':p['price'],'min':p['min_quantity'],'max':p['max_quantity']} for p in t['prices']]} for t in s['ticket_types']]
    S.append({'id':s['id'],'title':s['title'].strip(),'slug':s['slug'],'address':s['address'],'rating':s['rating'],'hl':s['highlight_label'],
      'dest':s['destinations'],'cat':[x['id'] for x in s['categories']],'price':s['price'],'orig':s['original_price'],'disc':s['has_discount'],
      'upd':s['updated_at'],'kw':(s['seo'] or {}).get('keywords') or '','gal':len(s.get('gallery') or []),
      'c':{k:clean(c.get(k)) for k in ['combo_content','promotion_policy','service_details','policy_terms','guide_info','cancellation_policy']},'tt':tt})
    KB.append({'id':s['id'],'title':s['title'].strip(),'url':'https://saigontourist.net/services/'+s['slug'],'destinations':s['destinations'],
      'categories':[x['name'] for x in s['categories']],'address':s['address'],'rating':s['rating'],'price_from':s['price'],'original_price':s['original_price'],
      'highlight_label':s['highlight_label'],'seo_keywords':(s['seo'] or {}).get('keywords'),
      'highlights':text(c.get('combo_content')),'promotion':text(c.get('promotion_policy')),'details':text(c.get('service_details')),
      'terms':text(c.get('policy_terms')),'guide':text(c.get('guide_info')),'cancellation':text(c.get('cancellation_policy')),
      'ticket_types':tt})
cats={int(o['value']):o['label'] for o in d['filters']['categories'] if o['group']}
used=set(x for s in S for x in s['dest'])
dests=[o for o in d['filters']['destinations'] if o['label'] in used]
meta={'fetched_at':d['fetched_at'],'cats':cats,'dests':dests,'price_ranges':d['filters']['price_ranges'],'source':'https://sandbox.saigontourist.me/channel/v1'}
blob='const META='+json.dumps(meta,ensure_ascii=False)+';\nconst SERVICES='+json.dumps(S,ensure_ascii=False,separators=(',',':'))+';\nconst THUMBS='+json.dumps({int(k):v for k,v in th.items()},separators=(',',':'))+';'
blob=blob.replace('</','<\\/')
tpl=open(ROOT+'src/template.html',encoding='utf-8').read()
out=tpl.replace('/*__DATA__*/',blob)
open(ROOT+'index.html','w',encoding='utf-8').write(out)
json.dump({'source':meta['source'],'fetched_at':meta['fetched_at'],'count':len(KB),'categories':list(cats.values()),'services':KB},open(ROOT+'services_kb.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out)//1024,'KB html')
