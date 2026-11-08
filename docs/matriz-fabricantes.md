# Matriz de fabricantes de WAN Architect

## Alcance y fuentes

Base inspeccionada: `6f45dc1e54051a2467241ee50f59fa18906cf23c`, [WAN_v4.html](../WAN_v4.html), especialmente `configNodes`, `assertReady`, `generate`, `endpoint`, `trunkCommands`, `topologyIssues` y `validateImport`.

Requisitos oficiales: [Guía Docente.html](<requisitos/Guía Docente.html>), «Marcas que debe soportar» y rúbrica Corte 3. Criterios de arquitectura: [Arquitectura_Agente_WAN_Architect.docx](requisitos/Arquitectura_Agente_WAN_Architect.docx). Antecedentes: [README.md](../README.md), [Correcciones Pendientes.txt](<requisitos/Correcciones Pendientes.txt>) e [Instrucciones de Código.txt](<requisitos/Instrucciones de Código.txt>).

**No hay modelos de dispositivo ni versiones objetivo confirmados o validados en laboratorio para ninguna marca.** Los nombres de sistemas siguientes identifican familias, no una certificación de compatibilidad. No se ejecutaron comandos en equipos ni simuladores. Las referencias técnicas enlazadas en el HTML son material de consulta; no demuestran compatibilidad de todas sus salidas.

## Capacidades y dependencias

| Fabricante | Funcionalidades requeridas por guía | Implementado por inspección | Configuraciones generadas por código | Dependencias VLAN/direccionamiento/topología | Modelo y versión objetivo |
| --- | --- | --- | --- | --- | --- |
| Cisco IOS / IOS XE | Para Cisco IOS: VLAN, direccionamiento, enrutamiento básico y acceso. El código también anuncia IOS XE | Adaptador dentro de `generate`, selección por fabricante y comparación; routers, switches y switches capa 3 | Hostname, acceso SSH/ACL administrativa, VLAN, access/trunk, SVI, enlaces enrutados, OSPF, DHCP local o relay, ruta estática opcional, HSRP, LACP/Port-channel y STP según tipo/opciones; cierre `end` y `write memory` | Plan confirmado, VLAN por sede, redes /30, interfaces `ac`/`bc`, IP de gestión, enlaces y redundancia; gateways y reservas alimentan SVI/DHCP | Sin confirmar. IOS e IOS XE no son intercambiables de forma universal |
| Huawei VRP | Equivalencia de las funciones base en sintaxis VRP | Rama Huawei de `generate`, selección de nodos y alternativa de equivalencias si no hay Huawei; Comparación | `system-view`, `sysname`, STelnet/AAA/ACL, VLAN, access/trunk, Vlanif, interfaces enrutadas, OSPF, DHCP global o relay, ruta estática, VRRP, Eth-Trunk/LACP y MSTP según opciones; cierre `return` y `save` | Mismo plan por sede, interfaces `ah`/`bh`, enlaces, IP físicas/virtuales y tipos de equipo. La comparación no cambia el fabricante almacenado | Sin confirmar. No se conoce familia/modelo ni versión VRP |
| Fortinet FortiOS | Interfaces, políticas y direccionamiento del firewall; cuatro marcas completas para Corte 3 | Pendiente: sin módulo ni adaptador FortiOS. El tipo de nodo Firewall no implica generador implementado | Ninguna salida FortiOS soportada | Adaptador futuro debe tomar subredes, VLAN, enlaces, interfaces/zonas y reglas de política definidas; la topología actual se centra en switching/enrutamiento | Sin confirmar. Políticas, zonas, VDOM o NAT deben definirse si el alcance los necesita; no se asumen como implementados |
| MikroTik RouterOS | Direcciones, rutas y servicios; cuarta marca seleccionada por el curso | Pendiente: sin módulo ni adaptador RouterOS | Ninguna salida RouterOS soportada | Adaptador futuro necesita asignación explícita de interfaces, subredes, gateways/rutas y servicios; puente/VLAN filtering solo si el diseño aprobado lo requiere | Sin confirmar. No se selecciona RouterOS v6/v7 ni modelo por defecto |

Las funcionalidades avanzadas presentes en el código no son todas requisitos expresos de la guía por fabricante. Su existencia no equivale a validación. El generador recibe opciones comunes; no todos los comandos se emiten para cada equipo o combinación.

## Validaciones, riesgos y pruebas necesarias

La evidencia P5 de esta tabla se repitió el 7 de noviembre de 2026 (America/Bogota) contra el mismo `WAN_v4.html` de la base indicada. Solo comprueba generación de texto en Comparación; mantiene pendientes las pruebas por plataforma y versión.

