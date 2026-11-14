#!/usr/bin/env python3
"""Laboratorio público completo y tabla física: E2E offline, sin infraestructura ni CLI ejecutada."""
from pathlib import Path
import copy,ipaddress,json
ROOT=Path(__file__).resolve().parents[1]

def register(case,check):
    def load(lab):
        lab.go(1);lab.button('Cargar ejemplo de laboratorio').click(timeout=30000);lab.valid()
        return lab.snapshot()['state']
    def table(lab,vendor):
        lab.go({'Cisco':6,'Huawei':7,'Fortinet':8,'MikroTik':9}[vendor]);lab.valid()
        return lab.page.locator('table.physical-inventory')

    @case('L01','Laboratorio público: 15 pasos integrales','Cargar el botón real offline y verificar proyecto/sedes/RFC1918/VLSM/redes/topología/modelos/puertos/marcas/CLI/tabla/comparación/SSH/JSON/offline.')
    def e2e(lab):
        calls=lab.evaluate('({allocate:0})')
        lab.evaluate('''window.__labSteps={project:0,site:0,counts:0,vlans:0,vendors:0,topology:0};
            for(const [name,key] of [['saveProject','project'],['saveSite','site'],['saveCounts','counts'],['confirmVlans','vlans'],['saveVendorProfiles','vendors'],['buildTopology','topology']]){const original=window[name];window[name]=(...args)=>{__labSteps[key]++;return original(...args)}}''')
        lab.context.set_offline(True)
        steps=[]
        try:
            data=load(lab);check(lab.evaluate('projectValid();true') and data['project'].get('confirmed') is True,'Proyecto no validado');steps.append('proyecto')
            check(len(data['sites'])==2 and all(s.get('confirmed') and s.get('counts') and s.get('vendorsConfirmed') for s in data['sites']),'Fichas/inventario/fabricantes no confirmados');steps.append('dos sedes')
            pools={s['id']:ipaddress.IPv4Network(s['ipv4Base']) for s in data['sites']}
            check(str(pools['s1'])=='192.168.32.0/21' and str(pools['s2'])=='172.16.64.0/21','No utiliza rangos distintos esperados')
            check(data['project']['transitBase']=='10.250.0.0/24','Tránsito no independiente');steps.append('RFC1918 distintos')
            check(lab.evaluate('confirmedPlan()') and data['approved'],'Aprobación no representa un plan válido')
            actual_calls=lab.evaluate('__labSteps');check(actual_calls['project']>=1 and actual_calls['site']==2 and actual_calls['counts']==2 and actual_calls['vlans']>=1 and actual_calls['vendors']>=1 and actual_calls['topology']>=1,'Se marcaron confirmaciones sin sus validadores')
            for r in data['plan']:
                network=ipaddress.IPv4Network(f"{r['network']}/{r['prefix']}")
                check(any(network.subnet_of(ipaddress.IPv4Network(p)) for p in ['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']),'Red no RFC1918')
                check(network.subnet_of(pools[r['site']] if r['kind']=='vlan' else ipaddress.IPv4Network(data['project']['transitBase'])),'Red fuera de pool')
                if r['kind']=='vlan':
                    import math
                    check(r['available']>=math.ceil(r['hostsRequested']*(1+data['project']['growth']/100)),'Capacidad/crecimiento insuficientes')
                    check(ipaddress.IPv4Address(r['gateway']) in network and r['gateway'] not in [str(network.network_address),str(network.broadcast_address)],'Gateway inválido')
            steps.append('VLAN/VLSM/capacidad/gateway')
            networks=[ipaddress.IPv4Network(f"{r['network']}/{r['prefix']}") for r in data['plan']]
            check(all(not a.overlaps(b) for i,a in enumerate(networks) for b in networks[i+1:]),'Solapamientos');steps.append('sin solapamientos')
            check(data['nodes'] and data['links'] and not lab.evaluate('topologyIssues().filter(x=>x.block)'),'Topología incoherente');steps.append('topología')
            devices=lab.evaluate('state.nodes.filter(n=>configurable(n)||fortinetNode(n)||mikrotikNode(n))')
            check(all(n.get('modelId') for n in devices),'Hay equipo CLI sin modelo')
            for n in devices:check(lab.evaluate('id=>!!validateNodeModel(node(id))',n['id']),'Modelo/rol incompatible')
            steps.append('modelos compatibles')
            check(lab.evaluate('validateCatalogBindings(state);true'),'Interfaces inconsistentes')
            for n in devices:
                names=lab.evaluate('id=>connected(node(id)).map(l=>endpoint(l,node(id),node(id).vendor).iface)',n['id'])
                capacity=lab.evaluate('id=>modelById(node(id).modelId).ports.filter(p=>p.assignable).length',n['id'])
                check(len(names)<=capacity and len(set(names))==len(names),'Puertos insuficientes o duplicados')
            steps.append('interfaces suficientes')
            vendors=['Cisco','Huawei','Fortinet','MikroTik'];check({n['vendor'] for n in devices}==set(vendors),'Faltan fabricantes mixtos');steps.append('cuatro marcas')
            dns=ipaddress.IPv4Address(data['project']['dns']);check(any(n['type']=='Servidor' and n['ip']==str(dns) for n in data['nodes']),'DNS no corresponde a servidor real del proyecto')
            for vendor in vendors:
                outputs=lab.configs(vendor);check(outputs,'Configuración vacía '+vendor)
                for n in [x for x in devices if x['vendor']==vendor]:
                    cli=outputs[n['id']+'-'+vendor]
                    check(lab.evaluate('id=>connected(node(id)).every(l=>{const e=endpoint(l,node(id),node(id).vendor);return l.type!=="routed"||e.r&&e.ip})',n['id']),'Extremo sin IP /30')
                    physical=lab.evaluate('id=>connected(node(id)).filter(l=>l.type==="routed").map(l=>{const e=endpoint(l,node(id),node(id).vendor);return {ip:e.ip,mask:e.r.mask,prefix:e.r.prefix}})',n['id'])
                    check(all(e['ip'] in cli and (e['mask'] in cli or e['ip']+'/'+str(e['prefix']) in cli) for e in physical),'CLI no usa IP/máscara de cada /30')
                    if vendor in ['Cisco','Fortinet','MikroTik']:
                        check({'Cisco':'router ospf','Fortinet':'config router ospf','MikroTik':'/routing ospf interface-template'}[vendor] in cli,'Falta OSPF del fabricante en el laboratorio')
                    if n['type']=='Switch capa 3':
                        for r in data['plan']:
                            if r['kind']=='vlan' and r['site']==n['site']:check(lab.evaluate('a=>coreAddress(node(a[0]),a[1])',[n['id'],r]) in cli,'SVI/core/gateway no corresponde al plan')
                    check(n['name'] in cli and all(name in cli for name in lab.evaluate('id=>connected(node(id)).map(l=>endpoint(l,node(id),node(id).vendor).iface)',n['id'])),'CLI no usa nombres reales')
                if vendor=='Cisco':check(any('dns-server '+str(dns) in text for text in outputs.values()),'DHCP no usa DNS privado')
            aps=[n for n in data['nodes'] if n['type']=='Access Point'];check(aps and all(n['ip'] and n['network'] and n['id']+'-'+n['vendor'] not in data['configs'] for n in aps),'AP eliminado o con CLI genérica')
            steps.append('CLI y rutas del plan')
            for vendor in vendors:
                inventory=table(lab,vendor);check(inventory.count()==1,'Falta tabla')
                check(inventory.locator('thead th').all_text_contents()==['Equipo','Tipo','Fabricante','Modelo','Interfaz','Función','Conectado a'],'Columnas incompletas')
                for n in [x for x in devices if x['vendor']==vendor]:
                    group=inventory.locator(f'tbody[data-device="{n["id"]}"]');links=lab.evaluate('id=>connected(node(id))',n['id'])
                    check(group.locator('tr').count()==len(links),'No muestra todos los puertos asignados')
                    text=group.inner_text();check(n['name'] in text and vendor in text and lab.evaluate('id=>modelById(node(id).modelId).model',n['id']) in text,'Datos de equipo erróneos')
                    for l in links:
                        iface=lab.evaluate('args=>endpoint(state.links.find(l=>l.id===args[0]),node(args[1]),node(args[1]).vendor).iface',[l['id'],n['id']]);peer=lab.evaluate('id=>node(id).name',l['b'] if l['a']==n['id'] else l['a'])
                        row=group.locator(f'tr[data-link="{l["id"]}"]');check(iface in row.inner_text() and peer in row.inner_text(),'Puerto/vecino no corresponden al enlace')
                check(not lab.page.locator('#view select[id^="model-"]').count(),'Solicita modelo de nuevo')
            steps.append('tabla física exacta')
            lab.go(10);check(all(r['text'] for r in lab.evaluate('compareFourEntries("interfaces")')),'Comparación incompleta');steps.append('comparación')
            lab.go(13)
            for vendor in vendors:
                n=next(n for n in devices if n['vendor']==vendor);lab.page.locator('#sshDevice').select_option(n['id'])
                command={'Cisco':'show ip route','Huawei':'display ip routing-table','Fortinet':'get router info routing-table all','MikroTik':'/ip route print'}[vendor]
                lab.page.locator('#sshCommand').fill(command);lab.page.locator('#sshCommand').press('Enter')
                check('SIMULACIÓN' in lab.page.locator('#sshSimulation').inner_text() and 'Comando no disponible' not in lab.page.locator('#sshSimulation').inner_text(),'Simulación falló')
            steps.append('SSH simulado')
            expected=lab.snapshot();expected['state'].setdefault('subnetOK',False);calls=lab.evaluate('[__calls4,__calls6]');lab.upload(lab.export());lab.valid()
            check(lab.snapshot()==expected and lab.evaluate('[__calls4,__calls6]')==calls,'JSON pierde datos o redistribuye redes');steps.append('JSON v4 exacto')
            check(not lab.external and lab.evaluate('sshSocket===null'),'Red externa o SSH real abierto');steps.append('offline')
            check(len(steps)==15,'Faltan pasos integrales')
            return f'15/15 pasos: {", ".join(steps)}; {len(data["plan"])} redes, {len(data["nodes"])} nodos, {len(data["links"])} enlaces y {len(devices)} configuraciones nativas; AP conservados.'
        finally:lab.context.set_offline(False)

    @case('L02','Inventario físico ES/EN responsive','Tabla agrupada en cuatro módulos; columnas traducidas, CLI debajo, anchos 1440/390 sin desborde nuevo.')
    def responsive(lab):
        load(lab);before=lab.snapshot();out=Path('/tmp/wan-laboratorio-visual');out.mkdir(exist_ok=True)
        for lang in ['es','en']:
            lab.evaluate('lang=>setLanguage(lang)',lang)
            for width in [1440,390]:
                lab.page.set_viewport_size({'width':width,'height':900})
                for vendor in ['Cisco','Huawei','Fortinet','MikroTik']:
                    inventory=table(lab,vendor);check(lab.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Desborde '+vendor)
                    expected=['Equipo','Tipo','Fabricante','Modelo','Interfaz','Función','Conectado a'] if lang=='es' else ['Device','Type','Manufacturer','Model','Interface','Function','Connected to']
                    check(inventory.locator('thead th').all_text_contents()==expected,'Columnas sin traducir')
                    check(lab.evaluate('''()=>{const table=document.querySelector('.physical-inventory'),cli=document.querySelector('.console');return table&&cli&&!!(table.compareDocumentPosition(cli)&Node.DOCUMENT_POSITION_FOLLOWING)}'''),'CLI no aparece debajo de la tabla')
                    inventory.scroll_into_view_if_needed();lab.page.wait_for_timeout(180)
                    if lang=='es':lab.page.screenshot(path=str(out/f'inventario-{vendor}-{width}.png'))
        check(lab.snapshot()==before,'Tabla/idioma cambió datos o CLI')
        return '16 combinaciones marca/idioma/ancho; tablas agrupadas y CLI debajo; capturas reales en /tmp/wan-laboratorio-visual; proyecto intacto.'

    @case('L03','Modo genérico y datos reales','Proyectos anteriores sin modelo mantienen generación y tabla en Modo genérico con interfaces/vecinos reales.')
    def generic(lab):
        lab.lab();lab.topology();lab.configs('Cisco');inventory=table(lab,'Cisco')
        check('Modo genérico' in inventory.inner_text(),'No identifica modo genérico')
        identifier=lab.evaluate("configNodes('Cisco')[0].id");name=lab.evaluate('id=>node(id).name',identifier)
        check(name in inventory.inner_text() and 'GigabitEthernet0/' in inventory.inner_text(),'Inventario usa nombres fijos')
        before=lab.snapshot();lab.evaluate("setLanguage('en')");check('Generic mode' in lab.page.locator('.physical-inventory').inner_text(),'Genérico no traducido');check(lab.snapshot()==before,'Leer tabla mutó estado')
        return 'Modo genérico visible ES/EN, nombres/puertos/enlaces del proyecto anterior; generación y datos preservados.'

    @case('L04','Carga cancelada y fallo atómico','Cancelar o catálogo sin candidatos conserva proyecto, borradores y localStorage; no sobrescribe proyectos importados.')
    def atomic(lab):
        lab.lab();lab.topology();lab.evaluate('saveLocal()');lab.go(1);lab.page.locator('#pname').fill('BORRADOR-USUARIO')
        before=lab.snapshot();storage=lab.evaluate('JSON.stringify(localStorage)');renders=lab.evaluate('__renders')
        lab.accept_dialog=False;lab.button('Cargar ejemplo de laboratorio').click();lab.accept_dialog=True
        check(lab.snapshot()==before and lab.evaluate('__renders')==renders and lab.page.locator('#pname').input_value()=='BORRADOR-USUARIO','Cancelar cambió datos/DOM')
        lab.evaluate('window.__modelsFor=modelsFor;modelsFor=()=>[]')
        lab.button('Cargar ejemplo de laboratorio').click(timeout=30000)
        check(lab.page.locator('#toast.error').count()==1,'No indicó catálogo incompatible')
        check(lab.snapshot()==before and lab.page.locator('#pname').input_value()=='BORRADOR-USUARIO' and lab.evaluate('JSON.stringify(localStorage)')==storage,'Fallo perdió datos/borrador/almacenamiento')
        lab.evaluate('modelsFor=__modelsFor');load(lab);lab.evaluate('saveLocal();state=fresh();loadLocal()');lab.valid();check(lab.evaluate('confirmedPlan()'),'Laboratorio no restaura')
        lab.upload({'state':before['state'],'imageData':''});lab.valid();after=lab.snapshot()['state'];check(after['project']==before['state']['project'] and after['plan']==before['state']['plan'],'Importar proyecto anterior cambió sus redes')
        return 'Cancelar sin mutación; catálogo sin candidatos revierte el reemplazo y conserva borrador/localStorage; guardar/cargar laboratorio e importar usuario preservan redes.'

    @case('L05','Laboratorio determinista y regenerable','Dos cargas/regeneración conservan redes, marcas, modelos y asignaciones; capacidad real sin puertos inventados.')
    def stable(lab):
        first=load(lab);lab.go(5);lab.button('Generar desde el plan').click();lab.valid();regenerated=lab.snapshot()['state']
        check(regenerated['plan']==first['plan'] and regenerated['links']==first['links'],'Regenerar mueve redes o puertos')
        check([(n['id'],n.get('modelId')) for n in regenerated['nodes']]==[(n['id'],n.get('modelId')) for n in first['nodes']],'Modelos/IDs perdidos')
        second=load(lab);check(second['plan']==first['plan'] and second['nodes']==first['nodes'] and second['links']==first['links'] and second['configs']==first['configs'],'Misma entrada no es determinista')
        return 'Dos cargas y regeneración: redes/orden, IDs, modelos, enlaces/puertos y configuraciones estables; validación de capacidad y exclusión AP vigentes.'

if __name__=='__main__':
    import test_corte3 as runner
    runner.CASES.clear();register(runner.case,runner.check)
    raise SystemExit(runner.main())
