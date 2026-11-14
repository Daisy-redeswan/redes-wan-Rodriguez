# Catálogo local de modelos e interfaces

Verificación documental: **14 de noviembre de 2026**. Base de código: `6466c9494cefdb5423d95e1bc04175304a4e248d`. No se conectaron equipos ni se ejecutó CLI; «verificado» significa contrastado con documentación oficial, no certificación física, de firmware o de licencias.

## Uso y distribución sin internet

1. Abra `WAN_v4.html` conservando junto al HTML la carpeta `data/`. La ejecución se verificó mediante HTTP local y el servicio SSH opcional; la apertura file:// está diseñada sin fetch, pero su prueba fue bloqueada por política del navegador de este entorno.
2. En Topología, abra **Editar fabricante y equipo**, elija fabricante y modelo filtrado por tipo, y confirme el equipo. En las vistas de configuración puede seleccionar directamente el modelo del fabricante actual.
3. La vista previa muestra nombres, medio, velocidades documentadas, restricciones y fuentes. Los enlaces reciben puertos automáticamente; no se escriben modelo, versión, URL ni cada puerto en un formulario obligatorio.
4. Revise la asignación por enlace y genere la propuesta. Si falta capacidad, compatibilidad de medio/velocidad o respaldo para una función activa, se muestra un error específico; no se añaden puertos ficticios ni se guarda una transacción parcial.

La aplicación lee **solo datos locales**: [JSON canónico](../data/catalogo-interfaces.json) y [script de datos empaquetado](../data/catalogo-interfaces.js). El script permite carga clásica también desde `file://`, sin `fetch`, CORS ni scraping. `python tools/build_catalogo.py` regenera el script tras editar el JSON; `python tools/build_catalogo.py --check` detecta diferencias. No requiere paquetes nuevos. Distribuir únicamente el HTML pierde el catálogo: el modo genérico heredado continúa con advertencia, pero un proyecto que declara un modelo desconocido se rechaza en vez de degradarlo silenciosamente.

## Modelos exactos incluidos

Las velocidades indicadas no prueban negociación física. No se incluyen módulos opcionales, puertos de consola, gestión fuera de banda ni variantes no identificadas.

| Fabricante / modelo y variante | Rol admitido por el adaptador | Sistema / referencia | Interfaces incluidas y capacidad | Asignación / límites |
| --- | --- | --- | --- | --- |
| Cisco C9200L-24T-4G | Switch L2 o capa 3 | IOS XE 17.11.x, Network Advantage como supuesto declarado; miembro 1 independiente | 24 RJ45 GE `GigabitEthernet1/0/1…24`; 4 SFP 1G `GigabitEthernet1/1/1…4` | 28 puertos; sin PoE en variante T; sin stack ni módulos |
| Cisco C9200L-48T-4G | Switch L2 o capa 3 | Igual referencia, variante 48T explícita | 48 RJ45 GE `GigabitEthernet1/0/1…48`; 4 SFP 1G `GigabitEthernet1/1/1…4` | 52 puertos; mismas reservas y límites |
| Cisco ISR4321/K9 | Router | IOS XE 16.3.1 de ejemplo oficial | `GigabitEthernet0/0/0` combo RJ45/SFP y `GigabitEthernet0/0/1` RJ45; GE | Dos interfaces lógicas, no tres conectores independientes. Perfil usa cobre; solo routed, sin NIM/ROAS |
| Huawei S5700-28P-LI-AC | Switch L2 | VRP V200 independiente, slot/subcard 0 | Banco RJ45 GE `GigabitEthernet0/0/1…24` | Inventario parcial: cuatro SFP físicos documentados excluidos hasta verificar nombres CLI inequívocos de la variante |
| Huawei S5700-28P-LI-DC | Switch L2 | Igual familia, variante DC explícita | Banco RJ45 GE `GigabitEthernet0/0/1…24` | Mismo límite parcial; no se extrapola a -X/-24S/otras variantes |
| Huawei S5700-52P-LI-AC | Switch L2 | VRP V200 independiente | Banco RJ45 GE `GigabitEthernet0/0/1…48` | Cuatro SFP excluidos por la misma falta de evidencia CLI; no se ofrece como core L3 |
| Fortinet FortiGate 60F | Firewall | FortiOS 7.4.x, sin multi-VDOM | Diez GE: `wan1`, `wan2`, `dmz`, `internal1…5`, `a`, `b` | Solo tres asignables: wan1/wan2/dmz; no se desmontan switch interno ni FortiLink |
| Fortinet FortiGate 61F | Firewall | Igual referencia, variante 61F identificada | Mismos diez nombres confirmados en tabla oficial 60F/61F | Mismas reservas; no inferir otros modelos |
| Fortinet FortiGate 70F | Firewall | FortiOS 7.4.x, sin multi-VDOM | Diez GE con los nombres de su tabla oficial 70F/71F | Se incluye únicamente 70F; tres asignables, resto reservado |
| MikroTik RB750Gr3 (hEX) | Router | RouterOS 7.x, sin VRF/CAPsMAN | Cinco GE `ether1…5` | Nombres de fábrica; no detecta renombrados ni configuración previa |
| MikroTik RB760iGS (hEX S) | Router | RouterOS 7.x | Cinco GE `ether1…5`, un SFP 1G `sfp1` | Variante RB760iGS; no el hEX S de 2025 |
| MikroTik CCR2004-16G-2S+ | Router | RouterOS 7.x | 16 GE `ether1…16`, dos SFP+ `sfp-sfpplus1…2` de 1/10G | No se extrapola a variante PC; transceptores y cables requieren revisión |

