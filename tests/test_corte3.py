#!/usr/bin/env python3
"""Regresión local Corte 3. No aplica CLI ni modifica WAN_v4.html.

python tests/test_corte3.py
python tests/test_corte3.py --report tests/reporte-corte3.html \
    --capture docs/capturas/09-pruebas.png

Los resultados normales se escriben fuera del repositorio, en un directorio
 temporal anunciado al terminar. No depende de Node, pytest ni datos de sesión.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import importlib.metadata
import ipaddress
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[1]
APPLICATION = ROOT / "WAN_v4.html"
FIXTURE = ROOT / "tests/fixtures/laboratorio-v2.json"
CASES = []


def check(condition, message):
    """No usa assert: también falla si Python se ejecuta con -O."""
    if not condition:
        raise AssertionError(message)


def case(identifier, name, expected):
    def register(function):
        CASES.append((identifier, name, expected, function))
        return function
    return register


def network(row):
    return ipaddress.ip_network(f"{row['network']}/{row['prefix']}")


def disjoint(rows):
    nets = [network(row) for row in rows]
    check(all(not a.overlaps(b) for i, a in enumerate(nets) for b in nets[i + 1:]),
          "Hay redes IPv4 solapadas")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class Lab:
    """Un contexto nuevo por caso, con estado/almacenamiento aislados."""
    def __init__(self, browser, url):
        self.context = browser.new_context(viewport={"width": 1440, "height": 900},
                                           locale="es-CO", timezone_id="America/Bogota")
        self.page = self.context.new_page()
        self.page.set_default_timeout(7000)
        self.errors = []
        self.external = []
        self.origin = url.rsplit("/", 1)[0] + "/"
        self.accept_dialog = True
        self.page.on("dialog", lambda dialog: dialog.accept() if self.accept_dialog else dialog.dismiss())
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.on("console", lambda message: self.errors.append(message.text)
                     if message.type == "error" else None)
        self.context.route("**/*", self._route)
        response = self.page.goto(url, wait_until="load")
        check(response and response.status == 200, "No se pudo cargar el HTML local")
        check(self.page.evaluate("state.version===4 && state.vlans.length===0 && localStorage.length===0"),
              "El contexto no inició limpio en v4")
        self.page.evaluate("""window.__renders=0;window.__render=render;
            render=function(){__renders++;return __render()};
            window.__calls4=0;window.__calls6=0;
            const a4=allocate,a6=allocateIPv6;
            allocate=(...a)=>{__calls4++;return a4(...a)};
            allocateIPv6=(...a)=>{__calls6++;return a6(...a)};void 0""")

    def _route(self, route):
        url = route.request.url
        if url.startswith(self.origin):
            route.continue_()
        else:
            self.external.append(url)
            route.abort()

    def close(self):
        self.context.close()

    def evaluate(self, expression, arg=None):
        return self.page.evaluate(expression, arg)

    def snapshot(self):
        return self.evaluate("JSON.parse(JSON.stringify({state,imageData}))")

    def button(self, name):
        return self.page.get_by_role("button", name=name, exact=True)

    def go(self, page):
        self.evaluate("p=>go(p)", page)

    def fixture(self, version=2):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        if version == 3:
            # Muestra v3 explícita a partir del laboratorio v2: solo cambia
            # su contrato de intención; el plan y las cuatro CLI quedan intactos.
            payload["state"]["version"] = 3
            payload["state"]["project"]["transitBase"] = ""
            for site in payload["state"]["sites"]:
                site["ipv4Base"] = ""
            for vlan in payload["state"]["vlans"]:
                vlan["ipv4Cidr"] = ""
            for row in payload["state"]["plan"]:
                if row["kind"] == "vlan":
                    row["ipv4Cidr"] = ""
        return payload

    def upload(self, payload):
        control = self.page.locator('input[onchange="importJSON(this)"]')
        control.set_input_files({"name": "laboratorio.json", "mimeType": "application/json",
                                "buffer": json.dumps(payload).encode("utf-8")})
        self.page.wait_for_function("document.querySelector('input[onchange=\"importJSON(this)\"]').value === ''")

    def export(self):
        with self.page.expect_download() as download:
            self.button("Exportar JSON").click()
        return json.loads(Path(download.value.path()).read_text(encoding="utf-8"))

    def valid(self):
        check(not self.page.locator("#toast.error").count(),
              self.page.locator("#toast").inner_text())

    def lab(self, scoped=False):
        self.go(1)
        self.evaluate("demo();proposeVlans()")
        if scoped:
            self.evaluate("""state.sites[0].ipv4Base='10.20.16.0/20';
                state.sites[1].ipv4Base='10.20.32.0/20';
                state.project.transitBase='10.20.250.0/24';render()""")
            self.page.locator("#vc0").fill("10.20.20.0/24")
            index = self.evaluate("state.vlans.findIndex(v=>v.site==='s2')")
            self.page.locator(f"#vc{index}").fill("10.20.35.0/24")
        self.button("Confirmar VLAN y calcular VLSM").click()
        self.valid()
        return self.snapshot()["state"]

    def topology(self):
        self.go(5)
        self.button("Generar desde el plan").click()
        self.valid()
        check(self.page.locator("#toposvg").count() == 1, "Falta el SVG de topología")
        check(not self.evaluate("topologyIssues().filter(x=>x.block)"), "Topología bloqueada")

    def configs(self, vendor):
        self.go({"Cisco": 6, "Huawei": 7, "Fortinet": 11, "MikroTik": 12}[vendor])
        self.button(f"Generar todos los {vendor}").click()
        self.valid()
        return {key: value["text"] for key, value in self.snapshot()["state"]["configs"].items()
                if key.endswith("-" + vendor)}

    def edge(self, vendor):
        self.go(1)
        self.evaluate("demo();state.sites.forEach(s=>s.redundant=false);proposeVlans()")
        self.button("Confirmar VLAN y calcular VLSM").click()
        self.valid()
        self.evaluate("""vendor=>{
            const n=(id,name,type,brand,site)=>({id,name,type,vendor:brand,site,ip:'',network:'',x:100,y:100});
            const l=(id,a,b,type,network,ia,ib)=>({id,a,b,type,network,vlan:0,bundle:0,
                ac:'GigabitEthernet0/'+ia,bc:'GigabitEthernet0/'+ib,
                ah:'GigabitEthernet0/0/'+ia,bh:'GigabitEthernet0/0/'+ib});
            state.nodes=[n('edge','EDGE-LAB',vendor==='Fortinet'?'Firewall':'Router',vendor,'s1'),
                n('sw','SW-LAB','Switch','Cisco','s1'),n('r1','R-LAB1','Router','Cisco','s1'),
                n('r2','R-LAB2','Router','Cisco','s2'),n('core2','CORE-LAB2','Switch capa 3','Cisco','s2')];
            state.links=[l('lan','edge','sw','trunk','',1,1),
                l('up','edge','r1','routed','t-s1-0',2,1),
                l('wan','r1','r2','routed','w-s2',2,1),
                l('core','r2','core2','routed','t-s2-0',2,1)];
            state.links[0][vendor==='Fortinet'?'af':'am']=vendor==='Fortinet'?'port1':'ether1';
            state.links[1][vendor==='Fortinet'?'af':'am']=vendor==='Fortinet'?'port2':'ether2';
            state.configs={};render();
        }""", vendor)
        payload = self.snapshot()
        self.upload(payload)
        self.valid()
        return self.configs(vendor)["edge-" + vendor]

    def ipv6(self, base="fd12:3456:789a::/48", site_blocks=None):
        self.go(13)
        self.page.locator("#ipv6Enabled").check()
        self.page.locator("#ipv6Base").fill(base)  # Fijo para pruebas deterministas.
        if site_blocks:
            for index, block in enumerate(site_blocks):
                self.page.locator(f"#ipv6Site{index}").fill(block)
        self.button("Confirmar planificación IPv6").click()
        self.valid()
        return self.snapshot()["state"]["ipv6Plan"]

    def atomic_error(self, action, input_id):
        before = self.snapshot()
        self.evaluate("saveLocal()")
        storage = self.evaluate("localStorage.getItem('WAN-Architect-v4')")
        renders = self.evaluate("__renders")
        element = self.page.locator(input_id).element_handle()
        value = self.page.locator(input_id).input_value()
        action()
        check(self.page.locator("#toast.error").count() == 1, "La operación inválida no mostró error")
        check(self.snapshot() == before, "Error no atómico: cambió el estado")
        check(self.evaluate("__renders") == renders and element.evaluate("e=>e.isConnected"),
              "Error no atómico: reconstruyó el formulario")
        check(self.page.locator(input_id).input_value() == value, "Se perdió texto pendiente")
        check(self.evaluate("localStorage.getItem('WAN-Architect-v4')") == storage,
              "Cambió almacenamiento tras error")
        return self.page.locator("#toast").inner_text()


@case("C01", "Calculadora IPv4", "192.168.10.50/26: red .0, broadcast .63 y 62 hosts; /31 y /32 correctos.")
def ipv4(lab):
    lab.go(4)
    lab.page.locator("#calc").fill("192.168.10.50/26")
    lab.button("Calcular").click()
    lab.valid()
    result = lab.evaluate("subnet('192.168.10.50/26')")
    check((result["network"], result["broadcast"], result["hosts"]) ==
          ("192.168.10.0", "192.168.10.63", 62), "Resultado /26 incorrecto")
    check(lab.evaluate("subnet('10.0.0.0/31').hosts===2&&subnet('10.0.0.1/32').hosts===1"),
          "Límites /31 y /32 incorrectos")
    return "Red 192.168.10.0/26, broadcast .63, 62 hosts; límites /31 y /32 verificados."


@case("C02", "Calculadora IPv6", "128 bits exactos, forma canónica, clasificación y broadcast no aplicable.")
def ipv6_calculator(lab):
    vectors = ["2001:0DB8:0000:0000:0001:0000:0000:0001", "::", "::1",
               "fd12:3456:789a::1", "::ffff:192.0.2.1", "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"]
    for address in vectors:
        value = lab.evaluate("x=>ipv6Number(x).toString()", address)
        check(int(value) == int(ipaddress.IPv6Address(address)), "Parser difiere de Python ipaddress")
    check(lab.evaluate("ipv6String(ipv6Number('2001:0DB8:0:0:1:0:0:1'))") == "2001:db8::1:0:0:1",
          "Canonicidad RFC 5952 incorrecta")
    for address, category in {"2001:4860::1": "Global", "fd12::1": "ULA", "fe80::1": "Link-local",
                              "ff02::1": "Multicast", "::1": "Loopback", "::": "Unspecified",
                              "2001:db8::1": "Documentación", "64:ff9b::1": "Especial"}.items():
        check(category in lab.evaluate("x=>ipv6Type(ipv6Number(x))", address), "Clasificación IPv6 incorrecta")
    lab.go(4)
    lab.page.locator("#calc").fill("2001:DB8:1234:5678::9/64")
    lab.button("Calcular").click()
    text = lab.page.locator("#calcResult").inner_text()
    check("18446744073709551616" in text and "No aplica (IPv6)" in text
          and "2001:db8:1234:5678::/64" in text, "Rango/capacidad IPv6 incorrectos")
    return "6 vectores frente a ipaddress, 8 categorías y /64 = 18446744073709551616 direcciones."


def migration(lab, version):
    source = lab.fixture(version)
    lab.upload(source)
    lab.valid()
    actual = lab.snapshot()
    expected = copy.deepcopy(source)
    state = expected["state"]
    state["version"] = 4
    state["subnetOK"] = state.get("subnetOK", False)
    state["project"].update(transitBase=state["project"].get("transitBase", ""), ipv6Base="")
    state["ipv6Plan"] = []
    for site in state["sites"]:
        site.update(ipv4Base=site.get("ipv4Base", ""), ipv6Base="")
    for vlan in state["vlans"]:
        vlan["ipv4Cidr"] = vlan.get("ipv4Cidr", "")
    for row in state["plan"]:
        if row["kind"] == "vlan":
            row["ipv4Cidr"] = row.get("ipv4Cidr", "")
    check(actual == expected, "La migración alteró datos válidos del laboratorio")
    check(lab.evaluate("__calls4===0&&__calls6===0"), "La importación ejecutó un asignador")
    return f"v{version}→v4 sin asignar; 15 VLAN, 28 nodos, 34 enlaces y 4 CLI preservados."


@case("C03", "Migración v2 → v3 → v4", "Migrar sin reasignar ni perder plan, topología, opciones o CLI válidas.")
def migration_v2(lab):
    return migration(lab, 2)


@case("C04", "Migración v3 → v4 y JSON", "Migrar v3 y exportar/importar v4 sin cambiar datos ni llamar asignadores.")
def migration_v3(lab):
    migration(lab, 3)
    payload = lab.export()
    lab.upload(payload)
    lab.valid()
    check(lab.snapshot() == payload and lab.evaluate("__calls4===0&&__calls6===0"),
          "Ida/vuelta JSON v4 no conserva el estado")
    return "v3→v4 e ida/vuelta JSON exactos; cero llamadas a allocate/allocateIPv6."


@case("C05", "Persistencia local v2/v3/v4", "Priorizar v4, migrar fallbacks y no sobrescribir claves antiguas.")
def storage(lab):
    old2, old3 = json.dumps(lab.fixture(2)), json.dumps(lab.fixture(3))
    lab.evaluate("([a,b])=>{localStorage.setItem('WAN-Architect-v2',a);localStorage.setItem('WAN-Architect-v3',b);loadLocal()}", [old2, old3])
    check(lab.evaluate("state.version===4&&localStorage.getItem('WAN-Architect-v4')===null"), "Fallback no migró solo en memoria")
    lab.ipv6()
    lab.evaluate("saveLocal()")
    saved = lab.snapshot()
    lab.page.reload(wait_until="load")
    lab.evaluate("loadLocal()")
    check(lab.snapshot() == saved, "No restauró v4 con prioridad")
    check(lab.evaluate("localStorage.getItem('WAN-Architect-v2')") == old2
          and lab.evaluate("localStorage.getItem('WAN-Architect-v3')") == old3, "Sobrescribió claves históricas")
    lab.evaluate("localStorage.removeItem('WAN-Architect-v4');localStorage.removeItem('WAN-Architect-v3');loadLocal()")
    check(lab.evaluate("state.version===4&&state.ipv6Plan.length===0"), "Fallback v2 incorrecto")
    return "v4 prioritario y restaurado; fallback v3/v2 en memoria; contenido antiguo intacto."


@case("C06", "Eliminar VLAN sin perder ediciones", "Conservar nombre/hosts pendientes; cancelar o validar mal no debe eliminar/renderizar.")
def delete_vlan(lab):
    lab.lab()
    lab.go(3)
    lab.page.locator("#vn0").fill("Nombre pendiente")
    lab.page.locator("#vh1").fill("23")
    before = lab.snapshot()
    lab.accept_dialog = False
    lab.evaluate("deleteVlan(2)")
    check(lab.snapshot() == before and lab.page.locator("#vn0").input_value() == "Nombre pendiente", "Cancelar cambió VLAN")
    lab.accept_dialog = True
    lab.evaluate("deleteVlan(2)")
    state = lab.snapshot()["state"]
    check(len(state["vlans"]) == 14 and state["vlans"][0]["name"] == "Nombre pendiente"
          and state["vlans"][1]["hosts"] == 23, "Eliminar perdió ediciones ajenas")
    lab.page.locator("#vh0").fill("0")
    lab.atomic_error(lambda: lab.evaluate("deleteVlan(2)"), "#vh0")
    return "Solo se eliminó la tercera VLAN; nombre/hosts conservados; cancelar e inválido atómicos."


@case("C07", "IPv4 por sede y CIDR manual", "Asignar dentro de pools, respetar manuales y separar /30 sin solapamientos.")
def scoped_ipv4(lab):
    state = lab.lab(scoped=True)
    disjoint(state["plan"])
    for row in state["plan"]:
        pool = state["project"]["transitBase"] if row["kind"] != "vlan" else next(
            site["ipv4Base"] for site in state["sites"] if site["id"] == row["site"])
        check(network(row).subnet_of(ipaddress.ip_network(pool)), "Red fuera del pool correspondiente")
    for vlan in state["vlans"]:
        if vlan["ipv4Cidr"]:
            row = next(row for row in state["plan"] if row["key"] == vlan["key"])
            check(str(network(row)) == vlan["ipv4Cidr"], "Se movió una subred manual")
    return f"{len(state['plan'])} redes disjuntas; manuales 10.20.20.0/24 y 10.20.35.0/24 conservadas."


@case("C08", "Error IPv4 atómico", "Entrada incompatible debe conservar estado, derivados, almacenamiento y texto.")
def ipv4_atomic(lab):
    lab.lab(scoped=True)
    lab.topology()
    lab.configs("Cisco")
    lab.go(3)
    lab.page.locator("#vn0").fill("Edición pendiente conservada")
    lab.page.locator("#vc0").fill("10.99.0.0/24")
    lab.atomic_error(lambda: lab.button("Confirmar VLAN y calcular VLSM").click(), "#vc0")
    return "CIDR fuera del bloque rechazado: estado/CLI/DOM/localStorage intactos."


@case("C09", "Planificación IPv6", "Asignar /48→/56→/64 de modo estable, con reservas según redundancia.")
def ipv6_plan(lab):
    lab.lab()
    plan = lab.ipv6(site_blocks=["", "fd12:3456:789a::/56"])
    nets = [ipaddress.ip_network(row["cidr"]) for row in plan]
    check(len(plan) == 15 and all(n.prefixlen == 64 for n in nets), "Faltan /64 por VLAN")
    check(all(not a.overlaps(b) for i, a in enumerate(nets) for b in nets[i + 1:]), "Solapamiento IPv6")
    for row in plan:
        net = ipaddress.ip_network(row["cidr"])
        check(net.subnet_of(ipaddress.ip_network(row["siteCidr"])), "VLAN fuera de su sede IPv6")
        check(ipaddress.ip_address(row["router"]) == net.network_address + 1, "Router incorrecto")
        offsets = [2, 3] if row["site"] == "s1" else [1]
        check(list(map(ipaddress.ip_address, row["physical"])) == [net.network_address + x for x in offsets], "Reservas físicas incorrectas")
    check(next(row for row in plan if row["site"] == "s1")["siteCidr"] == "fd12:3456:789a:100::/56", "No reservó primero la sede manual")
    lab.evaluate("state.sites.reverse();state.vlans.reverse();go(13)")
    lab.button("Confirmar planificación IPv6").click()
    check(lab.snapshot()["state"]["ipv6Plan"] == plan, "El orden de filas alteró el plan")
    payload = lab.export()
    lab.upload(payload)
    lab.valid()
    # El importador materializa este metadato opcional como false; no es
    # pérdida del plan. Comprobar el resto del estado completo sin omitir campos.
    expected = copy.deepcopy(payload)
    expected["state"]["subnetOK"] = expected["state"].get("subnetOK", False)
    check(lab.snapshot() == expected, "JSON v4 perdió plan/intenciones IPv6")
    return "15 /64 disjuntas; /56 manual reservado; orden estable, reservas e ida/vuelta exactos."


@case("C10", "Error IPv6 atómico", "Insuficiencia o solapamiento no deben reemplazar planes ni formulario.")
def ipv6_atomic(lab):
    lab.lab()
    lab.topology()
    lab.configs("Cisco")
    lab.ipv6()
    lab.page.locator("#ipv6Base").fill("fd12:3456:789a::/56")
    lab.atomic_error(lambda: lab.button("Confirmar planificación IPv6").click(), "#ipv6Base")
    lab.page.locator("#ipv6Base").fill("fd12:3456:789a::/48")
    for index in [0, 1]:
        lab.page.locator(f"#ipv6Site{index}").fill("fd12:3456:789a::/56")
    lab.atomic_error(lambda: lab.button("Confirmar planificación IPv6").click(), "#ipv6Site1")
    return "Capacidad /56 insuficiente y sedes solapadas rechazadas sin pérdidas."


@case("C11", "Topología e interfaces", "Los enlaces routed deben usar las /30 y extremos reales del plan confirmado.")
def topology(lab):
    lab.lab(scoped=True)
    lab.topology()
    state = lab.snapshot()["state"]
    endpoints = lab.evaluate("state.links.filter(l=>l.type==='routed').map(l=>({a:endpoint(l,node(l.a),node(l.a).vendor),b:endpoint(l,node(l.b),node(l.b).vendor)}))")
    for ends in endpoints:
        check(ends["a"]["r"]["prefix"] == 30 and ends["a"]["r"]["key"] == ends["b"]["r"]["key"], "Enlace no corresponde a /30")
        check(ends["a"]["ip"] == ends["a"]["r"]["first"] and ends["b"]["ip"] == ends["b"]["r"]["last"], "Extremos incorrectos")
    return f"{len(state['nodes'])} nodos, {len(state['links'])} enlaces; {len(endpoints)} /30 coherentes y sin bloqueos."


def legacy_cli(lab, vendor):
    lab.lab(scoped=True)
    lab.topology()
    outputs = lab.configs(vendor)
    check(len(outputs) == 14, f"Se esperaban 14 propuestas {vendor}")
    joined = "\n".join(outputs.values())
    check(("configure terminal" if vendor == "Cisco" else "system-view") in joined, "Falta modo propio del fabricante")
    check(("router ospf 1" if vendor == "Cisco" else "ospf 1 router-id") in joined, "Falta OSPF")
    check(("ip dhcp pool" if vendor == "Cisco" else "ip pool VLAN-") in joined, "Falta DHCP")
    state = lab.snapshot()["state"]
    for row in state["plan"]:
        if row["kind"] == "vlan":
            check((f"interface Vlan{row['id']}" if vendor == "Cisco" else f"interface Vlanif{row['id']}") in joined, "Falta SVI/Vlanif de VLAN real")
            check(row["gateway"] in joined, "Falta gateway del plan")
    other = "system-view" if vendor == "Cisco" else "configure terminal"
    check(other not in joined and "config system global" not in joined and "/system identity" not in joined, "Sintaxis ajena mezclada")
    return f"14 textos {vendor}; VLAN, gateways, OSPF y DHCP del plan, sin gramáticas ajenas."


@case("C12", "Cisco IOS / IOS XE (texto)", "Generar VLAN/SVI, IP, DHCP y OSPF del plan sin mezclar fabricantes.")
def cisco(lab):
    return legacy_cli(lab, "Cisco")


@case("C13", "Huawei VRP (texto)", "Generar Vlanif, IP, DHCP y OSPF del plan en gramática VRP separada.")
def huawei(lab):
    return legacy_cli(lab, "Huawei")


def fortios_tree(text):
    root = {"name": "root", "children": [], "sets": {}}
    stack = [root]
    for line in text.splitlines():
        words = shlex.split(line.strip())
        if not words or words[0].startswith("#"):
            continue
        verb = words[0]
        if verb in ("config", "edit"):
            entry = {"name": " ".join(words[1:]), "verb": verb, "children": [], "sets": {}}
            stack[-1]["children"].append(entry)
            stack.append(entry)
        elif verb in ("set", "unset"):
            stack[-1]["sets"][words[1]] = words[2:]
        elif verb in ("end", "next"):
            check(len(stack) > 1 and stack[-1]["verb"] == ("config" if verb == "end" else "edit"), "Bloques FortiOS desbalanceados")
            stack.pop()
        else:
            raise AssertionError("Verbo inesperado en propuesta FortiOS: " + verb)
    check(len(stack) == 1, "Quedaron bloques FortiOS abiertos")
    return root


@case("C14", "Fortinet FortiOS 7.4 (texto)", "Interfaces/VLAN/IP, DHCP o relay, rutas y administración restringida desde datos reales.")
def fortinet(lab):
    text = lab.edge("Fortinet")
    fortios_tree(text)
    state = lab.snapshot()["state"]
    for row in state["plan"]:
        if row["kind"] == "vlan" and row["site"] == "s1":
            check(f"set ip {row['gateway']} {row['mask']}" in text, "IP/máscara Fortinet no coincide con el plan")
    check("config system dhcp server" in text and "config router ospf" in text, "Falta DHCP/OSPF FortiOS")
    check("config firewall local-in-policy" in text and "set action deny" in text, "Falta restricción administrativa")
    check("set nat enable" not in text, "NAT implícito inseguro")
    lab.page.locator("#fodhcp").uncheck()
    lab.page.locator("#forelay").check()
    lab.page.locator("#frelay").fill("10.20.35.10")
    lab.button("Generar equipo").click()
    lab.valid()
    relay = lab.snapshot()["state"]["configs"]["edge-Fortinet"]["text"]
    check("set dhcp-relay-service enable" in relay and "10.20.35.10" in relay, "Relay FortiOS incorrecto")
    lab.page.locator("#foospf").uncheck()
    lab.button("Generar equipo").click()
    lab.valid()
    check("config router static" in lab.snapshot()["state"]["configs"]["edge-Fortinet"]["text"], "Faltan rutas estáticas FortiOS")
    return "IP/máscaras reales; estructura CLI balanceada; DHCP, relay, OSPF, rutas y local-in verificados."


def routeros_rows(text, path):
    rows = []
    for line in text.splitlines():
        if line.startswith(path + " "):
            rows.append(dict(word.split("=", 1) for word in shlex.split(line) if "=" in word))
    return rows


@case("C15", "MikroTik RouterOS 7 (texto)", "Bridge/VLAN/IP, OSPF v7, DHCP/relay y forward bloqueado por defecto.")
def mikrotik(lab):
    text = lab.edge("MikroTik")
    state = lab.snapshot()["state"]
    addresses = routeros_rows(text, "/ip address")
    lans = [row for row in state["plan"] if row["kind"] == "vlan" and row["site"] == "s1"]
    for row in lans:
        check(any(item.get("address") == f"{row['gateway']}/{row['prefix']}" for item in addresses), "Falta gateway IPv4 MikroTik")
    check(len(routeros_rows(text, "/interface bridge vlan")) == len(lans), "Tabla bridge VLAN incompleta")
    check("/routing ospf interface-template" in text and "version=2" in text, "Faltan menús OSPF de RouterOS 7")
    check(routeros_rows(text, "/ip dhcp-server"), "Falta DHCP RouterOS")
    filters = routeros_rows(text, "/ip firewall filter")
    check(any(r.get("chain") == "forward" and r.get("action") == "drop" and r.get("place-before") == "0" for r in filters), "Forward no está restringido")
    check(not any(r.get("chain") == "forward" and r.get("action") == "accept" for r in filters), "Permiso forward implícito")
    check("/ip service set telnet disabled=yes" in text and "/tool mac-server set allowed-interface-list=none" in text, "Servicios/MAC inseguros")
    lab.page.locator("#modhcp").uncheck()
    lab.page.locator("#morelay").check()
    lab.page.locator("#mrelay").fill("10.20.35.10")
    lab.button("Generar equipo").click()
    lab.valid()
    relay = lab.snapshot()["state"]["configs"]["edge-MikroTik"]["text"]
    check(all(r["dhcp-server"] == "10.20.35.10" for r in routeros_rows(relay, "/ip dhcp-relay"))
          and routeros_rows(relay, "/ip dhcp-relay"), "Relay RouterOS incorrecto")
    return "Bridge/VLAN y gateways reales; OSPF v7, DHCP/relay, servicios/MAC y forward drop verificados."


@case("C16", "Separación de cuatro fabricantes", "Cada adaptador usa su gramática; los nuevos equipos no caen en IOS/VRP.")
def separation(lab):
    lab.lab()
    lab.topology()
    samples = {vendor: "\n".join(lab.configs(vendor).values()) for vendor in ("Cisco", "Huawei")}
    samples["Fortinet"] = lab.edge("Fortinet")
    samples["MikroTik"] = lab.edge("MikroTik")
    markers = {"Cisco": "configure terminal", "Huawei": "system-view",
               "Fortinet": "config system global", "MikroTik": "/system identity"}
    for vendor, text in samples.items():
        check(markers[vendor] in text, "Falta identificador de gramática propia")
        check(all(marker not in text for other, marker in markers.items() if other != vendor), "Se mezclaron gramáticas")
    check(lab.evaluate("!configNodes('Cisco').some(n=>n.id==='edge')&&!configNodes('Huawei').some(n=>n.id==='edge')"),
          "MikroTik entra en equivalencias IOS/VRP")
    return "IOS, VRP, FortiOS y RouterOS separados; MikroTik excluido de equivalencias Cisco/Huawei."


@case("C17", "Entradas inseguras e importación", "Rechazar hostname, puertos, CIDR y versión peligrosos sin sustituir el estado.")
def unsafe(lab):
    lab.edge("MikroTik")
    source = lab.snapshot()
    payloads = []
    bad = copy.deepcopy(source)
    bad["state"]["nodes"][0]["name"] = 'EDGE; /system reboot'
    payloads.append(bad)
    bad = copy.deepcopy(source)
    bad["state"]["links"][0]["am"] = 'ether1"; /system reboot'
    payloads.append(bad)
    bad = copy.deepcopy(source)
    bad["state"]["project"]["ipv6Base"] = 'fd12::/48<script>'
    payloads.append(bad)
    bad = copy.deepcopy(source)
    bad["state"]["version"] = 99
    payloads.append(bad)
    lab.evaluate("saveLocal()")
    stored = lab.evaluate("localStorage.getItem('WAN-Architect-v4')")
    for payload in payloads:
        lab.upload(payload)
        check(lab.page.locator("#toast.error").count() == 1 and lab.snapshot() == source, "Importación insegura no atómica")
        check(lab.evaluate("localStorage.getItem('WAN-Architect-v4')") == stored, "Importación inválida alteró localStorage")
    return "4 payloads inseguros/futuros rechazados; estado y almacenamiento intactos."


@case("C18", "Sintaxis JavaScript y consola", "Compilar los scripts, cargar la app y no registrar errores JS ni solicitudes externas.")
def syntax(lab):
    count = lab.evaluate("Array.from(document.scripts).filter(s=>!s.src).map(s=>{new Function(s.textContent);return 1}).length")
    check(count >= 1 and not lab.errors and not lab.external, "Error de compilación/carga")
    return f"{count} script compilado por Chromium; consola/página limpias; sin solicitudes externas."


@case("C19", "Descargas reales", "Descargar JSON v4, una propuesta y el conjunto sin alterar su texto.")
def downloads(lab):
    lab.lab()
    lab.topology()
    outputs = lab.configs("Cisco")
    expected = next(iter(outputs.values()))
    with lab.page.expect_download() as download:
        lab.button("Télécharger").first.click()
    check(Path(download.value.path()).read_text(encoding="utf-8") == expected, "La descarga individual alteró la CLI")
    with lab.page.expect_download() as download:
        lab.button("Descargar todos").click()
    text = Path(download.value.path()).read_text(encoding="utf-8")
    check(all(output in text for output in outputs.values()), "La descarga conjunta perdió propuestas")
    payload = lab.export()
    check(payload == lab.snapshot() and payload["state"]["version"] == 4, "JSON descargado no coincide")
    return "CLI individual exacta, 14 propuestas en descarga conjunta y JSON v4 exacto."


@case("C20", "Responsive 1440 / 390 px", "Calculadora y planificación IPv6 caben en página y muestran límites IPv4.")
def responsive(lab):
    lab.lab()
    lab.ipv6()
    for width in (1440, 390):
        lab.page.set_viewport_size({"width": width, "height": 900})
        for page in (4, 13, 6, 7, 11, 12):
            lab.go(page)
            if page == 4:
                lab.page.locator("#calc").fill("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/0")
                lab.button("Calcular").click()
            dimensions = lab.evaluate("({width:innerWidth,scroll:document.documentElement.scrollWidth})")
            check(dimensions["scroll"] <= width, f"Desbordamiento en etapa {page}: {dimensions}")
            if page in (6, 7, 11, 12):
                check("exclusivamente IPv4" in lab.page.locator("#view").inner_text(), "Falta aviso del límite IPv4")
    return "12 combinaciones etapa/viewport sin desbordamiento de página; avisos IPv4 visibles."


def git_value(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "no disponible"


def summary(records):
    counts = {state: sum(r["state"] == state for r in records)
              for state in ("superada", "fallida", "bloqueada", "no ejecutada")}
    executed = counts["superada"] + counts["fallida"]
    percent = counts["superada"] / executed * 100 if executed else None
    return counts, executed, percent


def write_report(path, records, environment, elapsed):
    counts, executed, percent = summary(records)
    score = f"{counts['superada']}/{executed} · {percent:.2f}%" if percent is not None else "0/0 · no calculable"
    escape = lambda value: html.escape(str(value))
    status = "Ejecución incompleta: error de entorno/artefacto" if environment.get("fatal_error") else "Ejecución real finalizada"
    warning = ("<p><b>Error global:</b> " + escape(environment["fatal_error"]) + "</p>") if environment.get("fatal_error") else ""
    rows = "".join(f"<tr><td>{r['id']}</td><td><b>{escape(r['name'])}</b><small>{escape(r['expected'])}</small></td>"
                   f"<td>{escape(r['actual'])}</td><td class='{r['state'].split()[0]}'>{escape(r['state'].upper())}"
                   f"<small>{r['seconds']:.2f} s</small></td></tr>" for r in records)
    # Un único HTML es la evidencia legible y el origen de la captura, sin JSON
    # intermedio. Sus datos embebidos permiten cotejar doc/reporte/imagen.
    data = json.dumps({"environment": environment, "elapsed_seconds": elapsed, "records": records,
                       "counts": counts, "executed": executed, "percent": percent}, ensure_ascii=False)
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    text = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>Regresión Corte 3 · WAN Architect</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#edf2f7;color:#183047;font:14px/1.4 system-ui,sans-serif}}
main{{max-width:1400px;margin:auto;padding:30px}}header{{background:#132b43;color:white;border-radius:12px;padding:24px}}
h1{{margin:0 0 8px;font-size:29px}}.score{{font-size:38px;font-weight:800;color:#88e5c2}}.details{{font-size:12px;word-break:break-word}}
.counts{{padding:14px 0;font-weight:700}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{text-align:left;border:1px solid #d5dfe8;padding:10px;vertical-align:top}}th{{background:#dce8f2}}td:first-child{{width:55px}}td:last-child{{width:115px;font-size:12px;font-weight:800}}small{{display:block;color:#50677a;font-size:12px;margin-top:4px}}.superada{{color:#08744f}}.fallida,.bloqueada{{color:#a92626}}footer{{padding:15px;background:#fff7dd;border-radius:8px;margin-top:16px}}</style>
<main><header><h1>WAN Architect · Regresión automatizada Corte 3</h1><div>{status} · Python / Playwright · HTTP local</div>{warning}
<div class="score">{score}</div><div class="details">{escape(environment['date'])} · {escape(environment['python'])} · Playwright {escape(environment['playwright'])} · Chromium {escape(environment['browser'])}<br>
Commit: {escape(environment['commit'])}<br>SHA-256 WAN_v4.html: {environment['application_sha256']}<br>Suite SHA-256: {environment['suite_sha256']} · Duración: {elapsed:.1f} s</div></header>
<div class="counts">Superadas: {counts['superada']} · Fallidas: {counts['fallida']} · Bloqueadas: {counts['bloqueada']} · No ejecutadas: {counts['no ejecutada']} · Total definido: {len(records)}</div>
<table><thead><tr><th>Caso</th><th>Prueba / esperado</th><th>Obtenido / evidencia observable</th><th>Estado</th></tr></thead><tbody>{rows}</tbody></table>
<footer>Porcentaje = superadas / ejecutadas × 100. Cada caso usa un contexto limpio. Validación local y textual: no se ejecuta CLI, no se demuestra conectividad ni compatibilidad física. Los cuatro generadores siguen siendo IPv4; IPv6 se calcula y planifica.</footer></main>
<script id="results" type="application/json">{data}</script></html>"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", type=Path, help="HTML de resultados; por defecto, fuera del repositorio")
    parser.add_argument("--capture", type=Path, help="PNG real del reporte; solo se escribe si se solicita")
    parser.add_argument("--browser", type=Path, help="Ejecutable Chromium alternativo (también CHROMIUM_EXECUTABLE)")
    args = parser.parse_args()
    report = args.report.resolve() if args.report else Path(tempfile.mkdtemp(prefix="wan-corte3-")) / "reporte.html"
    targets = {report, *([args.capture.resolve()] if args.capture else [])}
    if targets & {APPLICATION.resolve(), FIXTURE.resolve(), Path(__file__).resolve()}:
        parser.error("El reporte/captura no puede sobrescribir aplicación, fixture o runner.")
    if args.capture and report == args.capture.resolve():
        parser.error("HTML y PNG requieren rutas distintas.")
    if not APPLICATION.is_file() or not FIXTURE.is_file():
        parser.error("Falta WAN_v4.html o tests/fixtures/laboratorio-v2.json; ejecute desde un checkout completo.")
    initial_hash = hashlib.sha256(APPLICATION.read_bytes()).hexdigest()
    try:
        date = datetime.now(ZoneInfo("America/Bogota")).isoformat(timespec="seconds")
    except ZoneInfoNotFoundError:
        date = datetime.now(timezone.utc).isoformat(timespec="seconds") + " (UTC; zona Bogotá no instalada)"
    environment = {"date": date, "commit": git_value("rev-parse", "HEAD"),
                   "branch": git_value("branch", "--show-current"), "python": platform.python_version(),
                   "os": platform.platform(), "playwright": "no disponible", "browser": "no disponible",
                   "application_sha256": initial_hash, "suite_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest()}
    records = []
    started = time.perf_counter()
    server = None
    server_thread = None
    fatal = None
    print("WAN Architect · Regresión Corte 3 · contexto limpio por caso", flush=True)
    try:
        from playwright.sync_api import sync_playwright
        environment["playwright"] = importlib.metadata.version("playwright")
        with sync_playwright() as playwright:
            # Preferir Chromium de Playwright instalado/documentado. En entornos
            # que ya proporcionan Chromium, permitirlo sin reinstalar paquetes.
            configured = str(args.browser) if args.browser else os.environ.get("CHROMIUM_EXECUTABLE")
            bundled = Path(playwright.chromium.executable_path)
            executable = configured or (str(bundled) if bundled.is_file() else shutil.which("chromium") or shutil.which("chromium-browser"))
            if not executable:
                raise RuntimeError("Falta Chromium. Ejecute: python -m playwright install chromium")
            with playwright.chromium.launch(executable_path=executable, headless=True) as browser:
                environment["browser"] = browser.version
                environment["browser_executable"] = executable
                server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
                server_thread = Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                url = f"http://127.0.0.1:{server.server_port}/WAN_v4.html"
                environment["server_origin"] = url.rsplit("/", 1)[0]
                for identifier, name, expected, function in CASES:
                    beginning = time.perf_counter()
                    lab = None
                    try:
                        lab = Lab(browser, url)
                        actual = function(lab)
                        check(not lab.errors, "Errores JavaScript/consola: " + repr(lab.errors))
                        check(not lab.external, "La app intentó solicitudes externas: " + repr(lab.external))
                        state = "superada"
                    except Exception as error:
                        state = "fallida"
                        actual = f"{type(error).__name__}: {error}"
                        print(traceback.format_exc(limit=3), file=sys.stderr, flush=True)
                    finally:
                        if lab is not None:
                            lab.close()
                    record = {"id": identifier, "name": name, "expected": expected, "actual": actual,
                              "state": state, "seconds": time.perf_counter() - beginning}
                    records.append(record)
                    print(f"{identifier} {state.upper()}: {name} — {actual}", flush=True)
                elapsed = time.perf_counter() - started
                write_report(report, records, environment, elapsed)
                if args.capture:
                    args.capture.parent.mkdir(parents=True, exist_ok=True)
                    with browser.new_context(viewport={"width": 1400, "height": 1000}, device_scale_factor=1) as context:
                        page = context.new_page()
                        # Renderizar exactamente el HTML generado: funciona también
                        # donde la política de Chromium bloquea navegación file://.
                        page.set_content(report.read_text(encoding="utf-8"), wait_until="load")
                        page.screenshot(path=str(args.capture.resolve()), full_page=True, animations="disabled")
    except Exception as error:
        fatal = f"{type(error).__name__}: {error}"
        print("BLOQUEO/ERROR DE ENTORNO O ARTEFACTO: " + fatal, file=sys.stderr, flush=True)
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
    completed = {record["id"] for record in records}
    for identifier, name, expected, _function in CASES:
        if identifier not in completed:
            print(f"{identifier} {'BLOQUEADA' if fatal else 'NO EJECUTADA'}: {name} — {fatal or 'No se llegó a ejecutar'}", flush=True)
            records.append({"id": identifier, "name": name, "expected": expected,
                            "actual": fatal or "No se llegó a ejecutar", "state": "bloqueada" if fatal else "no ejecutada", "seconds": 0})
    if hashlib.sha256(APPLICATION.read_bytes()).hexdigest() != initial_hash:
        fatal = "WAN_v4.html cambió durante la ejecución; evidencia inválida."
    elapsed = time.perf_counter() - started
    if fatal:
        environment["fatal_error"] = fatal
        write_report(report, records, environment, elapsed)
    counts, executed, percent = summary(records)
    score = f"{counts['superada']}/{executed} = {percent:.2f}%" if percent is not None else "0/0 = no calculable"
    print(f"\nResultado: {score}; fallidas={counts['fallida']}; bloqueadas={counts['bloqueada']}; no ejecutadas={counts['no ejecutada']}")
    print(f"Tiempo: {elapsed:.1f} s · Reporte HTML: {report}")
    if args.capture and not fatal:
        print(f"Captura real: {args.capture.resolve()}")
    return 0 if not fatal and counts["superada"] == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
