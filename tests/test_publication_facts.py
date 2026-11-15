"""Regression tests for drift that must stop a publication or package build."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,subprocess,sys,tempfile,unittest,zipfile
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'base').is_dir():ROOT=ROOT/'base'
sys.path.insert(0,str(ROOT/'tools'))
import publication_facts as pf

class PublicationFacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='publication-regression-')
        cls.root=Path(cls.temp.name)/'fixture'
        shutil.copytree(ROOT,cls.root,ignore=shutil.ignore_patterns('.git','__pycache__','tests','_site'))
        cls.cfg=pf.configuration(cls.root);cls.mode=cls.cfg['mode']
        cls.original={p.relative_to(cls.root):p.read_bytes() for p in cls.root.rglob('*') if p.is_file()}
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def tearDown(self):
        for name,raw in self.original.items():
            p=self.root/name
            if not p.exists() or p.read_bytes()!=raw:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    def facts(self):return pf.read(self.root/self.cfg['facts'])
    def savefacts(self,d):(self.root/self.cfg['facts']).write_bytes(pf.encode(d))
    def primary(self):return self.root/('docs/WHITE_PAPER.md' if self.mode=='ra' else 'resume.html')
    def test_current_reviewed_publication_passes(self):
        self.assertEqual(pf.check(self.root,deep=True)['status'],'PASS')
    def test_render_is_idempotent_and_preserves_current_artifacts(self):
        before={n:pf.sha(self.root/n) for n in self.original}
        pf.render(self.root);pf.render(self.root)
        self.assertEqual(before,{n:pf.sha(self.root/n) for n in self.original})
    def test_stale_visible_count_is_rejected(self):
        p=self.primary();raw=p.read_bytes();self.assertIn(b'169-page',raw);p.write_bytes(raw.replace(b'169-page',b'136-page',1))
        with self.assertRaisesRegex(pf.PublicationError,'fact drift'):pf.check(self.root)
    def test_wrong_fact_type_is_rejected(self):
        d=self.facts();d['facts']['nwsw.report.pages']['value']='169';self.savefacts(d)
        with self.assertRaisesRegex(pf.PublicationError,'Wrong fact type'):pf.check(self.root)
    def test_impossible_observation_date_is_rejected(self):
        d=self.facts();d['facts']['nwsw.report.pages']['as_of']='2026-02-30';self.savefacts(d)
        with self.assertRaisesRegex(pf.PublicationError,'Invalid date'):pf.check(self.root)
    def test_primer_date_changes_all_bound_citations(self):
        d=self.facts();d['facts']['primer.date']['value']='2010-04';self.savefacts(d);pf.render(self.root)
        if self.mode=='ra':
            refs=pf.read(self.root/'docs/WHITE_PAPER_REFERENCES.json')['external_references'];ref=next(r for r in refs if r['id']=='16')
            self.assertIn('April',ref['venue']);self.assertEqual(ref['year'],'2010')
            with zipfile.ZipFile(self.root/'docs/WHITE_PAPER.docx') as z:
                doc=z.read('word/document.xml');self.assertIn(b'April. Hosted',doc);self.assertIn(b"CIA's 2010 Tradecraft Primer",doc)
        else:self.assertIn(b'April 2010',(self.root/'project-research-architect.html').read_bytes())
        with self.assertRaisesRegex(pf.PublicationError,'different facts'):pf.check(self.root)
    def test_inconsistent_grade_total_is_rejected(self):
        d=self.facts();d['facts']['nwsw.claim_review.total']['value']=131;self.savefacts(d)
        with self.assertRaisesRegex(pf.PublicationError,'do not sum'):pf.check(self.root)
    def test_unknown_binding_stops_render_before_any_output_write(self):
        cfg=pf.read(self.root/'publication/CONSUMERS.json');item=cfg['consumers'][0];key=next(iter(item['required']));p=self.root/item['template']
        p.write_bytes(p.read_bytes().replace(key.encode(),b'unknown.fact'));item['required']['unknown.fact']=item['required'].pop(key)
        (self.root/'publication/CONSUMERS.json').write_bytes(pf.encode(cfg));before=self.primary().read_bytes()
        with self.assertRaisesRegex(pf.PublicationError,'Unknown fact'):pf.render(self.root)
        self.assertEqual(before,self.primary().read_bytes())
    def test_removed_binding_is_rejected(self):
        item=self.cfg['consumers'][0];p=self.root/item['template'];text=p.read_text(encoding='utf-8');text=pf.TOKEN.sub('169',text,count=1);p.write_text(text,encoding='utf-8',newline='')
        with self.assertRaisesRegex(pf.PublicationError,'bindings removed'):pf.check(self.root)
    def test_path_escape_is_rejected_without_writing(self):
        cfg=pf.read(self.root/'publication/CONSUMERS.json');cfg['consumers'][0]['output']='../escaped.txt';(self.root/'publication/CONSUMERS.json').write_bytes(pf.encode(cfg))
        with self.assertRaisesRegex(pf.PublicationError,'escapes root'):pf.render(self.root)
        self.assertFalse((self.root.parent/'escaped.txt').exists())
    def test_canonical_snapshot_mismatch_is_rejected(self):
        other=Path(self.temp.name)/'other.json';d=self.facts();d['revision']='2026-11-15.2';other.write_bytes(pf.encode(d))
        with self.assertRaisesRegex(pf.PublicationError,'canonical facts'):pf.check(self.root,canonical_path=other)
    def test_fact_update_renders_but_old_artifacts_do_not_pass(self):
        old=self.primary().read_bytes();d=self.facts();d['facts']['nwsw.report.pages']['value']=170;d['facts']['nwsw.report.printed_last']['value']=168;self.savefacts(d);pf.render(self.root)
        self.assertIn(b'170-page',self.primary().read_bytes());self.assertNotEqual(old,self.primary().read_bytes())
        with self.assertRaisesRegex(pf.PublicationError,'different facts'):pf.check(self.root)
        if self.mode=='ra':
            # Dated evidence stays literal when current facts change.
            prior=next(b for b in old.decode().split('\n\n') if b.startswith('[E16] '))
            self.assertIn(prior,self.primary().read_text(encoding='utf-8'))
            with self.assertRaisesRegex(pf.PublicationError,'PDF is stale'):pf.check_pdf_text(self.root,self.facts(),self.cfg)
    def test_tampered_pdf_fails_its_bound_receipt(self):
        p=self.root/('docs/WHITE_PAPER.pdf' if self.mode=='ra' else 'assets/documents/research-architect-white-paper.pdf');p.write_bytes(p.read_bytes()+b'\nchanged')
        with self.assertRaisesRegex(pf.PublicationError,'artifact'):pf.check(self.root)
    def test_reference_copy_drift_is_rejected(self):
        p=self.root/('docs/WHITE_PAPER_REFERENCES.json' if self.mode=='ra' else 'docs/research-architect-white-paper.references.json');p.write_bytes(p.read_bytes().replace(b'U.S. Government',b'Wrong Author'))
        with self.assertRaises(pf.PublicationError):pf.check(self.root)
    def test_source_inventory_or_incomplete_import_is_rejected(self):
        if self.mode=='ra':
            p=self.root/'VERSION.json';d=pf.read(p);d['kit_runtime_version']='0.0.0';p.write_bytes(pf.encode(d))
            with self.assertRaisesRegex(pf.PublicationError,'differs from source'):pf.check(self.root)
        else:
            p=self.root/'publication/OWNER_DELIVERY.json';d=pf.read(p);d['files']={};p.write_bytes(pf.encode(d))
            with self.assertRaisesRegex(pf.PublicationError,'incomplete'):pf.check(self.root)
    def test_failed_validation_prevents_a_release_artifact(self):
        p=self.primary();p.write_bytes(p.read_bytes().replace(b'169-page',b'136-page',1))
        output=Path(self.temp.name)/'blocked-output'
        tool='build_pilot.py' if self.mode=='ra' else 'build_site.py'
        r=subprocess.run([sys.executable,'-B',str(self.root/'tools'/tool),'--output',str(output)],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0,r.stdout+r.stderr);self.assertFalse(output.exists())
    def test_resume_source_fingerprint_or_stale_figure(self):
        if self.mode=='portfolio':
            p=self.root/'resume.pdf';from pypdf import PdfReader,PdfWriter
            w=PdfWriter();w.clone_document_from_reader(PdfReader(p));w.add_metadata({'/Subject':'stale'});w.write(p)
            with self.assertRaisesRegex(pf.PublicationError,'Resume PDF is stale'):pf.check(self.root,deep=True)
        else:
            p=self.root/'docs/figures/figure-7-completed-case.png';p.write_bytes(p.read_bytes()+b'changed')
            with self.assertRaisesRegex(pf.PublicationError,'artifact'):pf.check(self.root)
    def test_portable_archive_rebuild_or_site_package(self):
        if self.mode=='portfolio':
            output=Path(self.temp.name)/'checked-site'
            r=subprocess.run([sys.executable,'-B',str(self.root/'tools/build_site.py'),'--output',str(output)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertEqual((output/'data/project-facts.json').read_bytes(),(self.root/'data/project-facts.json').read_bytes())
            self.assertTrue((output/'resume.pdf').is_file());self.assertFalse((output/'tools').exists());self.assertFalse((output/'publication').exists())
            return
        output=Path(self.temp.name)/'portable.zip'
        r=subprocess.run([sys.executable,'-B',str(self.root/'tools/build_pilot.py'),'--output',str(output)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        extracted=Path(self.temp.name)/'extracted'
        with zipfile.ZipFile(output) as z:
            self.assertIn('base/publication/FACTS.json',z.namelist());self.assertIn('base/tools/publication_facts.py',z.namelist());z.extractall(extracted)
        rebuilt=Path(self.temp.name)/'rebuilt.zip'
        r=subprocess.run([sys.executable,'-B',str(extracted/'base/tools/build_pilot.py'),'--output',str(rebuilt)],capture_output=True,text=True,cwd=extracted)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertEqual(pf.sha(output),pf.sha(rebuilt))
if __name__=='__main__':unittest.main()