## Fuentes oficiales y alcance de la comprobación

Cada ficha JSON conserva URL, fecha y evidencia específica. Las referencias que sustentan los datos anteriores son:

- [Cisco · C9200L-24T-4G y -48T-4G: puertos de acceso GE y cuatro uplinks SFP GE fijos.](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/hardware/install/b-c9200-hig/product_overview.html)
- [Cisco · Standalone 1; downlinks módulo 0, uplinks módulo 1; nombres y switching/routed de IOS XE.](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/software/release/17-11/configuration_guide/int_hw/b_1711_int_and_hw_9200_cg/configuring_interface_characteristics.html)
- [Cisco · DHCP, relay y HSRP; verificar licencia/versión antes de aplicar.](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/software/release/17-11/configuration_guide/ip/b_1711_ip_9200_cg.html)
- [Cisco · Familia de comandos IPv4/OSPF; referencia con Network Advantage.](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/software/release/17-11/configuration_guide/rtng/b_1711_rtng_9200_cg.pdf)
- [Cisco · ISR4321: dos interfaces GE integradas; un conector SFP comparte interfaz con cobre, no añade un tercer enlace.](https://www.cisco.com/c/en/us/products/collateral/routers/4000-series-integrated-services-routers-isr/data_sheet-c78-732542.html)
- [Cisco · ISR4321 / IOS XE 16.3.1: GigabitEthernet0/0/0 y GigabitEthernet0/0/1.](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/interoperability-portal/fusion-connect-sip-trunking.pdf)
- [Cisco · ISR4321: GE0/0/0 RJ45 y SFP comparten nombre y capacidad; GE0/0/1 es cobre dedicado. Perfil conservador usa el combo por cobre.](https://www.cisco.com/c/ja_jp/td/docs/rt/branchrt/4451-xisr/ig/001/c4400-isr/overview.html)
- [Huawei · S5700-28P-LI AC/DC: 24 RJ45 GE y cuatro SFP; S5700-52P-LI AC: 48 RJ45 GE y cuatro SFP. VLAN/MSTP/SSH; LI sin OSPF avanzado.](https://enterprise.huawei.com/nla/products/network/switch/campus-switch/hw-143233.htm)
- [Huawei · Ficha oficial S5700-LI: inventario y separación de variantes AC/DC; familia VRP. No extrapolar a variantes -X o -24S.](https://enterprise.huawei.com/ucmf/groups/public/documents/enterprise_webasset/hw_331882.pdf)
- [Huawei · Nomenclatura GigabitEthernet0/0/N y MSTP de S5700 standalone. Solo se incorpora el banco RJ45; los SFP quedan fuera hasta completar evidencia de nombres.](https://info.support.huawei.com/network/ptmngsys/Web/tsrev_s/en/content/s/16_edesk_stp_failure/edesk_stp_failure_edesk003.html)
- [Fortinet · Tabla diagnose npu: wan1, wan2, dmz, internal1..5, a, b; diez puertos GE. a/b FortiLink se excluyen de asignación.](https://docs.fortinet.com/document/fortigate/7.4.0/hardware-acceleration/758378/fortigate-60f-and-61f-fast-path-architecture)
- [Fortinet · Familia FortiOS 7.4: IPv4/VLAN/relay. Requiere interfaces libres de referencias/configuración previa; no se eliminan switches ni FortiLink automáticamente.](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/8620/config-system-interface)
- [Fortinet · Tabla oficial para 70F/71F: wan1, wan2, dmz, internal1..5, a, b, todos GE.](https://docs.fortinet.com/document/fortigate/7.4.0/hardware-acceleration/749156/fortigate-70f-and-71f-fast-path-architecture)
- [MikroTik · RB750Gr3: cinco puertos Ethernet Gigabit.](https://mikrotik.com/product/RB750Gr3)
- [MikroTik · Tabla de modelos/nombres: RB750Gr3 ether1..5; RB760iGS ether1..5 y sfp1; CCR2004-16G-2S+ ether1..16 y sfp-sfpplus1..2.](https://help.mikrotik.com/docs/spaces/ROS/pages/21725296/MTU%20in%20RouterOS)
- [MikroTik · Sintaxis RouterOS 7. El adaptador conserva sus restricciones: sin VRRP, LACP, VRF ni CAPsMAN.](https://help.mikrotik.com/docs/spaces/ROS/pages/331612216/routing+ospf)
- [MikroTik · RB760iGS: cinco puertos Ethernet Gigabit y un SFP 1G; no confundir con hEX S 2025.](https://mikrotik.com/product/hex_s)
- [MikroTik · CCR2004-16G-2S+: dieciséis RJ45 GE y dos SFP+ 10G; no variante PC.](https://help.mikrotik.com/docs/spaces/UM/pages/78086248/CCR2004-16G-2S)
- [MikroTik · CCR2004-16G-2S+: los SFP+ pueden trabajar a 1G con óptica apropiada; transceptor no descubierto por la app.](https://help.mikrotik.com/docs/spaces/ROS/pages/220233794/MikroTik%20wired%20interface%20compatibility)

Las páginas completas Fortinet pueden devolver 403 en este entorno; se contrastaron los nombres con las tablas visibles en el índice oficial y sus referencias de hardware/CLI, sin afirmar inspección física ni acceso completo a páginas denegadas. Huawei ofrece un inventario deliberadamente parcial: se verificó el banco RJ45 y la nomenclatura de su familia; no se publican nombres CLI de los cuatro SFP sin prueba inequívoca por variante. Una familia/versión de referencia no certifica todas las combinaciones de comandos.

## Resolución determinista y conservación de enlaces

`assignCatalogInterfaces()` trabaja con una copia del grafo, conserva asignaciones anteriores válidas y únicas, y procesa primero los enlaces con menos alternativas; desempata por clave estable. Filtra puertos por tipo routed/trunk/access, medio y velocidad común. Prefiere WAN, LAN o uplink según el enlace; gestión procede de VLAN/SVI y dirección del plan, sin inventar un puerto OOB. Hacia un equipo sin modelo solo presupone cobre para no inventar ópticas. Hacia dos modelos puede usar fibra únicamente si los dos inventarios comparten medio y velocidad. Esto no garantiza disponibilidad/compatibilidad de transceptores, fibra, dúplex, alimentación o negociación en equipos reales.

La búsqueda retrocede por clases de puertos equivalentes y tiene un límite explícito de complejidad. Un fallo no modifica estado, planes, configuraciones, almacenamiento ni formulario. No se asigna una interfaz física a dos enlaces; regenerar conserva modelos/IDs y los puertos que siguen válidos. Una selección distinta no puede aumentar físicamente la capacidad del hardware.

`requireCatalogReady()` bloquea una función activa no respaldada por el perfil. Huawei LI se limita a switching L2, sin atribuirle OSPF/VRRP/LACP/DHCP del adaptador; Fortinet conserva sus límites HA/LACP/multi-VDOM y MikroTik los de RouterOS/Router. Los generadores usan los nombres nativos de los enlaces sin mezclar sintaxis. Comparación puede producir una propuesta alternativa genérica, explícitamente advertida como equivalencia lógica, no como segundo modelo certificado.

## JSON, proyectos anteriores, AP y seguridad

Extensión **opcional de v4**: `nodes[].modelId` referencia un ID cerrado del catálogo. Las interfaces efectivas siguen en `links[].ac/bc/ah/bh/af/bf/am/bm`. No cambia `state.version`, migración v2/v3, claves locales, redes, gateway ni plan IPv6. Un proyecto sin modelo conserva la generación anterior y muestra: «Modelo no especificado. Los nombres de interfaces son genéricos y deben verificarse antes de aplicar la configuración». Importar un proyecto con modelo valida fabricante/tipo, puerto existente/asignable, unicidad y enlace compatible; rechaza errores atómicamente, sin reasignar redes ni puertos durante carga.

Los perfiles físicos históricos se preservan como metadatos; un modelo seleccionado gobierna la propuesta nueva. Los AP continúan en inventario, topología, VLAN/IP/gestión y enlaces, pero no se ofrecen modelos ni CLI genérica de AP. Ninguna selección ejecuta configuraciones ni activa una conexión SSH.

## Ampliar el catálogo

Añada una ficha exacta con ID único, variante, tipos admitidos, OS/versión de referencia, fecha, fuentes oficiales y puertos documentados. Cada puerto declara nombre CLI, conector, medio, velocidades, tipos de enlace, prioridad, si es asignable y su reserva. `features` es una lista cerrada de capacidades conservadoras del adaptador; falso significa «no respaldado por este perfil», no necesariamente ausencia en hardware. Añada una ficha de contraste independiente a `tests/fixtures/catalogo-verificado.json`, regenere el script y ejecute las pruebas. No active funciones solo por existir un puerto: revise la sintaxis de la plataforma y licencias; un nuevo SO fuera de los cuatro adaptadores requiere desarrollo explícito.

No hay compatibilidad física certificada para ningún modelo. Permanecen fuera de alcance IPv6 CLI, pools/reservas manuales, descubrimiento remoto, módulos, ópticas y configuración existente. Véanse [pruebas](pruebas.md) y [matriz de fabricantes](matriz-fabricantes.md).
