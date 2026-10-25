"""Small company-only snapshots from the official French open API."""
import hashlib,json,re,urllib.parse,urllib.request
from datetime import datetime,timezone
BASE='https://recherche-entreprises.api.gouv.fr/search'
FIELDS=('siren','nom_complet','etat_administratif','activite_principale','nature_juridique')
def inputs(value):
 ids=value.get('sirens',[])
 if not isinstance(ids,list) or not 1<=len(ids)<=100:raise ValueError('Provide 1–100 SIRENs')
 if any(not isinstance(x,str) or not re.fullmatch(r'\d{9}',x) for x in ids):raise ValueError('SIRENs must be nine-digit strings')
 previous=value.get('previousHashes',{})
 if not isinstance(previous,dict) or any(not re.fullmatch(r'\d{9}',k) or not isinstance(v,str) or not re.fullmatch(r'[a-f0-9]{64}',v) for k,v in previous.items()):raise ValueError('Invalid previousHashes map')
 return list(dict.fromkeys(ids)),previous
def fetch(siren):
 query=urllib.parse.urlencode({'q':siren,'minimal':'true','per_page':1})
 request=urllib.request.Request(BASE+'?'+query,headers={'User-Agent':'FrixStudio company snapshot/0.1 (reda.frix.fr@gmail.com)','Accept':'application/json'})
 with urllib.request.urlopen(request,timeout=10) as response:
  raw=response.read(1_000_001)
  if len(raw)>1_000_000:raise ValueError('API response exceeds size limit')
  return json.loads(raw)
def snapshot(siren,previous=None,fetcher=fetch):
 now=datetime.now(timezone.utc).isoformat();base={'siren':siren,'checkedAt':now,'sourceUrl':BASE+'?'+urllib.parse.urlencode({'q':siren,'minimal':'true','per_page':1})}
 try:results=fetcher(siren).get('results',[])
 except Exception as e:return {**base,'status':'source_unavailable','error':type(e).__name__,'billable':False}
 record=next((r for r in results if r.get('siren')==siren),None)
 if not record:return {**base,'status':'not_found','billable':False}
 # Conservative legal-person scope: commercial companies (legal category 5), fully public.
 if not str(record.get('nature_juridique','')).startswith('5') or record.get('statut_diffusion')!='O':return {**base,'status':'excluded_non_company_or_non_public','billable':False}
 clean={key:record.get(key) for key in FIELDS}
 digest=hashlib.sha256(json.dumps(clean,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 return {**base,'status':'found','company':clean,'snapshotHash':digest,'changed':None if previous is None else digest!=previous,'billable':True}