| Fabricante | Evidencia real disponible en esta tarea | Validaciones pendientes | Riesgos de compatibilidad | Pruebas necesarias antes de declarar soporte |
| --- | --- | --- | --- | --- |
| Cisco IOS / IOS XE | P5: Comparación del primer equipo del laboratorio produjo texto con `hostname`. No se probó toda la salida ni todos los equipos | Validar comandos contra documentación oficial del modelo/OS, modos y capacidades de interfaces; comprobar seguridad, DHCP/relay, OSPF y redundancia | Router frente a switch L2/L3; nombres de interfaces; soporte de `no switchport`, HSRP, RSA, STP y comandos de guardado; usuario propuesto de privilegio 1 puede requerir un procedimiento externo de autorización | Casos de router, L2 y L3; comparar VLAN/IP/rutas con plan; sin/ con redundancia; DHCP y relay; LACP con enlaces completos; revisar CLI y comportamiento en laboratorio autorizado por tarea separada |
| Huawei VRP | P5: mismo equipo en Comparación produjo texto con `sysname`. No certifica selección del módulo Huawei ni comandos restantes | Confirmar soporte por modelo de STelnet/AAA, contraseña cifrada, Vlanif, `undo portswitch`, DHCP, OSPF, VRRP y Eth-Trunk; verificar prompts interactivos | Diferencias VRP/modelo y puertos L2/L3; equivalencia de una topología Cisco no asegura hardware Huawei equivalente; `irreversible-cipher` y generación de claves requieren revisión de versión | Casos Huawei nativos y topología automática sin Huawei; selección alternativa y mezcla de marcas; comparación de IP/VLAN con Cisco; pruebas de cada tipo de equipo y revisión de prompts en laboratorio |
| Fortinet FortiOS | Ninguna; pendiente de implementación | Definir modelo/versión, puertos, VLAN, zonas, direccionamiento y política mínima; diseñar salidas sin secretos. NAT o rutas adicionales según requisitos aceptados | Referencias a interfaces y políticas sin correspondencia; orden/identificadores de políticas; servicios demasiado amplios; diferencias de versión y VDOM si aplica | Casos normales e inválidos para interfaces/IP/políticas; comprobar referencias y mínimo privilegio; pruebas de salida determinista y revisión por versión; captura real 06 al existir generador |
| MikroTik RouterOS | Ninguna; pendiente de implementación | Definir modelo/versión, direccionamiento, rutas y servicios; decidir diseño de bridge/VLAN si corresponde | Sintaxis y valores por defecto v6/v7, nombres de interfaces, VLAN filtering y servicios administrativos; mezclar gramáticas de fabricantes | Casos de direcciones/rutas/servicios, next-hop inválido y servicios innecesarios; salida coherente con topología; pruebas por versión; captura real 07 al existir generador |

## Reglas compartidas para futuras implementaciones

1. Confirmar plataforma exacta, versión, funciones admitidas y nombres de interfaces antes de afirmar compatibilidad. Registrar fuente oficial y resultados de laboratorio; si faltan, mantener estado pendiente o bloqueado.
2. Mantener un plan coherente: VLAN por sede, gateway dentro de subred, ausencia de solapamientos, reserva de IP físicas/virtuales y enlaces enrutados completos. `assertReady` y `topologyIssues` bloquean incoherencias por inspección, pero cada rama de validación necesita pruebas.
3. Respetar dependencias actuales: OSPF requiere interfaces; DHCP requiere gateways/interfaces; switching con interfaces requiere VLAN. DHCP local y relay tienen validaciones de opciones. Probar combinaciones antes de cambiar controles.
4. Capturar salidas Cisco/Huawei y exportaciones v2 de referencia antes de añadir adaptadores. El importador actual limita `vendor` a Cisco/Huawei; añadir nombres requiere una decisión de compatibilidad/migración y autorización de código, no solo nuevos botones.
5. Mantener sintaxis y capacidades separadas. Actualmente `generate` bifurca entre Cisco y el camino Huawei; pasar un nombre nuevo a esa función no implementa otra marca y puede producir sintaxis equivocada.
6. Mantener marcadores `<CAMBIAR_EN_PRODUCCION>`; no guardar contraseñas ni tokens reales. Los prompts de generación de claves y guardado se atienden fuera de la herramienta. Nunca ejecutar automáticamente las propuestas.
7. Probar bloqueos: equipo sin plan/enlaces, VLAN ausente, IP duplicada/fuera de red, grupo LACP incompleto y cores redundantes incompatibles. HSRP/VRRP no se interoperan entre sí; DHCP del core primario no proporciona replicación de concesiones.
8. No equiparar ACL administrativa a aislamiento entre servicios, ni enlace WAN a VPN/cifrado. Una política de firewall futura debe derivarse de requisitos explícitos, no inventarse desde un diagrama.

## Plan de pruebas y entrega

P5 documentado en [estado-proyecto.md](estado-proyecto.md) es una prueba de humo de generación de texto; no valida forwarding, seguridad efectiva, convergencia, gramática completa ni compatibilidad de hardware. Las capturas históricas 03/04 existen pero no fueron auditadas como evidencia de esta revisión.

Para cada plataforma futura registrar: identificador de caso, commit, modelo/OS/versión, datos ficticios, opciones, salida esperada y obtenida, fuente técnica, resultado y evidencia. Separar pruebas unitarias de formato, pruebas de coherencia del plan y pruebas de integración en laboratorio. En esta tarea no se autorizó aplicar configuraciones de red.

Orden recomendado: fijar plataformas y salidas base → resolver conservación de estado y pruebas v2 → diseñar adaptadores nuevos con casos de aceptación → implementar y revisar por fabricante → ejecutar regresión Cisco/Huawei y persistencia → generar evidencia real de Corte 3. La documentación de resultados debe mantenerse en `docs/pruebas.md` cuando una tarea posterior autorice crearlo; ver [trazabilidad-corte3.md](trazabilidad-corte3.md).
