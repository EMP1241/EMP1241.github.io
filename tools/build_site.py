"""Validate the publication, then prepare an allowlisted static Pages artifact."""
from pathlib import Path
import argparse,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def build(output):
    output=Path(output).resolve()
    if output.exists():raise ValueError('Refusing to overwrite an existing site artifact')
    if output==ROOT or ROOT.is_relative_to(output):raise ValueError('Output must not contain the source checkout')
    subprocess.run([sys.executable,'-B',str(ROOT/'tools/check_site.py')],check=True,cwd=ROOT)
    sources=[p for p in ROOT.iterdir() if p.is_file() and (p.suffix in {'.html','.css','.js'} or p.name in {'resume.pdf','README.md','CNAME','robots.txt','sitemap.xml'})]
    for name in ('assets','docs','data'):
        sources.extend(p for p in (ROOT/name).rglob('*') if p.is_file())
    for p in sources:
        if p.is_symlink() or not p.resolve().is_relative_to(ROOT):raise ValueError('Site source is outside the checkout: '+str(p))
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='publication-site-',dir=output.parent) as tmp:
        staging=Path(tmp)/'site';staging.mkdir()
        for p in sources:
            dest=staging/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        (staging/'.nojekyll').write_bytes(b'')
        os.rename(staging,output)
    print(f'PASS: validated static site, {len(sources)} files, {output}')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'_site');a=p.parse_args();build(a.output)
