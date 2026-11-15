"""Render and verify RA/NWSW publication facts. No network access unless requested."""
from __future__ import annotations
import argparse,calendar,hashlib,html,json,os,re,subprocess,sys,tempfile,unicodedata,urllib.request,zipfile
from pathlib import Path
from datetime import date
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
TOKEN=re.compile(r'\{\{([a-z][a-z0-9_.]*)(?:\|([a-zA-Z0-9_]+))?\}\}')
AUTHORITY='https://raw.githubusercontent.com/EMP1241/EMP1241.github.io/main/data/project-facts.json'
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WORDS=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twenty-one']
TENS=['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
IMPORT_MAP={'docs/research-architect-white-paper.md':'docs/WHITE_PAPER.md','docs/research-architect-white-paper.references.json':'docs/WHITE_PAPER_REFERENCES.json','assets/documents/research-architect-white-paper.pdf':'docs/WHITE_PAPER.pdf','docs/figures/figure-7-completed-case.svg':'docs/figures/figure-7-completed-case.svg','docs/figures/figure-7-completed-case.png':'docs/figures/figure-7-completed-case.png'}

class PublicationError(ValueError):pass
def require(ok,message):
    if not ok:raise PublicationError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def sha(path):return digest(path.read_bytes())
def encode(obj):return (json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
def read(path):return json.loads(path.read_bytes())
def iso_date(value,label,month_only=False):
    require(isinstance(value,str) and bool(re.fullmatch(r'\d{4}-\d{2}'+('' if month_only else r'-\d{2}'),value)),'Invalid date: '+label)
    try:date.fromisoformat(value+('-01' if month_only else ''))
    except ValueError:raise PublicationError('Invalid date: '+label) from None
def within(root,name):
    require(isinstance(name,str) and name and not Path(name).is_absolute(),'Expected a relative publication path')
    path=(root/name).resolve();require(path.is_relative_to(root.resolve()),'Publication path escapes root: '+name)
    return path
def atomic(path,raw):
    if path.exists() and path.read_bytes()==raw:return
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(raw)
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
def configuration(root):
    cfg=read(root/'publication/CONSUMERS.json')
    require(cfg['schema_version']==1 and cfg['mode'] in ('ra','portfolio'),'Unsupported consumer configuration')
    return cfg
def catalog(raw):
    data=json.loads(raw);require(data.get('schema_version')==1,'Unsupported facts schema')
    require(data['authority']['url']==AUTHORITY,'Unexpected canonical facts authority')
    require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}\.\d+',data['revision'])),'Facts revision must be YYYY-MM-DD.N')
    for key,row in data['facts'].items():
        require(bool(re.fullmatch(r'[a-z][a-z0-9_.]*',key)),'Invalid fact key: '+key)
        kinds={'integer':int,'boolean':bool,'string':str};require(row['type'] in kinds and type(row['value']) is kinds[row['type']],'Wrong fact type: '+key)
        require(row['scope'] in ('current','historical','dated observation'),'Missing fact scope: '+key)
        iso_date(row['as_of'],key+' observation')
        require(row['source'] in data['sources'],'Missing source: '+key)
        if row['type']=='integer':require(row['value']>=0,'Negative count: '+key)
    v=lambda k:data['facts'][k]['value']
    require(sum(v('nwsw.claim_review.'+k) for k in ('establishes','suggests','consistent','does_not_show'))==v('nwsw.claim_review.total'),'Claim-review categories do not sum to total')
    require(v('nwsw.report.pages')==v('nwsw.report.printed_last')+2,'Assessment physical and printed pagination disagree')
    require(v('ra.inventory.local_texts')<=v('ra.inventory.sources'),'Local source count exceeds registry')
    require(v('nwsw.comparison.cutoff')<v('nwsw.comparison.start')<=v('nwsw.comparison.end'),'Comparison dates are out of order')
    return data
def value(data,key,fmt=None):
    require(key in data['facts'],'Unknown fact: '+key);v=data['facts'][key]['value']
    if fmt in ('words','Words'):
        require(type(v)==int and 0<=v<100,'Word formatter supports counts 0-99: '+key)
        out=WORDS[v] if v<20 else TENS[v//10]+(('-'+WORDS[v%10]) if v%10 else '')
        return out.capitalize() if fmt=='Words' else out
    if fmt in ('month','year','month_day','long','month_year'):
        iso_date(v,key,month_only=len(str(v))==7)
        parts=str(v).split('-');require(len(parts)>=2,'Expected an ISO date: '+key)
        year,month=int(parts[0]),int(parts[1]);name=calendar.month_name[month]
        if fmt=='month':return name
        if fmt=='year':return str(year)
        if fmt=='month_year':return f'{name} {year}'
        require(len(parts)==3,'Expected a complete date: '+key);day=int(parts[2])
        return f'{name} {day}'+(f', {year}' if fmt=='long' else '')
    if fmt=='comma':return f'{v:,}'
    if fmt=='rounded_thousand':return f'{round(v/1000)*1000:,}'
    if fmt=='nonlocal':return str(v-data['facts']['ra.inventory.local_texts']['value'])
    if fmt=='endash':return str(v).replace('-','–')
    if fmt=='curly':return str(v).replace("'",'’')
    if fmt=='automation':return 'automated' if v else 'not automated'
    if fmt=='retrospective':return 'retrospective' if v else 'prospective'
    require(fmt is None,'Unknown fact formatter: '+str(fmt))
    if type(v)==bool:return 'true' if v else 'false'
    return str(v)
def template(root,item,data):
    text=within(root,item['template']).read_bytes().decode('utf-8')
    counts={}
    for m in TOKEN.finditer(text):counts[m[1]]=counts.get(m[1],0)+1
    require(counts==item['required'],'Fact bindings removed or added without review: '+item['template'])
    def sub(m):
        out=value(data,m[1],m[2]);fmt=item.get('format','text')
        if fmt in ('html','xml'):return html.escape(out,quote=m[1].endswith('.url'))
        if fmt=='json':return json.dumps(out,ensure_ascii=False)[1:-1]
        return out
    result=TOKEN.sub(sub,text)
    require('{{' not in TOKEN.sub('',text).replace('{{ ',''),'Unrecognized template token in '+item['template'])
    if item.get('format')=='json':json.loads(result)
    if item.get('format')=='xml':ET.fromstring(result)
    return result.encode('utf-8')
def expectations(root,data,cfg):
    results=[];seen=set()
    for item in cfg['consumers']:
        ident=(item['output'],item.get('member'));require(ident not in seen,'Duplicate consumer target');seen.add(ident)
        results.append((item,template(root,item,data)))
    return results
def check_consumers(root,data,cfg):
    rows=expectations(root,data,cfg)
    for item,expected in rows:
        p=within(root,item['output']);require(p.is_file(),'Missing generated output: '+item['output'])
        if item.get('member'):
            with zipfile.ZipFile(p) as z:actual=z.read(item['member'])
        else:actual=p.read_bytes()
        require(actual==expected,'Publication fact drift: '+item['output']+((':'+item['member']) if item.get('member') else '')+'; render from the canonical facts, do not patch generated text')
    return len(rows)
def inventory(root):
    lib=root/'scientific_library';version=read(root/'VERSION.json');idx=read(lib/'knowledge/INDEX.json')['records']
    discovery=read(lib/'knowledge/safeguards/DISCOVERY.json')
    result={'ra.factory.version':version['version'],'ra.factory.status':version['status'].lower().replace('_',' '),'ra.factory.distribution_revision':version['distribution_revision'],'ra.runtime.version':version['kit_runtime_version'],'ra.library.revision':version['scientific_library_revision'],
      'ra.inventory.methods':len(read(lib/'method_modules/MODULE_REGISTRY.json')['modules']),
      'ra.inventory.sources':len(read(lib/'references/SOURCE_REGISTRY.json')['sources']),
      'ra.inventory.local_texts':len(list((lib/'references/open_texts').glob('*.md'))),
      'ra.inventory.appraisals':len(list((lib/'knowledge/reviews').glob('*.json'))),
      'ra.inventory.worked_designs':len(read(lib/'knowledge/DESIGN_CASES.json')['cases']),
      'ra.inventory.local_words':sum(len(p.read_text(encoding='utf-8').split()) for p in (lib/'references/open_texts').glob('*.md')),
      'ra.inventory.operational_cases':len(read(lib/'knowledge/cases/RA_OPERATIONS.json')['cases']),
      'ra.inventory.runnable_cases':len(list((lib/'knowledge/cases').glob('RC??_data.json')))}
    result.update({'ra.inventory.discovery_records':len(discovery['entries']),
      'ra.inventory.discovery_citation_rows':sum(len(r['provided_records']) for r in discovery['entries']),
      'ra.inventory.bias_controls':len(discovery['bias_control_options']),
      'ra.inventory.review_templates':len(list((lib/'knowledge/templates').glob('*.md'))),
      'ra.inventory.safeguard_guides':sum(r['id'].startswith(('specialist:SG','specialist:BI')) for r in idx)})
    for prefix,key in [('foundation','foundations'),('specialist','guides'),('domain','domain_guides')]:result['ra.inventory.'+key]=sum(r['id'].startswith(prefix+':') for r in idx)
    return result
def check_inventory(root,data):
    for key,actual in inventory(root).items():require(data['facts'][key]['value']==actual,'Published inventory differs from source: '+key)
    lib=root/'scientific_library'
    for n,pin in read(lib/'SOURCE_MANIFEST.json')['files'].items():require(sha(within(lib,n))==pin,'Scientific source manifest mismatch: '+n)
    for r in read(lib/'knowledge/INDEX.json')['records']:
        if r.get('path') and r.get('sha256'):require(sha(within(lib,r['path']))==r['sha256'],'Scientific index mismatch: '+r['id'])
def refresh_coverage_pins(root):
    lib=root/'scientific_library';p=lib/'knowledge/INDEX.json';raw=p.read_bytes();idx=json.loads(raw)
    for r in idx['records']:
        if r.get('path')=='knowledge/COVERAGE.md':r['sha256']=sha(lib/r['path'])
    out=encode(idx);atomic(p,out.replace(b'\n',b'\r\n') if b'\r\n' in raw else out)
    p=lib/'SOURCE_MANIFEST.json';raw=p.read_bytes();manifest=json.loads(raw)
    for n in ['knowledge/COVERAGE.md','knowledge/COVERAGE.json','knowledge/INDEX.json']:manifest['files'][n]=sha(lib/n)
    out=encode(manifest);atomic(p,out.replace(b'\n',b'\r\n') if b'\r\n' in raw else out)
def render(root,facts_path=None):
    cfg=configuration(root);fp=within(root,cfg['facts']);raw=Path(facts_path).read_bytes() if facts_path else fp.read_bytes();data=catalog(raw)
    rows=expectations(root,data,cfg) # Validate all templates before any write.
    docs={}
    for item,out in rows:
        path=within(root,item['output'])
        if item.get('member'):docs.setdefault(path,{})[item['member']]=out
    prepared={}
    for path,members in docs.items():
        import io
        with zipfile.ZipFile(path) as old:
            require(set(members)<=set(old.namelist()),'DOCX member is missing')
            if all(old.read(n)==b for n,b in members.items()):continue
            stream=io.BytesIO()
            with zipfile.ZipFile(stream,'w') as z:
                for info in old.infolist():z.writestr(info,members.get(info.filename,old.read(info.filename)))
            prepared[path]=stream.getvalue()
    atomic(fp,raw)
    for item,out in rows:
        if not item.get('member'):atomic(within(root,item['output']),out)
    for path,out in prepared.items():atomic(path,out)
    if cfg['mode']=='ra':refresh_coverage_pins(root)
    return {'rendered_consumers':len(rows),'revision':data['revision']}
def normalize(s):
    return re.sub(r'[^\w]','',unicodedata.normalize('NFKC',s)).lower()
def check_pdf_text(root,data,cfg):
    from pypdf import PdfReader
    pdf=PdfReader(root/'docs/WHITE_PAPER.pdf')
    text=' '.join(p.extract_text() or '' for p in pdf.pages)
    text=re.sub(r'Research Architect\s*\|\s*Technical white paper\s*\d+','',text)
    haystack=normalize(text);checked=0
    item=next(i for i in cfg['consumers'] if i.get('member')=='word/document.xml')
    source=ET.fromstring(within(root,item['template']).read_bytes());final=ET.fromstring(template(root,item,data))
    before=list(source.iter(W+'p'));after=list(final.iter(W+'p'));require(len(before)==len(after),'DOCX paragraph mismatch')
    for a,b in zip(before,after):
        original=''.join(n.text or '' for n in a.iter(W+'t'))
        if TOKEN.search(original):
            expected=''.join(n.text or '' for n in b.iter(W+'t'))
            require(normalize(expected) in haystack,'PDF is stale for fact-bearing paragraph: '+expected[:95]);checked+=1
    return {'pages':len(pdf.pages),'fact_paragraphs':checked}
def seal(root,note):
    cfg=configuration(root);require(cfg['mode']=='ra','Seal the paper in its RA owner checkout')
    require(bool(note.strip()),'Record the actual artifact review note')
    raw=within(root,cfg['facts']).read_bytes();data=catalog(raw);check_consumers(root,data,cfg);check_inventory(root,data)
    checked=check_pdf_text(root,data,cfg);path=root/'publication/ARTIFACTS.json';old=read(path) if path.exists() else None
    inputs={n:sha(root/n) for n in cfg['paper_inputs']};outputs={n:sha(root/n) for n in cfg['paper_outputs']}
    if old and inputs['docs/figures/figure-7-completed-case.svg']!=old['inputs']['docs/figures/figure-7-completed-case.svg']:
        require(outputs['docs/figures/figure-7-completed-case.png']!=old['outputs']['docs/figures/figure-7-completed-case.png'],'Figure 7 source changed but its bitmap did not; regenerate and review it before sealing')
    with zipfile.ZipFile(root/'docs/WHITE_PAPER.docx') as z:
        require(z.read('word/media/figure-7-completed-case.png')==(root/'docs/figures/figure-7-completed-case.png').read_bytes(),'DOCX contains an older Figure 7')
    report={'schema_version':1,'facts_sha256':digest(raw),'revision':data['revision'],'inputs':inputs,'outputs':outputs,'pdf_check':checked,'review_note':note}
    atomic(path,encode(report));return report
def check_seal(root,raw,cfg,deep=False):
    receipt=read(root/'publication/ARTIFACTS.json');require(receipt['facts_sha256']==digest(raw),'Paper receipt is bound to different facts; review and seal current artifacts')
    require(set(receipt['inputs'])==set(cfg['paper_inputs']) and set(receipt['outputs'])==set(cfg['paper_outputs']),'Artifact receipt coverage changed')
    for name,pin in {**receipt['inputs'],**receipt['outputs']}.items():require(sha(within(root,name))==pin,'Unreviewed or stale paper artifact: '+name)
    with zipfile.ZipFile(root/'docs/WHITE_PAPER.docx') as z:require(z.read('word/media/figure-7-completed-case.png')==(root/'docs/figures/figure-7-completed-case.png').read_bytes(),'Stale embedded case figure')
    if deep:require(check_pdf_text(root,catalog(raw),cfg)==receipt['pdf_check'],'Paper text/page verification differs from the sealed artifact')
    return receipt
def check_import(root,raw,deep=False):
    receipt=read(root/'publication/OWNER_DELIVERY.json');require(receipt['facts_sha256']==digest(raw),'Imported RA paper is bound to different facts; synchronize the owner delivery')
    require(set(receipt['files'])==set(IMPORT_MAP),'Imported artifact receipt is incomplete')
    for name,pin in receipt['files'].items():require(sha(within(root,name))==pin,'Imported RA artifact drift: '+name)
    require(receipt['engine_sha256']==sha(root/'tools/publication_facts.py'),'Publication checker differs from the owner delivery')
    doc=read(root/'docs/ra-white-paper-delivery.json')
    for key,n in {'pdf_sha256':'assets/documents/research-architect-white-paper.pdf','source_sha256':'docs/research-architect-white-paper.md','references_sha256':'docs/research-architect-white-paper.references.json'}.items():require(doc[key]==sha(root/n),'Paper receipt does not match '+n)
    if deep:
        from pypdf import PdfReader
        require(len(PdfReader(root/'assets/documents/research-architect-white-paper.pdf').pages)==doc['pages'],'Imported paper page count differs')
        require(PdfReader(root/'resume.pdf').metadata.subject=='resume.html SHA-256: '+sha(root/'resume.html'),'Resume PDF is stale; rebuild it from generated resume.html')
def check(root=ROOT,canonical_path=None,canonical_url=None,deep=False):
    root=Path(root).resolve();cfg=configuration(root);raw=within(root,cfg['facts']).read_bytes();data=catalog(raw)
    if canonical_path:require(raw==Path(canonical_path).read_bytes(),'RA snapshot differs from the canonical facts file')
    if canonical_url:
        require(canonical_url==AUTHORITY,'Only the declared public authority can be fetched')
        with urllib.request.urlopen(urllib.request.Request(AUTHORITY,headers={'Cache-Control':'no-cache'}),timeout=25) as r:remote=r.read(2_000_001)
        require(len(remote)<=2_000_000,'Canonical response exceeds limit');catalog(remote);require(raw==remote,'RA snapshot is behind the published canonical facts')
    count=check_consumers(root,data,cfg)
    if cfg['mode']=='ra':check_inventory(root,data);check_seal(root,raw,cfg,deep)
    else:check_import(root,raw,deep)
    return {'status':'PASS','mode':cfg['mode'],'revision':data['revision'],'facts':len(data['facts']),'consumers':count,'facts_sha256':digest(raw)}
def sync_portfolio(root,portfolio):
    root=Path(root).resolve();portfolio=Path(portfolio).resolve();cfg=configuration(root);pcfg=configuration(portfolio)
    require(cfg['mode']=='ra' and pcfg['mode']=='portfolio','Expected RA owner and portfolio roots')
    raw=within(root,cfg['facts']).read_bytes();canonical=within(portfolio,pcfg['facts']).read_bytes()
    require(raw==canonical,'RA snapshot differs from canonical portfolio facts; render RA with --facts first')
    check(root,deep=True);data=catalog(raw);expectations(portfolio,data,pcfg)
    files={dest:(root/src).read_bytes() for dest,src in IMPORT_MAP.items()}
    receipt=read(portfolio/'docs/ra-white-paper-delivery.json');sealed=read(root/'publication/ARTIFACTS.json')
    pins={**sealed['inputs'],**sealed['outputs']}
    require(all(digest(files[dest])==pins[src] for dest,src in IMPORT_MAP.items()),'Owner artifact changed during import; retry from a stable reviewed snapshot')
    if receipt['pdf_sha256']!=digest(files['assets/documents/research-architect-white-paper.pdf']):receipt['predecessor_pdf_sha256']=receipt['pdf_sha256']
    receipt.update(pages=sealed['pdf_check']['pages'],pdf_sha256=digest(files['assets/documents/research-architect-white-paper.pdf']),source_sha256=digest(files['docs/research-architect-white-paper.md']),references_sha256=digest(files['docs/research-architect-white-paper.references.json']),facts_revision=data['revision'],facts_sha256=digest(raw))
    engine=(root/'tools/publication_facts.py').read_bytes()
    delivery={'schema_version':1,'facts_sha256':digest(raw),'revision':data['revision'],'engine_sha256':digest(engine),'owner_docx_sha256':sha(root/'docs/WHITE_PAPER.docx'),'owner_receipt_sha256':sha(root/'publication/ARTIFACTS.json'),'files':{n:digest(b) for n,b in files.items()}}
    for n,b in files.items():atomic(within(portfolio,n),b)
    atomic(portfolio/'tools/publication_facts.py',engine);atomic(portfolio/'publication/OWNER_DELIVERY.json',encode(delivery));atomic(portfolio/'docs/ra-white-paper-delivery.json',encode(receipt))
    render(portfolio)
    from pypdf import PdfReader
    if PdfReader(portfolio/'resume.pdf').metadata.subject!='resume.html SHA-256: '+sha(portfolio/'resume.html'):
        fd,tmp=tempfile.mkstemp(suffix='.pdf',dir=portfolio);os.close(fd)
        try:
            subprocess.run([sys.executable,'-B',str(portfolio/'tools/build_resume.py'),'--output',tmp],check=True,cwd=portfolio)
            atomic(portfolio/'resume.pdf',Path(tmp).read_bytes())
        finally:Path(tmp).unlink(missing_ok=True)
    return check(portfolio,deep=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','render','seal','sync-portfolio','inventory']);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--facts',type=Path);p.add_argument('--canonical-url',action='store_true');p.add_argument('--deep',action='store_true');p.add_argument('--portfolio',type=Path);p.add_argument('--review-note')
    a=p.parse_args()
    try:
        if a.command=='check':r=check(a.root,a.facts,AUTHORITY if a.canonical_url else None,a.deep)
        elif a.command=='render':r=render(a.root,a.facts)
        elif a.command=='seal':r=seal(a.root,a.review_note or '')
        elif a.command=='inventory':r=inventory(a.root)
        else:require(a.portfolio is not None,'--portfolio is required');r=sync_portfolio(a.root,a.portfolio)
        print(json.dumps(r,indent=2))
    except (PublicationError,OSError,KeyError,json.JSONDecodeError,zipfile.BadZipFile) as e:p.exit(1,'Publication check failed: '+str(e)+'\n')
if __name__=='__main__':main()
