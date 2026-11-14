#!/usr/bin/env python3
"""Comprueba file:// real sin servidor ni cambios de políticas del navegador.

Salida 0: superada; 1: fallida; 2: bloqueada por una política administrativa.
python tests/check_file_catalogo.py --report /tmp/wan-file.json
"""
from pathlib import Path
import argparse,json,shutil,sys,tempfile,datetime,hashlib,subprocess
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path);args=parser.parse_args()
    result={'case':'FILE01','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expected':'HTML aislado en file://: 12 fichas, topología y CLI con puertos del catálogo, sin data/ ni Python','status':'fallida'}
    result['commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    result['application_sha256']=hashlib.sha256((ROOT/'WAN_v4.html').read_bytes()).hexdigest()
    errors=[];requests=[]
    with tempfile.TemporaryDirectory(prefix='wan-file-catalogo-') as directory, sync_playwright() as p:
        path=Path(directory)/'WAN_v4.html';shutil.copyfile(ROOT/'WAN_v4.html',path)
        bundled=Path(p.chromium.executable_path);executable=str(bundled) if bundled.is_file() else shutil.which('chromium')
        with p.chromium.launch(executable_path=executable,headless=True) as browser:
            result['browser']=browser.version;page=browser.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('request',lambda request:requests.append(request.url))
            try:
                page.goto(path.as_uri(),wait_until='load')
                assert page.evaluate('state.version===4&&interfaceCatalog.length===12')
                page.on('dialog',lambda dialog:dialog.accept())
                page.evaluate('demo();proposeVlans();confirmVlans();go(5);state.sites.forEach(s=>s.vendorProfile={router:"Cisco",core:"Cisco",distribution:"Cisco",access:"Cisco",firewall:"",backupRouter:""});buildTopology()')
                assert page.evaluate('''()=>{const n=state.nodes.find(n=>n.type==='Switch capa 3');setNodeModel(n.id,'cisco-c9200l-24t-4g');return generate(node(n.id),'Cisco').includes('GigabitEthernet1/')}''')
                assert not errors and not any(url.startswith(('http:','https:')) for url in requests)
                result.update(status='superada',actual='12 fichas en HTML aislado; plan/topología/CLI y nombres Catalyst correctos; cero solicitudes HTTP y errores JS.')
            except Exception as error:
                message=str(error)
                result.update(status='bloqueada' if 'ERR_BLOCKED_BY_ADMINISTRATOR' in message else 'fallida',actual=message[:700])
    if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return {'superada':0,'fallida':1,'bloqueada':2}[result['status']]
if __name__=='__main__':sys.exit(main())
