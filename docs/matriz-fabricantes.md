# Matriz de fabricantes · entrega auditada

Fecha 2026-11-15; main `1b46af32c8217a1f9bcea686151b1f070ac38352`. Fuentes y doce fichas: [catálogo oficial local](catalogo-modelos.md). Validación **documental/textual**, no física. Guía: Cisco IOS, Huawei VRP, Fortinet FortiOS y MikroTik RouterOS; no obliga a inventar soporte de todos los roles o modelos.

| Fabricante | Modelo del laboratorio / referencia | Funciones implementadas según rol/opciones | Dependencias y límites | Evidencia actual |
| --- | --- | --- | --- | --- |
| Cisco IOS/IOS XE | C9200L-24T-4G, IOS XE 17.11.x y licencia declarada en ficha | Hostname, VLAN, trunks/access, SVI IPv4, OSPF, DHCP/relay, rutas, HSRP/SSH según rol y capacidades | Core L3, VLAN/plan/interfaces reales; revisar licencia/versión, ópticas y prompts; no generar CLI AP | 03; C12/C26/K/F/L en reporte UI |
| Huawei VRP | S5700-28P-LI-AC, VRP V200 | Sysname, VLAN, trunks/access, Vlanif de Gestión, ruta administrativa, STelnet; el adaptador genérico admite otras funciones solo en perfiles compatibles | LI es L2: no atribuirle OSPF/VRRP/LACP/DHCP del adaptador; RJ45 verificados, SFP excluidos | 04; C13/C26/K/F/L |
| Fortinet FortiOS | FortiGate 60F / FortiOS 7.4.x, sin multi-VDOM | Hostname, interfaces físicas/VLAN e IP, objetos, DHCP/relay si procede, rutas/OSPF, administración limitada y políticas no permisivas implícitas | Solo Firewall; no HA/LACP; tres puertos asignables, switch interno/FortiLink reservados; no NAT/Internet inventados | 06; C14/K/F/L |
| MikroTik RouterOS | RB750Gr3 hEX / RouterOS 7.x | Identidad, puertos, bridge/VLAN si hay LAN, IPv4, rutas/OSPF v7, DHCP/relay si procede, servicios/SSH restringidos | Solo Router; sin VRF/CAPsMAN/VRRP/LACP; puertos/objetos existentes exigen revisión; forward bloqueado sin intención explícita | 07; C15/K/F/L |

En el laboratorio público Cisco termina las VLAN y gateways; Huawei aporta acceso L2 y Gestión, Fortinet y MikroTik usan tránsitos del plan. No se duplican gateways para forzar funciones. Una función no pertinente al rol se omite o bloquea, en vez de inventar comandos. Comparación muestra extractos nativos para cinco funciones; ausencia de equipo compatible se explica. La equivalencia adicional IOS/VRP es lógica, no cambio de fabricante real.

Los módulos de configuración leen modelos guardados en Topología y tabla física de siete columnas. Modelos sin seleccionar conservan Modo genérico con aviso; AP permanece en inventario/topología/gestión y enlaces sin CLI genérica. Interfaces exactas proceden del catálogo y enlaces; los modelos, firmware y puertos renombrados requieren contraste físico.

## Contrato y pruebas

Los cuatro consumen estado v4: IPv4/VLSM automático y mixto, bloques privados independientes por sede y tránsito, gateways y opciones comunes. JSON v2/v3 migra sin reasignar; localStorage v4 prioriza y hace fallback no destructivo. IPv6 ULA mantiene plan separado: **ningún generador emite CLI IPv6**; alcance de configuraciones IPv6 por aclarar con docente. No hay pools DHCP ni reservas manuales editables.

Resultado actual: **114/114 UI + 26/26 SSH loopback = 140/140**, sin repetir la suite en la auditoría. [Reportes y límites](pruebas.md). Las capturas 06/07 ya están generadas y revisadas; no siguen pendientes. Validación física, convergencia, tráfico, firmware/licencias y ópticas sí permanecen pendientes. SSH real opcional no constituye certificación de los cuatro fabricantes.

## Antecedentes conservados

Las pruebas 27/27 Fortinet, 30/30 MikroTik, 9/9 integrales y posteriores conjuntos de 31/50/73/99/122/135 son históricos y no se suman al 140 actual. La [matriz anterior completa](https://github.com/Daisy-redeswan/redes-wan-Rodriguez/blob/1b46af32c8217a1f9bcea686151b1f070ac38352/docs/matriz-fabricantes.md) conserva sus escenarios y fuentes por plataforma; sus menciones a capturas pendientes o modelos genéricos deben leerse en su fecha. [Documentación del código](documentacion-codigo.md), [manual SSH](manual-ssh.md) y [auditoría normativa](auditoria-entrega-final.md).
