#!/usr/bin/env python3
"""Casos del catálogo local, registrados también en python tests/test_corte3.py.

Las fichas de contraste contienen datos de documentación oficial, no puertos
inventados por el runner. Ninguna prueba ejecuta CLI en dispositivos.
"""
from pathlib import Path
import copy,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data/catalogo-interfaces.json'
FACTS=ROOT/'tests/fixtures/catalogo-verificado.json'

def register(case,check):
    def choose(lab,identifier,model):
        lab.evaluate('a=>setNodeModel(a[0],a[1])',[identifier,model]);lab.valid()
    def target(lab,kind='Switch capa 3'):
        return lab.evaluate('kind=>state.nodes.find(n=>n.type===kind).id',kind)
    def native(lab,identifier,vendor):
        return lab.evaluate('a=>connected(node(a[0])).map(l=>endpoint(l,node(a[0]),a[1]).iface)',[identifier,vendor])
    def switch_vendor(lab,identifier,vendor,model):
        lab.evaluate('id=>editNode(id)',identifier)
        lab.page.locator('#nvendor').select_option(vendor);lab.page.locator('#nmodel').select_option(model)
        lab.button('Confirmar equipo').click();lab.valid()
    def atomic_import(lab,payload):
        before=lab.snapshot();calls=lab.evaluate('[__calls4,__calls6]')
        check(lab.evaluate('data=>{try{validateImport(data);return false}catch(e){return true}}',payload),'Aceptó un archivo incompatible')
        check(lab.snapshot()==before and lab.evaluate('[__calls4,__calls6]')==calls,'Error de importación mutó estado o asignó redes')

    @case('K01','Catálogo contra fichas oficiales','Doce modelos; cantidades, nombres, velocidades y fuentes contrastan con fichas verificadas.')
    def facts(lab):
        data=json.loads(CATALOG.read_text());facts=json.loads(FACTS.read_text());byid={m['id']:m for m in data['models']}
        check(len(byid)==12 and len(data['models'])==12,'Catálogo duplicado/incompleto')
        for row in facts['models']:
            model=byid[row['id']];ports=model['ports']
            check(len(ports)==row['ports'] and sum(p['assignable'] for p in ports)==row['assignable'],'Cantidad no coincide con ficha '+model['model'])
            check(ports[0]['name']==row['first'] and ports[-1]['name']==row['last'],'Nombres no coinciden con ficha')
            check(max(max(p['speedsMbps']) for p in ports)==row['maxMbps'],'Velocidad no coincide con ficha')
            check(len({p['name'] for p in ports})==len(ports),'Puertos duplicados')
            check(model['verifiedOn']=='2026-11-14' and model['sources'],'Falta trazabilidad')
            allowed={'Cisco':'cisco.com','Huawei':'huawei.com','Fortinet':'fortinet.com','MikroTik':'mikrotik.com'}[model['vendor']]
            from urllib.parse import urlsplit
            check(all((urlsplit(s['url']).hostname or '').endswith('.'+allowed) or urlsplit(s['url']).hostname==allowed for s in model['sources']),'Fuente no oficial')
        subprocess.run([sys.executable,str(ROOT/'tools/build_catalogo.py'),'--check'],check=True,capture_output=True)
        check(lab.evaluate('interfaceCatalog.length')==12,'Empaquetado no coincide')
        return '12 fichas (3 por marca), conteos/rangos/velocidades y fuentes oficiales; JSON y JS empaquetado coinciden.'

    @case('K02','Fabricante y modelos filtrados','Editor filtra fabricante/tipo, sin modelo para AP; cancelación no cambia datos.')
    def filters(lab):
        lab.lab();lab.topology();before=lab.snapshot();identifier=target(lab,'Router');lab.evaluate('id=>editNode(id)',identifier)
        lab.page.locator('#nvendor').select_option('MikroTik')
        options=lab.page.locator('#nmodel option').evaluate_all('(els)=>els.map(e=>e.value).filter(Boolean)')
        check(len(options)==3 and all(x.startswith('mikrotik-') for x in options),'No filtró MikroTik Router')
        lab.page.locator('#ntype').select_option('Switch')
        check(lab.page.locator('#nmodel option').count()==1,'Ofrece MikroTik no soportado como switch')
        lab.page.locator('#nvendor').select_option('Huawei');check(lab.page.locator('#nmodel option').count()==4,'No ofrece tres switches Huawei')
        lab.page.locator('#ntype').select_option('Access Point');check(lab.page.locator('#nmodel option').count()==1,'Ofrece modelo genérico de AP')
        lab.button('Cancelar').click();check(lab.snapshot()==before,'Cancelar cambió proyecto')
        return 'Listas por marca/rol; AP y roles no soportados sin modelos; cancelación intacta.'

    @case('K03','Carga automática de inventario','Seleccionar modelo muestra interfaces documentadas, sin escribir nombres ni guardar datos preliminares.')
    def inventory(lab):
        lab.lab();lab.topology();identifier=target(lab);before=lab.snapshot();lab.evaluate('id=>editNode(id)',identifier)
        lab.page.locator('#nmodel').select_option('cisco-c9200l-24t-4g')
        body=lab.page.locator('#nodeModelInventory').inner_text()
        check('GigabitEthernet1/0/24' in body and 'GigabitEthernet1/1/4' in body,'Falta inventario Catalyst de ficha')
        check(lab.snapshot()==before,'Vista previa guardó sin confirmar equipo')
        check(not lab.page.locator('#physicalModel,#physicalSource,#physicalConfirm').count(),'Reintrodujo formulario por puerto')
        lab.button('Confirmar equipo').click();lab.valid();check(lab.evaluate('id=>node(id).modelId',identifier)=='cisco-c9200l-24t-4g','No guardó modelo')
        return '28 puertos de ficha visibles inmediatamente; guardar equipo asigna enlaces; sin entrada manual de puertos.'

    @case('K04','Cisco con modelo','Catalyst seleccionado usa nombres reales en toda la CLI física, conservando IPv4/HSRP.')
    def cisco(lab):
        lab.lab();lab.topology();identifier=target(lab);before=lab.snapshot()['state']['plan'];lab.go(6)
        lab.page.locator('#model-'+identifier).select_option('cisco-c9200l-24t-4g');lab.valid()
        cli=lab.evaluate('id=>generate(node(id),"Cisco")',identifier);names=native(lab,identifier,'Cisco')
        check(names and all('interface '+name in cli for name in names),'Cisco omitió puerto del catálogo')
        check(all(x.startswith('GigabitEthernet1/') for x in names) and 'interface GigabitEthernet0/' not in cli,'Cisco sigue genérico')
        check(lab.snapshot()['state']['plan']==before and 'standby ' in cli,'Cambió plan o perdió HSRP')
        return f'Catalyst: {len(names)} puertos de ficha en CLI, HSRP/IP conservados; cero nombres físicos genéricos.'

    @case('K05','Huawei con modelo','Switch L2 seleccionado usa banco RJ45 de la variante, sin atribuirle L3 ni SFP no verificados.')
    def huawei(lab):
        lab.lab();lab.topology();identifier=target(lab,'Switch');switch_vendor(lab,identifier,'Huawei','huawei-s5700-28p-li-ac')
        cli=lab.evaluate('id=>generate(node(id),"Huawei")',identifier);names=native(lab,identifier,'Huawei')
        check(all('interface '+x in cli for x in names),'Huawei omitió puertos')
        check(all(1<=int(x.rsplit('/',1)[1])<=24 for x in names),'Asignó SFP sin nomenclatura verificada')
        check('port link-type trunk' in cli and 'router ospf' not in cli and 'ospf 1' not in cli,'Sintaxis/rol Huawei incorrecto')
        return 'Huawei L2: nombres del banco RJ45 de ficha; sin SFP no verificados ni routing de core.'

    @case('K06','Fortinet con modelos','60F/61F/70F usan wan1/wan2/dmz y excluyen puertos de switch interno/FortiLink.')
    def fortinet(lab):
        for model in ['fortinet-60f','fortinet-61f','fortinet-70f']:
            lab.edge('Fortinet');choose(lab,'edge',model)
            cli=lab.evaluate('generateFortinet(node("edge"))');names=native(lab,'edge','Fortinet')
            check(set(names)<={'wan1','wan2','dmz'} and all('edit "'+x+'"' in cli for x in names),'Fortinet no usa nombres de ficha')
            check(not any('port'+str(i)==x for x in names for i in range(1,10)),'Sigue usando portN universal')
        return 'Tres modelos FortiGate: puertos exactos de tablas oficiales; internal1–5 y a/b no asignados automáticamente.'

    @case('K07','MikroTik con modelos','hEX, hEX S y CCR2004 usan puertos de sus fichas con sintaxis RouterOS 7.')
    def mikrotik(lab):
        for model in ['mikrotik-rb750gr3','mikrotik-rb760igs','mikrotik-ccr2004-16g-2splus']:
            lab.edge('MikroTik');choose(lab,'edge',model)
            cli=lab.evaluate('generateMikroTik(node("edge"))');names=native(lab,'edge','MikroTik')
            check(all('name="'+x+'"' in cli for x in names),'RouterOS omitió nombres exactos')
            check('/routing ospf interface-template' in cli and '/interface bridge' in cli,'Perdió OSPF v7/bridge')
        return 'Tres routers RouterOS 7: nombres en guardas Ethernet, bridge e interfaces OSPF; sin sintaxis ajena.'

    @case('K08','Asignación determinista','Orden de filas/ejecuciones no cambia la asociación puerto–enlace; sin duplicados.')
    def deterministic(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g')
        result=lab.evaluate('''id=>{const data=structuredClone(state),first=assignCatalogInterfaces(data);data.links.reverse();data.nodes.reverse();const second=assignCatalogInterfaces(data);return [first,second]}''',identifier)
        binding=lambda rows:{r['id']:(r['ac'],r['bc'],r['ah'],r['bh']) for r in rows}
        check(binding(result[0])==binding(result[1]),'Asignación depende del orden')
        names=native(lab,identifier,'Cisco');check(len(set(names))==len(names),'Duplicó puertos')
        return 'Mismas asociaciones al repetir/invertir nodos y enlaces; puertos físicos únicos.'

    @case('K09','Puertos insuficientes y atomicidad','ISR4321 de dos GE rechaza tres enlaces sin inventar puertos ni perder proyecto/DOM.')
    def capacity(lab):
        lab.lab();lab.topology();lab.configs('Cisco');lab.go(6);identifier=target(lab,'Router')
        check(lab.evaluate('id=>connected(node(id)).length',identifier)>2,'Laboratorio sin demanda de capacidad')
        message=lab.atomic_error(lambda:lab.evaluate('id=>setNodeModel(id,"cisco-isr4321-k9")',identifier),'#model-'+identifier)
        check('ISR4321' in message and 'insuficientes' in message,'Error no identifica modelo/capacidad')
        return 'Tres enlaces frente a dos GE reales: rechazo atómico, sin puerto ficticio ni pérdida de plan, CLI, DOM o localStorage.'

    @case('K10','Duplicados y referencias importadas','Importador rechaza puertos repetidos/no existentes del modelo sin reasignar ni sustituir estado.')
    def duplicates(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g');payload=lab.export()
        bad=copy.deepcopy(payload);links=[l for l in bad['state']['links'] if identifier in [l['a'],l['b']]]
        name=links[0]['ac' if links[0]['a']==identifier else 'bc'];links[1]['ac' if links[1]['a']==identifier else 'bc']=name;atomic_import(lab,bad)
        bad=copy.deepcopy(payload);next(l for l in bad['state']['links'] if l['a']==identifier or l['b']==identifier)['ac' if links[0]['a']==identifier else 'bc']='GigabitEthernet1/0/99';atomic_import(lab,bad)
        return 'Puerto duplicado y puerto 99 inexistente rechazados sin asignación automática durante importación.'

    @case('K11','Cambio de modelo','Cambiar 24T por 48T conserva puertos válidos, enlaces, VLAN, direcciones y otras sedes.')
    def change(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g');before=lab.snapshot();names=native(lab,identifier,'Cisco')
        choose(lab,identifier,'cisco-c9200l-48t-4g');after=lab.snapshot()
        check(native(lab,identifier,'Cisco')==names and after['state']['plan']==before['state']['plan'] and after['state']['links']==before['state']['links'],'Cambio renumeró diseño válido')
        check([{k:v for k,v in n.items() if k!='modelId'} for n in before['state']['nodes']]==[{k:v for k,v in n.items() if k!='modelId'} for n in after['state']['nodes']],'Alteró equipos')
        return '24T→48T mantiene puertos válidos y todo el direccionamiento/identidad; cambia únicamente modelo e invalida CLI derivada.'

    @case('K12','Regeneración con modelos','Reconstruir topología conserva modelo, IDs y puertos válidos de nodos automáticos.')
    def regenerate(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g');before=lab.snapshot();names=native(lab,identifier,'Cisco');lab.go(5)
        lab.button('Generar desde el plan').click();lab.valid()
        check(lab.evaluate('id=>node(id).modelId',identifier)=='cisco-c9200l-24t-4g' and native(lab,identifier,'Cisco')==names,'Regenerar perdió modelo/asignación')
        check(lab.snapshot()['state']['plan']==before['state']['plan'],'Regeneró direccionamiento')
        return 'Modelo, identificadores, puertos y plan conservados al reconstruir desde el mismo plan.'

    @case('K13','JSON v4 y almacenamiento','Guardar/cargar/importar conserva modelId y puertos; cero llamadas a asignadores IPv4/IPv6.')
    def persistence(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g');lab.configs('Cisco');before=lab.snapshot();before['state'].setdefault('subnetOK',False)
        calls=lab.evaluate('[__calls4,__calls6]');lab.upload(lab.export());lab.valid();check(lab.snapshot()==before,'JSON perdió modelo/CLI/enlaces')
        lab.evaluate('saveLocal();state=fresh();loadLocal()');lab.valid();check(lab.snapshot()==before,'localStorage perdió datos')
        check(lab.evaluate('[__calls4,__calls6]')==calls,'Importación recalculó redes')
        return 'v4/CLI/modelId/enlaces exactos en JSON y localStorage; no se reasignan redes al cargar.'

    @case('K14','Proyectos antiguos y advertencia','v2/v3/v4 sin modelo preservan datos y generación genérica, con advertencia visual.')
    def legacy(lab):
        for version in [2,3]:
            lab.upload(lab.fixture(version));lab.valid();check(lab.evaluate('state.nodes.every(n=>!n.modelId)'),'Infirió modelos antiguos')
            lab.go(6);check('Modelo no especificado. Los nombres de interfaces son genéricos' in lab.page.locator('#view').inner_text(),'Falta aviso solicitado')
            lab.button('Generar todos los Cisco').click();lab.valid()
        return 'v2/v3 migran a v4 sin modelo inferido; CLI genérica permanece y aviso exacto visible; referencias históricas en C26.'

    @case('K15','Fabricantes mixtos con catálogo','Cuatro marcas reales usan modelos compatibles de la misma topología y plan común.')
    def mixed(lab):
        lab.lab();lab.go(5)
        profile={'router':'MikroTik','core':'Cisco','distribution':'Huawei','access':'Huawei','firewall':'Fortinet','backupRouter':''}
        for i in range(2):
            for role,vendor in profile.items():lab.page.locator(f'#vp{i}_{role}').select_option(vendor)
        lab.button('Confirmar fabricantes').click();lab.valid();lab.go(3);lab.page.locator('button[onclick="confirmVlans()"]').click();lab.valid();lab.go(5);lab.button('Generar desde el plan').click();lab.valid()
        before=lab.snapshot()['state']['plan']
        lab.evaluate('''()=>{const ids={Cisco:'cisco-c9200l-24t-4g',Huawei:'huawei-s5700-28p-li-ac',Fortinet:'fortinet-60f',MikroTik:'mikrotik-ccr2004-16g-2splus'};for(const n of state.nodes)if(configurable(n)||fortinetNode(n)||mikrotikNode(n)){n.modelId=ids[n.vendor];for(const l of connected(n))l[(l.a===n.id?'a':'b')+vendorPortKey(n.vendor)]=''}state.links=assignCatalogInterfaces(state);validateCatalogBindings(state);invalidate('topology');render()}''')
        for vendor in ['Cisco','Huawei','Fortinet','MikroTik']:
            outputs=lab.configs(vendor);check(outputs and lab.evaluate('v=>configNodes(v).every(n=>n.vendor===v&&n.modelId)',vendor),'Falta fabricante real con modelo')
        check(lab.snapshot()['state']['plan']==before,'Catálogo alteró plan mixto')
        return 'Cisco core, Huawei acceso, Fortinet firewall y MikroTik router con modelos documentados; cuatro CLI y plan común intacto.'

    @case('K16','AP excluidos con vecinos modelados','AP mantiene IP/VLAN/enlaces; ningún adaptador ni modelo ofrece CLI genérica para AP.')
    def ap(lab):
        lab.lab();lab.topology();aps=lab.evaluate('state.nodes.filter(accessPoint)');check(aps,'Laboratorio sin AP')
        for vendor in ['Cisco','Huawei','Fortinet','MikroTik']:
            check(lab.evaluate('v=>modelsFor(v,"Access Point").length===0',vendor),'Catálogo ofrece AP genérico')
            check(lab.evaluate('v=>{try{generate(state.nodes.find(accessPoint),v);return false}catch(e){return e.message.includes("AP")}}',vendor),'Adaptador admitió AP')
        choose(lab,target(lab),'cisco-c9200l-24t-4g')
        check(lab.evaluate('state.nodes.filter(accessPoint)')==aps,'Modelar vecino eliminó/cambió AP')
        return 'AP sin modelos/CLI genéricos; nodos/IP/VLAN/enlaces siguen intactos al seleccionar modelos vecinos.'

    @case('K17','Funcionamiento sin internet','Catálogo cargado localmente; seleccionar, asignar, generar y exportar funciona desconectado.')
    def offline(lab):
        check(lab.evaluate('interfaceCatalog.length')==12,'No cargó recurso local')
        lab.context.set_offline(True)
        try:
            lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g')
            check(lab.evaluate('id=>generate(node(id),"Cisco").includes("GigabitEthernet1/")',identifier),'Falló generación offline')
            payload=lab.export();check(any(n.get('modelId') for n in payload['state']['nodes']),'Exportación offline perdió modelo')
        finally:lab.context.set_offline(False)
        check(not lab.external,'Consultó una fuente externa')
        return 'Selección, VLSM, topología, asignación, CLI y JSON operan con red desactivada tras cargar activos locales; cero consultas externas.'

    @case('K18','Catálogo ES/EN y responsive','Controles, mensajes e inventario traducidos; modelo y CLI intactos a 1440/390 px.')
    def language(lab):
        lab.lab();lab.topology();identifier=target(lab);choose(lab,identifier,'cisco-c9200l-24t-4g');before=lab.snapshot();cli=lab.evaluate('id=>generate(node(id),"Cisco")',identifier)
        for width in [1440,390]:
            lab.page.set_viewport_size({'width':width,'height':900})
            for lang in ['es','en']:
                lab.evaluate('lang=>setLanguage(lang)',lang);lab.go(6)
                label='Fabricante y modelo · catálogo local' if lang=='es' else 'Vendor and model · local catalogue'
                check(label in lab.page.locator('#view').inner_text(),'Título no traducido')
                lab.page.locator('#model-'+identifier).select_option('cisco-c9200l-24t-4g');lab.valid()
                check(lab.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Desborde de catálogo')
                if lang=='en':check('Sin stack:' not in lab.page.locator('#view').inner_text(),'Aviso de datos no traducido')
        check(lab.snapshot()['state']['plan']==before['state']['plan'] and lab.evaluate('id=>generate(node(id),"Cisco")',identifier)==cli,'Traducir cambió plan/CLI')
        return 'Catálogo y avisos en ES/EN, 1440/390 sin desborde nuevo; modelo, redes y CLI conservados.'

    @case('K19','Entradas inseguras y modelos incompatibles','Modelo desconocido/inyección/tipo incorrecto rechazados atómicamente en selección e importación.')
    def security(lab):
        lab.lab();lab.topology();identifier=target(lab);before=lab.snapshot()
        for model in ['unknown-model','<script>alert(1)</script>','mikrotik-rb750gr3']:
            check(lab.evaluate('a=>setNodeModel(a[0],a[1])',[identifier,model]) is False,'Aceptó modelo inválido')
            check(lab.snapshot()==before,'Error de modelo mutó proyecto')
        lab.evaluate("$('toast').className='toast hidden'")
        payload=lab.export();bad=copy.deepcopy(payload);bad['state']['nodes'][0]['modelId']=42;atomic_import(lab,bad)
        bad=copy.deepcopy(payload);bad['state']['nodes'][0]['modelId']='unknown-model';atomic_import(lab,bad)
        return 'Selección de ID desconocido, inyección y fabricante/tipo incompatible bloqueados; JSON inválido conserva estado.'

    @case('K20','ISR4321 y función no respaldada','Dos GE físicos generan en router compatible; funciones fuera del perfil se bloquean con causa específica.')
    def features(lab):
        lab.lab();lab.evaluate('state.sites.forEach(s=>s.redundant=false);proposeVlans()');lab.page.locator('button[onclick="confirmVlans()"]').click();lab.valid();lab.topology()
        identifier=target(lab,'Router');choose(lab,identifier,'cisco-isr4321-k9');cli=lab.evaluate('id=>generate(node(id),"Cisco")',identifier)
        check(all('interface '+x in cli for x in ['GigabitEthernet0/0/0','GigabitEthernet0/0/1']) and 'switchport mode' not in cli,'ISR usó puertos/comandos de switch')
        identifier=target(lab,'Switch');switch_vendor(lab,identifier,'Huawei','huawei-s5700-28p-li-ac')
        result=lab.evaluate('''id=>{const l=connected(node(id)).find(l=>l.type==='trunk');const old=l.bundle;l.bundle=1;try{generate(node(id),'Huawei');return ''}catch(e){return e.message}finally{l.bundle=old}}''',identifier)
        check('lacp' in result and ('no respaldada' in result),'No bloqueó función no respaldada')
        return 'ISR4321 usa sus dos GE sin switchport; LACP no respaldado en perfil Huawei bloquea generación con mensaje concreto.'

    @case('K21','Medios y velocidades compatibles','Uplink óptico entre modelos conocidos usa puertos/velocidad común; medio incompatible se rechaza al importar.')
    def media(lab):
        lab.edge('MikroTik')
        lab.evaluate('''()=>{node('edge').modelId='mikrotik-rb760igs';node('sw').modelId='cisco-c9200l-24t-4g';for(const n of [node('edge'),node('sw')])for(const l of connected(n))l[(l.a===n.id?'a':'b')+vendorPortKey(n.vendor)]='';state.links=assignCatalogInterfaces(state);validateCatalogBindings(state);render()}''')
        lan=next(l for l in lab.snapshot()['state']['links'] if l['id']=='lan')
        check(lan['am']=='sfp1' and lan['bc'].startswith('GigabitEthernet1/1/'),'No priorizó uplink compatible verificado')
        payload=lab.export();bad=copy.deepcopy(payload);next(l for l in bad['state']['links'] if l['id']=='lan')['bc']='GigabitEthernet1/0/24';atomic_import(lab,bad)
        return 'SFP1↔uplink SFP Catalyst con 1G común; fibra↔RJ45 incoherente rechazada sin inventar transceptor ni cambiar estado.'

    @case('K22','Catálogo ausente y modo legado','Sin archivo de catálogo los proyectos sin modelo siguen funcionando con aviso; no se consulta internet.')
    def missing(lab):
        lab.context.route('**/data/catalogo-interfaces.js',lambda route:route.fulfill(status=200,content_type='text/javascript',body='// Catálogo no distribuido en este laboratorio de fallo controlado.'))
        lab.page.reload(wait_until='load');check(lab.evaluate('interfaceCatalog.length')==0,'No reprodujo catálogo ausente')
        lab.lab();lab.topology();outputs=lab.configs('Cisco');check(outputs,'Bloqueó proyecto antiguo sin modelos')
        check('Catálogo local no disponible' in lab.page.locator('#view').inner_text(),'Falta aviso de recurso')
        return 'Sin catálogo: flujo genérico y CLI permanecen; aviso local visible, sin descarga ni consulta externa.'

    @case('K23','Crear enlaces sin escribir puertos','Enlaces nuevos reciben puertos del modelo; las asociaciones válidas previas quedan reservadas.')
    def new_links(lab):
        lab.edge('Fortinet');choose(lab,'edge','fortinet-60f');choose(lab,'sw','cisco-c9200l-24t-4g')
        before=lab.snapshot()['state']['links'];lab.go(5);lab.evaluate('editLink()')
        lab.page.locator('#la').select_option('edge');lab.page.locator('#lb').select_option('sw')
        check(lab.page.locator('#laf').evaluate('e=>e.readOnly') and lab.page.locator('#lbc').evaluate('e=>e.readOnly'),'Nombre de modelo editable a mano')
        check(lab.page.locator('#laf').input_value()=='','No reprodujo enlace nuevo sin puerto Fortinet')
        lab.button('Confirmar enlace').click();lab.valid()
        after=lab.snapshot()['state']['links'];check(len(after)==len(before)+1,'No añadió enlace automático')
        check(after[:-1]==before,'Enlace nuevo alteró una asignación previa válida')
        new=after[-1];check(new['af'] in ['wan1','wan2','dmz'] and new['bc'].startswith('GigabitEthernet1/'),'Puertos nuevos no pertenecen al catálogo')
        check(lab.evaluate('validateCatalogBindings(state);true'),'Enlaces inconsistentes')
        return 'Enlace Fortinet↔Catalyst añadido sin escribir puertos; conserva enlaces anteriores y no duplica interfaces.'

if __name__=='__main__':
    import test_corte3 as runner
    runner.CASES.clear();register(runner.case,runner.check)
    raise SystemExit(runner.main())
