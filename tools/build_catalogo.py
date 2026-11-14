#!/usr/bin/env python3
"""Empaqueta datos locales JSON para HTTP y file://; no consulta internet ni instala dependencias."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
def build(check=False):
    source=ROOT/'data/catalogo-interfaces.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    if data.get('schemaVersion')!=1 or not isinstance(data.get('models'),list):raise ValueError('Esquema de catálogo desconocido')
    ids=set()
    for model in data['models']:
        if model['id'] in ids:raise ValueError('Modelo duplicado')
        ids.add(model['id'])
        if model['vendor'] not in ['Cisco','Huawei','Fortinet','MikroTik']:raise ValueError('Fabricante desconocido')
        if len({p['name'] for p in model['ports']})!=len(model['ports']):raise ValueError('Puerto duplicado')
        if not model['sources'] or any(not s['url'].startswith('https://') for s in model['sources']):raise ValueError('Fuente oficial requerida')
    # Datos únicamente: los caracteres HTML se escapan para evitar cierres accidentales de script.
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    output='// Generado por python tools/build_catalogo.py; editar el JSON, no este archivo.\n'+'globalThis.WAN_INTERFACE_CATALOG = '+payload+';\n'
    dest=ROOT/'data/catalogo-interfaces.js'
    if check:
        if not dest.is_file() or dest.read_text(encoding='utf-8')!=output:raise ValueError('Catálogo JS desactualizado; ejecute python tools/build_catalogo.py')
    else:dest.write_text(output,encoding='utf-8')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();build(args.check)
    print('Catálogo local validado' if args.check else 'Catálogo local empaquetado')
