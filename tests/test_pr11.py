#!/usr/bin/env python3
"""Regresión funcional del PR #11; HTTP limpio y datos ficticios, sin CLI remota."""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]

def register(case,check):
    def model(lab,identifier,identifier_model):
        lab.go(5);lab.page.locator('#model-'+identifier).select_option(identifier_model);lab.valid()
    def profiles(lab,settings):
        lab.go(5)
        if lab.button('Editar fabricantes').count():lab.button('Editar fabricantes').click()
        for i in range(2):
            for role,brand in settings.items():lab.page.locator(f'#vp{i}_{role}').select_option(brand)
        lab.button('Confirmar fabricantes').click();lab.valid()
    def mixed(lab):
        lab.lab();profiles(lab,{'router':'Cisco','core':'Huawei','distribution':'Huawei','access':'Huawei','firewall':'Fortinet','backupRouter':'MikroTik'})
        lab.button('Generar desde el plan').click();lab.valid()
    @case('F01','Datos confirmados y persistencia','Confirmar bloquea campos; editar igualdad no invalida; JSON y localStorage conservan confirmación.')
    def project(lab):
        lab.lab();lab.topology();lab.configs('Cisco');before=lab.snapshot();lab.go(1)
        lab.button('Confirmar datos del proyecto').click();lab.valid()
        check(lab.page.locator('#pname').is_disabled() and lab.button('Editar datos').count()==1,'Datos no bloqueados')
        after=lab.snapshot();check(after['state']['project']['confirmed'] is True,'Sin bandera persistida')
        for key in ['vlans','plan','nodes','links','configs','revision','approved']:check(after['state'][key]==before['state'][key],'Confirmar borró '+key)
        lab.go(0);lab.go(1);lab.button('Editar datos').click();lab.button('Confirmar datos del proyecto').click();lab.valid()
        check(lab.snapshot()==after,'Confirmar igualdad invalidó')
        lab.upload(lab.export());lab.valid();lab.evaluate('saveLocal();state=fresh();loadLocal()');lab.go(1)
        check(lab.page.locator('#pname').is_disabled(),'Confirmación perdida tras JSON/localStorage')
        return 'Datos bloqueados/Editar; igualdad conserva plan y CLI; confirmación v4 restaurada desde JSON y almacenamiento.'

    @case('F02','Proyecto: validación atómica y metadatos','Entrada inválida conserva formulario/estado; editar texto informativo conserva redes; cambios estructurales invalidan.')
    def project_error(lab):
        lab.lab();lab.topology();lab.go(1);before=lab.snapshot();lab.button('Aplicar número de sedes').click();check(lab.snapshot()==before,'Aplicar cantidad idéntica invalidó');lab.page.locator('#pname').fill('')
        lab.atomic_error(lambda:lab.button('Confirmar datos del proyecto').click(),'#pname')
        lab.page.locator('#pname').fill('LAB-NOMBRE-NUEVO');before=lab.snapshot()['state']['plan'];lab.button('Confirmar datos del proyecto').click();lab.valid()
        check(lab.snapshot()['state']['plan']==before,'Metadato borró redes')
        lab.button('Editar datos').click();lab.page.locator('#pinter').uncheck();lab.button('Confirmar datos del proyecto').click();lab.valid()
        check(not lab.snapshot()['state']['approved'],'Cambio estructural mantuvo aprobación obsoleta')
        payload=lab.export();payload['state']['project']['confirmed']='true';before=lab.snapshot();lab.upload(payload)
        check(lab.snapshot()==before,'Importación aceptó tipo de confirmación inválido')
        lab.lab();lab.go(1);lab.page.locator('#pname').fill('LAB-NOMBRE-PENDIENTE');lab.page.locator('#sitecount').fill('3');lab.button('Aplicar número de sedes').click();check(lab.page.locator('#pname').input_value()=='LAB-NOMBRE-PENDIENTE','Aplicar sedes perdió datos pendientes');lab.button('Confirmar datos del proyecto').click();lab.valid();check(lab.evaluate('state.project.name')=='LAB-NOMBRE-PENDIENTE','No confirmó los datos conservados')
        return 'Error atómico, metadatos sin pérdida de redes; misma cantidad no invalida; cambio de sedes conserva identificación pendiente; tipo de bandera inválido rechazado.'

    @case('F03','Fabricantes sin perder VLAN/VLSM','Cambiar una marca permanece en Topología; conserva plan/IPv6, confirma y borra solo CLI dependientes.')
    def brands(lab):
        lab.lab();lab.topology();lab.configs('Cisco');lab.ipv6();before=lab.snapshot()['state'];lab.go(5)
        lab.page.locator('#vp0_access').select_option('Huawei');lab.button('Confirmar fabricantes').click();lab.valid()
        after=lab.snapshot()['state'];check(lab.evaluate('page')==5 and lab.evaluate('confirmedPlan()'),'Expulsó de Topología o desconfirmó plan')
        for key in ['plan','vlans','ipv6Plan','approved','revision']:check(after[key]==before[key],'Cambiar marca alteró '+key)
        check(lab.page.locator('#vp0_access').is_disabled() and lab.button('Editar fabricantes').count()==1,'Sin confirmación visual')
        other=[n['id'] for n in before['nodes'] if n['site']=='s2']
        check(all(after['configs'].get(k)==v for k,v in before['configs'].items() if any(k.startswith(i+'-') for i in other)),'Perdió CLI de otra sede')
        check(any(n['vendor']=='Huawei' and n.get('autoKey','').split(':')[1:2]==['access'] for n in after['nodes']),'Marca no aplicada al equipo automático')
        lab.upload(lab.export());lab.valid();lab.go(5);check(lab.button('Editar fabricantes').count()==1,'Confirmación fabricantes no persistida')
        return 'Topología permanece accesible y aprobada; plan/IPv6 intactos; marcas automáticas y cachés dependientes actualizadas; JSON conserva estado.'

    @case('F04','Funciones opcionales y nuevas /30','Añadir firewall/backup conserva redes previas y agrega solo /30 necesarias; igualdad no llama allocate.')
    def extra_transit(lab):
        lab.lab();before=lab.snapshot()['state']['plan']
        profiles(lab,{'router':'Cisco','core':'Cisco','distribution':'Cisco','access':'Cisco','firewall':'Fortinet','backupRouter':'MikroTik'})
        after=lab.snapshot()['state']['plan'];check(all(r in after for r in before),'Movió/redimensionó una red existente')
        check(lab.evaluate('confirmedPlan()') and any(r['key']=='f-s1' for r in after),'Faltan nuevas /30 o aprobación')
        calls=lab.evaluate('__calls4');lab.button('Editar fabricantes').click();lab.button('Confirmar fabricantes').click();lab.valid()
        check(lab.evaluate('__calls4')==calls and lab.snapshot()['state']['plan']==after,'Igualdad recalculó redes')
        return 'Nuevas funciones reservan /30 libres sin cambiar redes anteriores; misma selección no reasigna ni desconfirma.'

    @case('F05','HTML autónomo sin carpeta data','HTML solo sirve doce fichas embebidas; no solicita JS/JSON externos ni internet.')
    def standalone(lab):
        requests=[];lab.page.on('request',lambda request:requests.append(request.url))
        lab.context.route('**/data/**',lambda route:route.abort())
        lab.page.reload(wait_until='load');check(lab.evaluate('interfaceCatalog.length')==12,'HTML depende de carpeta data')
        check(not any('/data/' in url for url in requests),'Solicitó datos externos')
        lab.context.set_offline(True)
        try:
            lab.lab();lab.topology();identifier=lab.evaluate("state.nodes.find(n=>n.type==='Switch capa 3').id")
            model(lab,identifier,'cisco-c9200l-24t-4g');lab.configs('Cisco')
            check(lab.evaluate('id=>generate(node(id),"Cisco").includes("GigabitEthernet1/")',identifier),'No usa catálogo autónomo')
        finally:lab.context.set_offline(False)
        return 'Doce fichas disponibles con data/ bloqueada y sin internet; cero solicitudes de catálogo; CLI Catalyst usa nombres guardados.'

    @case('F06','Selección efectiva de doce modelos','Las doce fichas pueden elegirse en equipos/roles compatibles y generar CLI con sus puertos oficiales.')
    def twelve(lab):
        catalogue=json.loads((ROOT/'data/catalogo-interfaces.json').read_text())['models']
        for m in catalogue:
            if m['vendor'] in ['Fortinet','MikroTik']:lab.edge(m['vendor']);identifier='edge'
            else:
                lab.lab()
                if m['model']=='ISR4321/K9':
                    lab.evaluate('state.sites.forEach(s=>s.redundant=false);proposeVlans()');lab.page.locator('button[onclick="confirmVlans()"]').click();lab.valid()
                lab.topology();kind='Router' if m['model']=='ISR4321/K9' else 'Switch' if m['vendor']=='Huawei' else 'Switch capa 3'
                identifier=lab.evaluate('kind=>state.nodes.find(n=>n.type===kind).id',kind)
                if m['vendor']=='Huawei':
                    lab.evaluate('id=>editNode(id)',identifier);lab.page.locator('#nvendor').select_option('Huawei');lab.page.locator('#nmodel').select_option(m['id']);lab.button('Confirmar equipo').click();lab.valid()
            model(lab,identifier,m['id']);lab.go({'Cisco':6,'Huawei':7,'Fortinet':8,'MikroTik':9}[m['vendor']])
            cli=lab.evaluate('a=>generate(node(a[0]),a[1])',[identifier,m['vendor']]);check(cli and lab.evaluate('id=>node(id).modelId',identifier)==m['id'],'Modelo no usable '+m['id'])
            names={p['name'] for p in m['ports'] if p['assignable']}
            ports=lab.evaluate('id=>connected(node(id)).map(l=>endpoint(l,node(id),node(id).vendor).iface)',identifier)
            check(set(ports)<=names and all(name in cli for name in ports),'CLI no corresponde a ficha '+m['id'])
        return '12/12 modelos seleccionados por UI Topología/editor y usados por su adaptador; puertos coinciden con fichas sin alterar datos oficiales.'

    @case('F07','Modelo único en Topología','Cuatro módulos reutilizan selección; no muestran ni exigen selectores de modelo/puerto.')
    def selection(lab):
        for vendor,m in [('Cisco','cisco-c9200l-24t-4g'),('Huawei','huawei-s5700-28p-li-ac'),('Fortinet','fortinet-60f'),('MikroTik','mikrotik-rb750gr3')]:
            if vendor in ['Fortinet','MikroTik']:lab.edge(vendor);identifier='edge'
            else:
                lab.lab();lab.topology();identifier=lab.evaluate("state.nodes.find(n=>n.type==='Switch').id")
                if vendor=='Huawei':lab.evaluate('id=>{node(id).vendor="Huawei";render()}',identifier)
            model(lab,identifier,m);before=lab.snapshot()['state'];lab.configs(vendor)
            check(not lab.page.locator('#view select[id^="model-"],#nmodel').count(),'Volvió a pedir modelo en Configuración')
            after=lab.snapshot()['state'];check(after['nodes']==before['nodes'] and after['links']==before['links'],'Generar reasignó interfaces')
        return 'Cisco/Huawei/Fortinet/MikroTik sin selectores repetidos: leen modelos/enlaces guardados en Topología.'

    @case('F08','Comparación real de cuatro marcas','Función seleccionada muestra cuatro adaptadores, diferencias y sintaxis de equipos reales; comparación no muta state.')
    def four(lab):
        mixed(lab);before=lab.snapshot();lab.go(10)
        for feature in ['interfaces','vlans','ospf','dhcp','ssh']:
            lab.page.locator('#compareFunction').select_option(feature)
            rows=lab.evaluate('key=>compareFourEntries(key)',feature)
            check([r['vendor'] for r in rows]==['Cisco','Huawei','Fortinet','MikroTik'],'Falta marca')
            check(all(r['text'] or r['reason'] for r in rows),'Tarjeta vacía/inventada')
            if feature=='interfaces':check(all(r['text'] for r in rows),'Marca real compatible sin interfaz comparada')
            check(lab.snapshot()==before,'Comparación mutó proyecto/configs')
        return 'Cinco funciones × cuatro fabricantes; extractos reales/diferencias y límites; estado/CLI guardada intactos.'

    @case('F09','Comparación sin equivalencias falsas','Marca ausente/función desactivada produce aviso, no un router/firewall ficticio; mantiene IOS/VRP válido.')
    def unsupported(lab):
        lab.lab();lab.topology();lab.go(10)
        rows=lab.evaluate('compareFourEntries("interfaces")');check(all(not r['text'] and r['reason'] for r in rows if r['vendor']!='Cisco'),'Inventó marcas ausentes')
        lab.evaluate('state.opts.ospf=false');check(all(not r['text'] and r['reason'] for r in lab.evaluate('compareFourEntries("ospf")')),'Ignoró función desactivada')
        lab.evaluate('state.opts.ospf=true');identifier=lab.evaluate("configNodes('Cisco')[0].id");lab.evaluate('id=>generateCompare(id)',identifier);lab.valid()
        check(lab.evaluate('id=>!!state.configs[id+"-Cisco"]&&!!state.configs[id+"-Huawei"]',identifier),'Perdió equivalencia IOS/VRP válida')
        return 'Sin equipo/función: avisos sin CLI ficticia; equivalencia adicional IOS/VRP existente conservada.'

    @case('F10','Comandos simulados por fabricante','Todos los comandos anunciados responden con datos del proyecto; espacios/mayúsculas razonables se normalizan.')
    def ssh(lab):
        total=0
        for vendor in ['Cisco','Huawei','Fortinet','MikroTik']:
            if vendor in ['Fortinet','MikroTik']:lab.edge(vendor);identifier='edge'
            else:
                lab.lab();lab.topology()
                if vendor=='Huawei':lab.evaluate("state.nodes.filter(configurable).forEach(n=>n.vendor='Huawei')")
                lab.configs(vendor);identifier=lab.evaluate('v=>configNodes(v)[0].id',vendor)
            lab.evaluate('state.configs={}') # La lectura también debe funcionar sin generación previa en otro módulo.
            lab.go(13);lab.page.locator('#sshDevice').select_option(identifier)
            for command in lab.evaluate('v=>sshCommands({vendor:v})',vendor):
                lab.page.locator('#sshCommand').fill('  '+command.upper().replace(' ','   ')+'  ');lab.button('Enviar comando').click()
                output=lab.page.locator('#sshSimulation').inner_text();check('SIMULACIÓN' in output and 'Comando no disponible' not in output and 'Genere primero' not in output,'Comando anunciado falló '+vendor+' '+command);total+=1
            check(lab.evaluate('sshSocket===null'),'Simulación abrió SSH real')
        return str(total)+' comandos anunciados (4 fabricantes) respondieron, con espacios/mayúsculas; cero conexiones reales.'

    @case('F11','Simulación rechaza comandos ajenos','CLI de otra marca/comandos de escritura no se ejecutan ni producen respuestas operativas ficticias.')
    def ssh_negative(lab):
        lab.lab();lab.topology();before=lab.snapshot();lab.go(13);identifier=lab.evaluate('state.nodes[0].id');lab.page.locator('#sshDevice').select_option(identifier)
        for command in ['configure terminal','display vlan','/system reset-configuration','show ip route;reload']:
            lab.page.locator('#sshCommand').fill(command);lab.page.locator('#sshCommand').press('Enter');check('Comando no disponible' in lab.page.locator('#sshSimulation').inner_text(),'Aceptó comando no soportado')
        check(lab.snapshot()==before and lab.evaluate('sshSocket===null'),'Comando mutó estado o abrió red')
        return 'Comandos ajenos, escritura e inyección rechazados; solo buffer simulado cambia; proyecto y servicio real intactos.'

    @case('F12','Manual integrado offline ES/EN','Manual abre sin Python/popup/red y muestra comandos de cuatro marcas y seguridad real en ambos idiomas.')
    def manual(lab):
        lab.go(13);before=lab.snapshot();lab.context.set_offline(True)
        try:
            for lang,name,close in [('es','Manual de consola SSH','Cerrar manual'),('en','SSH console manual','Close manual')]:
                lab.evaluate('lang=>setLanguage(lang)',lang);lab.button(name).click()
                check(lab.page.locator('#modal').is_visible(),'Manual no abrió')
                text=lab.page.locator('#modalbody').inner_text()
                for command in ['show running-config','display current-configuration','get router info routing-table all','/export']:check(command in text,'Manual sin comando '+command)
                lab.button(close).click()
        finally:lab.context.set_offline(False)
        check(lab.snapshot()==before,'Abrir manual cambió proyecto')
        return 'Manual en diálogo local ES/EN con comandos y límites de las cuatro marcas; sin Python, solicitudes ni ventanas externas.'

    @case('F13','Revisión visual de flujos','Proyecto/fabricantes confirmados, Topología, cuatro configuraciones, comparación y manual accesibles a 1440/390 px.')
    def visual(lab):
        mixed(lab)
        out=Path('/tmp/wan-pr11-visual');out.mkdir(exist_ok=True)
        for width in [1440,390]:
            lab.page.set_viewport_size({'width':width,'height':900})
            for page in [1,5,6,7,8,9,10,13]:
                lab.go(page);check(lab.evaluate('page')==page,'Navegación se bloqueó')
                check(lab.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Desborde '+str(page))
                if page in [5,10]:
                    if page==10:lab.page.locator('#compareFunction').scroll_into_view_if_needed()
                    lab.page.wait_for_timeout(250);lab.page.screenshot(path=str(out/f'flujo-{page}-{width}.png'))
            lab.button('Manual de consola SSH').click();lab.page.wait_for_timeout(150);lab.page.screenshot(path=str(out/f'manual-{width}.png'));lab.button('Cerrar manual').click()
        return '16 vistas (8 × 2 anchos) sin desbordes; capturas reales de Topología, comparación y manual en /tmp/wan-pr11-visual.'

if __name__=='__main__':
    import test_corte3 as runner
    runner.CASES.clear();register(runner.case,runner.check)
    raise SystemExit(runner.main())
