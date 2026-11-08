# Estado de WAN Architect

## Alcance y referencia

Repositorio: `https://github.com/Daisy-redeswan/redes-wan-Rodriguez`.
Rama actual: `feature/mikrotik-routeros`.
Código MikroTik inspeccionado y probado: `a31d6554c72b815c1d7b8a799a072d90d8ddac27`; base verificada de `origin/main`: `42b6167cbcd6b2a6a1992b99eaabb7ba377c9ca6`.
Auditoría MikroTik: 8 de noviembre de 2026, UTC; antecedentes Fortinet y direccionamiento conservados.
Antecedente: código Fortinet inspeccionado y probado: `5d87d76d3e78ded591220f75e2960f736fcf28ce`; base verificada de `origin/main`: `c33859758c717b1f777174183409dcdf5376aaab`.
Pruebas Fortinet y revisión crítica: 8 de noviembre de 2026, America/Bogota. La auditoría I1–I9 del PR #3 se conserva con su referencia histórica.
Antecedente P1–P6/R1: 7 de noviembre de 2026 sobre `6f45dc1e54051a2467241ee50f59fa18906cf23c`; se conserva como evidencia histórica.
Antecedente conservado: commit de documentación `ce35714047c1e86a4823f5513b2a76867c06a188`, publicado sobre la base histórica `6f45dc1e54051a2467241ee50f59fa18906cf23c`. Aquella revisión reutilizó su rama sin reescribir el historial y verificó el adjunto de `AGENTS.md`.

Objetivo general: apoyar el diseño y la gestión de redes WAN por sedes, calcular direccionamiento, representar dispositivos y enlaces y generar propuestas de configuración por fabricante, con ciberdefensa integrada y evidencia académica reproducible. La aplicación genera texto; no aplica configuraciones a dispositivos.

El commit documental actualiza únicamente los tres documentos de orientación autorizados, sin modificar el HTML ya incluido en el commit de código. Describe el contrato v3 integrado mediante PR #3 y los adaptadores Fortinet/MikroTik implementados en los commits indicados; no instala dependencias ni ejecuta configuraciones sobre redes. La guía docente define requisitos; el código define implementación; una inspección no demuestra funcionamiento.

## Fuentes y clasificación

- [Guía Docente.html](<requisitos/Guía Docente.html>): fuente principal de requisitos, rúbrica y nombres de entrega, versión visible v4.0.
- [WAN_v4.html](../WAN_v4.html): implementación inspeccionada y utilizada en las pruebas.
- [Arquitectura_Agente_WAN_Architect.docx](requisitos/Arquitectura_Agente_WAN_Architect.docx): diseño del agente y prioridades; sus pruebas propuestas no son resultados ejecutados.
- [Correcciones Pendientes.txt](<requisitos/Correcciones Pendientes.txt>): incidencias e instrucciones históricas.
- [Instrucciones de Código.txt](<requisitos/Instrucciones de Código.txt>): normalización y conservación del comportamiento.
- [README.md](../README.md): descripción pública; contiene nombres de entrada antiguos y un pendiente Huawei que debe contrastarse con el código actual.

Estados usados: **requisito oficial** (guía), **inspeccionado** (código existente), **probado** (caso ejecutado descrito), **pendiente** (trabajo o prueba no realizados), **bloqueado** (requiere una decisión o recurso) y **supuesto** (propuesta sin confirmar). No se asigna cumplimiento completo por mera existencia del código.

## Arquitectura actual

Aplicación autónoma en `WAN_v4.html`: HTML, CSS y JavaScript integrados; sin backend, base de datos ni dependencias externas de ejecución. No hay manifiesto de paquetes ni suite de pruebas o CI versionada en esta base.

`state = fresh()` centraliza proyecto, sedes, VLAN, plan, nodos, enlaces, opciones, configuraciones y revisión. `state.version` es 3. `render()` y `go()` presentan trece etapas, incluidas evidencias Corte 2 y las pantallas Fortinet/MikroTik. Los formularios editan valores visibles que se confirman mediante funciones específicas; el DOM y el estado confirmado pueden diferir.

La persistencia guarda en `WAN-Architect-v3`; `loadLocal()` busca primero esa clave y, si no existe, carga `WAN-Architect-v2` y migra en memoria sin eliminarla ni sobrescribirla. `exportJSON()` serializa `{ state, imageData }` en versión 3; `validateImport()` admite v2 mediante `migrateV2()` y valida v3 antes de `applyImport()`, rechazando versiones desconocidas. La migración conserva el plan, gateways, nodos, enlaces, configuraciones y opciones; no llama a `allocate()` ni infiere subredes manuales. Los archivos v3 no son compatibles con la aplicación antigua. Los datos permanecen en el navegador o archivos exportados. El JSON no es un mecanismo para ejecutar comandos.

| Módulo | Funciones de referencia | Confirmado por inspección |
| --- | --- | --- |
| Proyecto y estimación | `fresh`, `siteDefault`, `saveProject`, `saveSite`, `estimated`, `proposal` | Sedes, usuarios, inventario, crecimiento y redundancia |
| VLAN y VLSM | `proposeVlans`, `readVlans`, `allocate`, `confirmVlans`, `editGateway` | Segmentación por sede, bloque privado global, bloques opcionales por sede/tránsito, CIDR manual por VLAN, asignación automática o mixta, reservas y tránsitos /30 |
| Calculadora IPv4 | `ipNum`, `ipType`, `subnet`, `calculate` | CIDR, red, broadcast, máscara, hosts y clasificación de direcciones; no IPv6 |
| Topología | `buildTopology`, `editNode`, `editLink`, `validateLink`, `svgTopology` | Generación y edición de nodos/enlaces, ISP, VLAN, interfaces, imagen manual de referencia y exportación SVG |
| Fabricantes | `configNodes`, `assertReady`, `generate`, `generateFortinet`, `generateMikroTik`, `generateCompare` | Cisco/Huawei para routers y switches; Fortinet separado para nodos Firewall; MikroTik separado para nodos Router |
| Ciberdefensa | `esc`, `hostname`, `interfaceName`, `topologyIssues`, `securityWarnings` | Escape de textos, validación, advertencias y marcadores de secretos; no auditoría integral |
| Persistencia y entregas | `saveLocal`, `loadLocal`, `importJSON`, `exportJSON`, `downloadPlan`, `downloadReport` | Guardado, importación validada, exportación JSON, CSV y resumen HTML |

## Fortinet FortiOS: implementado y validado como texto

**Supuesto técnico autorizado:** FortiGate genérico de laboratorio, FortiOS 7.4, modo sin VDOM adicionales; no es un modelo físico verificado. Las VLAN usan el contexto interno `root` requerido por los ejemplos oficiales, sin crear dominios ni activar multi-VDOM.

`generateFortinet()` es un adaptador separado. `fortinetInterfaces()` consume VLAN, gateways, máscaras y extremos /30 reales; `fortinetPath()`/`fortinetRoute()` buscan caminos de la topología. Incluye hostname/criptografía, interfaces físicas y VLAN, HTTPS/SSH restringidos a Gestión con denegación local-in, objetos de direcciones, DHCP con exclusiones automáticas o relay, OSPF área 0 con LAN pasivas y rutas estáticas cuando OSPF está desactivado. Una ruta por defecto exige siguiente salto conectado y justificación explícitos. Las políticas de tránsito quedan marcadas para revisión; no se generan permisos activos ni NAT implícitos. Las cuentas y certificados se revisan externamente con marcadores, sin secretos reales.

Los formularios e importación admiten `vendor: Fortinet` únicamente para tipo Firewall. Los enlaces conservan `af`/`bf` opcionales para interfaces Fortinet, separados de `ac`/`bc` y `ah`/`bh`. La versión y claves de almacenamiento siguen en v3; F1/F3 comprueban selección, persistencia e ida/vuelta JSON con propuesta regenerada. El firewall deriva sus IP de interfaces del plan: IP/red del nodo deben quedar vacíos. Bloquea ausencia de plan/enlaces, interfaces inválidas/duplicadas, gateways ya usados por cores y HA no modelada. La generación confirma opciones y salidas juntas o conserva la propuesta previa.

**Pruebas ejecutadas:** F1–F18 (18/18) más regresión integral v3 I1–I9 (9/9): **27/27 superadas = 100% del conjunto ejecutado**, sin fallidas, bloqueadas ni no ejecutadas dentro de ese conjunto. Python/Playwright, Chromium 154.0.8037.57, HTTP local, contextos limpios y datos ficticios. Se verificaron administración/políticas no permisivas, DHCP/relay, direccionamiento/rutas/OSPF, rechazo de hostname/interfaz maliciosos, separación y estructura de CLI, importación/exportación, guardado y descarga conjunta. Se comprobó presentación a 1440/390 px y ausencia de errores de página/consola. El caso F4 del harness ajustó una coincidencia literal del mensaje de bloqueo; no fue un defecto funcional.

Antes de publicar se repitieron solo F1/F2/F3/F5/F6/F7/F8/F10/F12/F14/F15 e I1/I4/I8: **14/14 críticas superadas**, sin sumarlas como casos independientes al 27/27 histórico. Ambos conjuntos corresponden al SHA-256 `dca2f5ac15e9de848f50205e18ece204e6aef2247304d1203e81f46df3da30ff`. La comparación conserva exactamente las 28 salidas Cisco/Huawei de referencia y el cuerpo anterior del generador; no cambia el asignador v3. Evidencia temporal de sesión: `/workspace/work/wan-fortinet/verify.py`, `historical-fortinet-results.json`, `historical-integral-results.json` y resultados críticos. No hay suite versionada ni reporte académico nuevo.

**Límites y pendientes:** validación únicamente local/estática del texto; no se ejecutaron comandos en FortiGate ni simuladores y no se certifica compatibilidad física. Revisar puertos, objetos, IDs `edit 0`, adyacencias, rutas de retorno y configuración existente; las propuestas no son respaldos completos ni aplicaciones idempotentes. La captura oficial `docs/capturas/06-config-fortinet.png` sigue pendiente. Ese alcance Fortinet no incluyó MikroTik; su implementación actual se detalla a continuación. IPv6, HA/LACP Fortinet, pools DHCP y reservas editables siguen pendientes. Las fuentes oficiales consultadas están en la pantalla Fortinet y en [matriz-fabricantes.md](matriz-fabricantes.md).

## MikroTik RouterOS: implementado y validado como texto

**Supuesto autorizado:** router genérico de laboratorio, RouterOS 7.x, sin VRF, CAPsMAN ni compatibilidad física certificada. Código `a31d6554c72b815c1d7b8a799a072d90d8ddac27`, HTML SHA-256 `9e68b48741fda952252680bac415e9dd56d18a79e7ed897b2ca21b1c634afd09`. No se ejecutaron comandos RouterOS en equipos ni simuladores.

`generateMikroTik()` es un adaptador separado. `mikrotikInterfaces()` deriva puertos físicos `am`/`bm`, bridge con filtrado VLAN y CPU tagged, access/PVID, VLAN/IP/gateways y extremos /30 del plan/topología reales. `mikrotikRoute()` obtiene el primer salto de enlaces existentes; genera rutas LAN si OSPF está desactivado y default únicamente con siguiente salto/justificación explícitos. OSPF usa menús RouterOS 7, instancia IPv4 versión 2, área 0 y LAN pasivas. DHCP automático excluye gateway y endpoints mediante `mikrotikDhcpRanges()`; relay usa el servidor configurado. No se añaden pools ni reservas **editables**.

Selección, formularios, JSON y persistencia admiten MikroTik solo como Router; `am`/`bm` son opcionales para otros fabricantes y obligatorios para sus extremos MikroTik. Se conserva `state.version = 3`, migración y claves v2/v3; no se recalcula el plan al importar. No cambia `allocate()`, `confirmVlans()`, `saveSite()` ni el cuerpo IOS/VRP o los helpers Fortinet. `generateMikroTikFromForm()` confirma opciones y propuestas juntas; errores conservan el estado previo y el formulario.

Administración: SSH fuerte en puerto 22 restringido al CIDR de Gestión y su interfaz real; sin Gestión alcanzable o con SSH desactivado, el servicio queda deshabilitado. Telnet, FTP, WWW/HTTPS, APIs y Winbox deshabilitados; también acceso MAC, descubrimiento y bandwidth-server. La cadena input admite control explícito (SSH, OSPF, DHCP/relay según opciones), established/related y termina denegando. Una regla inicial **drop en forward** bloquea el tráfico reenviado hasta que se definan intenciones; no hay accept forward ni NAT/Internet implícitos. No crea usuarios ni secretos. Los controles previos de la propuesta detectan objetos `wan-`, puertos inexistentes u ocupados; no sustituyen una auditoría de configuración existente.

**Pruebas finales ejecutadas:** Python/Playwright, Chromium 154.0.8037.57, HTTP local, contextos nuevos y datos ficticios. Comandos temporales: `python /workspace/work/wan-mikrotik/verify.py` y `python /workspace/work/wan-mikrotik/integral.py`. Resultado: **T1–T21 (21/21) + I1–I9 (9/9) = 30/30 = 100% del conjunto ejecutado**; 0 fallidas, bloqueadas o no ejecutadas en el conjunto final. Es validación local/estática del texto, no ejecución de la CLI.

| Casos | Esperado y obtenido en la ejecución final | Estado |
| --- | --- | --- |
| T1–T2 | Selección/edición de nodos y puertos, localStorage y JSON v3 conservados; cero asignaciones al importar | Superadas |
| T3–T4 | Ocho VLAN LAN y una /30 coinciden con el plan; bridge CPU tagged, trunk filtrado y access/PVID coherentes | Superadas |
| T5–T6 | Instancia/área/plantillas OSPF v7, LAN pasivas; siete rutas LAN reales y default solo explícito | Superadas |
| T7–T8 | Tres servidores DHCP con exclusiones de gateway/endpoints; tres relay con servidor/IP local reales, sin DHCP simultáneo | Superadas |
| T9–T10 | Siete servicios deshabilitados, SSH/Gestión y MAC restringidos; input controlado, forward denegado y NAT ausente | Superadas |
| T11–T14 | Once entradas maliciosas, roles/datos incompletos, conflictos de gateways, LACP y puertos duplicados rechazados sin sustituir estado | Superadas |
| T15–T17 | Cuatro gramáticas separadas; cuatro variantes Fortinet y 28 salidas Cisco/Huawei idénticas a sus referencias | Superadas |
| T18–T19 | Error conserva opciones/propuesta/DOM; descargas individuales, conjuntas (separadores comentados) y JSON correctas | Superadas |
| T20 | `node --check`, cero errores de página/consola; pantalla MikroTik y campos nuevos caben a 1440/390 px | Superada |
| T21 | Router solo enrutado conserva gateways de cores; Gestión por interfaz real y SSH deshabilitado si no existe Gestión | Superada |
| I1–I9 | Modo global exacto, v2→v3/JSON sin reasignar, pools sede/tránsito, asignación mixta, errores atómicos, persistencia v2/v3, eliminación VLAN y topología/textos Cisco/Huawei | Superadas |

Evidencia temporal de sesión: scripts, `mikrotik-results.json`, `integral-results.json`, `scope-check.json`, referencias Fortinet y capturas en `/workspace/work/wan-mikrotik/`; no es una suite versionada ni un reporte académico nuevo. El harness T20 inicialmente exigía que la tabla de topología histórica cupiera; se contrastó con la base (419 px de ancho a viewport 390) y la rama (414 px), verificando separadamente que el modal y sus campos nuevos sí caben. T21 corrigió una entrada de prueba que había eliminado redes aún referenciadas por endpoints; no requirió cambios funcionales.

**Pendiente/no validado físicamente:** captura oficial `docs/capturas/07-config-mikrotik.png`, modelo/patch 7.x, puertos, hardware offload, cuentas/SSH, adyacencias y rutas de retorno. Solo rol Router; LACP/VRRP, gateways compartidos, VRF/CAPsMAN e IPv6 no se inventan. Las propuestas no son idempotentes y forward queda bloqueado por diseño; requieren revisión manual y permisos de tráfico explícitos. Persisten `saveSite()`, selector a 320 px y tabla de topología a 390 px según datos; no se corrigieron. Fuentes oficiales por familia en [matriz-fabricantes.md](matriz-fabricantes.md).

## Direccionamiento IPv4 v3: implementado y probado

El estado separa intención y plan efectivo: `project.base` es el límite global; `project.transitBase`, `sites[].ipv4Base` y `vlans[].ipv4Cidr` son cadenas opcionales, vacías por defecto y al migrar v2. Sede y VLAN tienen campos visibles; tránsito se conserva mediante JSON v3, sin control visual propio. Las VLAN sin CIDR manual se asignan automáticamente dentro del bloque de sede o del global libre. Las manuales se reservan primero, conservan su CIDR y se excluyen de la búsqueda automática y de los tránsitos. Los bloques completos de otras sedes y de tránsito permanecen reservados.

Se validan alineación, RFC1918, contención, solapamientos y capacidad con crecimiento y reservas de uno o tres hosts según cores; LAN /31 y /32 se rechazan. La búsqueda usa huecos CIDR alineados y detecta fragmentación. El gateway es independiente de la subred y del pool DHCP: vacío o automático anterior se recalcula; uno manual incompatible bloquea la confirmación. Se conserva el DHCP automático existente; pools DHCP y reservas editables están pendientes.

La confirmación solo sustituye el plan e invalida topología/configuraciones tras resolver toda la asignación. Los errores conservan estado confirmado, aprobación, derivados, almacenamiento y entradas visibles. La importación acepta intenciones manuales válidas sin plan como borrador; con plan exige coincidencia de subred, gateway y capacidad/reservas. No reasigna al importar; el plan legado recibido se conserva y se revalida al confirmar.

## Auditoría integral del PR #3

Antecedente del PR #3: se ejecutó `python /workspace/work/wan-audit/integral.py` desde un clon independiente limpio en `7c97321a79eed489d007a296a468b7af57be24e0`, servido por HTTP local temporal, con Python/Playwright y Chromium 154.0.8037.57. Cada flujo usó contextos de navegador nuevos y datos ficticios. Scripts, resultados JSON y capturas son evidencia temporal de sesión fuera del repositorio; no constituyen una suite versionada ni el reporte académico `docs/pruebas.md`. SHA-256 del HTML probado: `3cc891c1a867215f466769772e7c5bb7d265d1a93ed8dcb3b73b97534278c163`.

| Caso | Esperado y acción | Obtenido / estado |
| --- | --- | --- |
| I1 | Proyecto nuevo v3; proponer, confirmar, generar y comparar con referencia global | Superada: 15 VLAN, 19 redes, orden, gateways, reservas, topología, configuraciones y JSON iguales a la referencia sin intenciones |
| I2 | Importar laboratorio v2, exportar v3 e importar en contexto nuevo sin asignar | Superada: datos existentes conservados, intenciones vacías y cero llamadas a `allocate()` |
| I3 | Dos sedes con bloques y tránsito separado | Superada: VLAN dentro de `10.20.16.0/20` y `10.20.32.0/20`; /30 dentro de `10.20.250.0/24`; sin solapamientos |
| I4 | Combinar CIDR manual y automático; repetir confirmación | Superada: `10.20.20.0/24` y `10.20.35.0/24` respetados, resto automático y plan determinista |
| I5 | Intentar solapamiento, capacidad insuficiente y gateway incompatible | Superada: tres rechazos sin renderizar ni alterar estado, aprobación, derivados, almacenamiento o textos pendientes |
| I6 | Cargar clave v2, guardar en v3 y restaurar con ambas claves | Superada: v2 idéntica byte a byte, prioridad de v3, recarga y JSON del plan mixto conservados |
| I7 | Editar nombre, hosts y CIDR sin confirmar; eliminar otra VLAN | Superada: solo desaparece la elegida, se conservan claves/ediciones y se confirma el plan restante |
| I8 | Generar topología y salidas Cisco/Huawei del plan mixto | Superada: 28 nodos, 34 enlaces, 28 textos; 30 comprobaciones VLAN/fabricante y coherencia de interfaces, gateway, DHCP, OSPF y rutas |
| I9 | `node --check`, consola y presentación a 1440/390 px | Superada: sintaxis válida, cero errores de página/consola, sin desbordamiento de página; tabla con desplazamiento interno móvil |

Resultado final: **9/9 superadas = 100% del conjunto integral ejecutado**; 0 fallidas, 0 bloqueadas y 0 no ejecutadas dentro de ese conjunto. El harness inicial omitía la normalización histórica `subnetOK=false` cuando faltaba; se corrigió la expectativa temporal tras contrastarla con main, sin modificar la aplicación. La evidencia previa M1–M12, S1–S17, A1–A18 y V1–V8/R1–R3, y C1–C20, corresponde al mismo HTML; no se repitieron esas matrices completas ni se suman a este porcentaje. Las expectativas intermedias anteriores sobre campos inertes o CIDR bloqueado quedaron sustituidas por el comportamiento aprobado actual.

Límites: Cisco/Huawei se comprobaron únicamente como texto; no se ejecutaron configuraciones ni se validaron modelos, versiones, forwarding, convergencia o seguridad física. No es una auditoría exhaustiva de la aplicación ni certifica cumplimiento completo de Corte 3. El diff acumulado previo a documentación contenía solo `WAN_v4.html`; sintaxis, `git diff --check` y revisión de secretos/temporales fueron satisfactorios.

## Pruebas históricas P1–P6/R1 (base anterior)

P1–P6 y R1 se repitieron en la revisión histórica del 7 de noviembre con Python/Playwright ya disponibles y Chromium 154.0.8037.57, contexto de navegador nuevo y datos ficticios. Se sirvió el checkout por HTTP local temporal con `http.server`; GET de `WAN_v4.html` devolvió 200. El servidor y el navegador se cerraron al terminar. No se instalaron dependencias ni se aplicaron configuraciones de red. El antecedente `ce35714` registra bloqueo de `file://` por política del navegador (`ERR_BLOCKED_BY_ADMINISTRATOR`); esa modalidad no se repitió en esta revisión y no demuestra un fallo del HTML.

| Caso | Acción y comprobación ejecutada | Resultado y límite |
| --- | --- | --- |
| P1 | En Subnetting IPv4, introducir `192.168.10.50/26` y pulsar Calcular | Red `192.168.10.0`, broadcast `192.168.10.63`, máscara `255.255.255.192` y 62 hosts visibles |
| P2 | Tras P1, calcular `999.1.1.1/24` | `state.calc` conserva el valor válido anterior; no se verificaron todos los mensajes ni todas las entradas inválidas |
| P3 | Cargar ejemplo de laboratorio, ir a Estimación, proponer segmentación y confirmar VLAN/VLSM | Plan aprobado con 19 subredes; comprobación por pares de ausencia de solapamientos y capacidad disponible mayor o igual a hosts solicitados |
| P4 | Desde P3, generar topología desde el plan | SVG presente, 28 nodos y 34 enlaces; no valida operación de una red real |
| P5 | Desde P4, Comparación → generar las dos sintaxis | Dos bloques de texto: Cisco contiene `hostname`, Huawei contiene `sysname`; no valida toda la sintaxis ni ejecución en hardware |
| P6 | Guardar proyecto después de P5 | Existe una entrada en `localStorage`; no se probó restauración, persistencia tras reinicio ni ida y vuelta de JSON |
| R1 | En VLAN, editar sin confirmar el nombre de la primera fila y eliminar la tercera | **Defecto reproducido:** el nombre visible vuelve al confirmado anterior; no se conserva la edición pendiente |

No hubo errores de página JavaScript en el flujo HTTP ejecutado. Los resultados P1–P6/R1 de la tabla corresponden a la base histórica, no a la auditoría v3. R1 reprodujo una incidencia posteriormente corregida en main mediante el PR #2 y verificada actualmente por I7. La reproducción histórica no cuenta como prueba superada de conservación. Las verificaciones se ejecutaron como comandos de sesión, sin incorporar un harness al repositorio. No se generaron capturas ni un reporte académico formal. No se calcula porcentaje de confianza con esta prueba de humo.

Reproducción histórica: abrir el HTML de aquella base servido localmente en un navegador limpio, ejecutar P1–P6 en el orden indicado y después R1. Para repetir las comprobaciones internas usar `state.plan`, `state.nodes`, `state.links` y `state.configs` en la consola; el código conserva estas variables en el contexto del script. JSON y restauración ya cuentan con I2/I6; otras descargas, fabricantes y límites requieren casos adicionales.

## Correcciones y brechas pendientes

| Prioridad | Estado y fuente | Trabajo siguiente y aceptación |
| --- | --- | --- |
| Resuelta en el alcance probado | R1 histórico corregido por PR #2; `deleteVlan` lee las filas antes de eliminar | I7 conserva nombre, hosts y CIDR pendientes; antecedentes V1–V8/R1–R3 cubren cancelación, última fila y dependencias |
| Implementada y probada | Direccionamiento IPv4 v3 automático/mixto por global, sede, tránsito y CIDR manual por VLAN | I1–I6/I8; gateway independiente. Pools DHCP y reservas editables pendientes, sin confundirlos con subredes |
| Parcial / alta | Fortinet/MikroTik implementados y probados como texto; guía exige cuatro marcas | Validación física y capturas 06/07 pendientes; conservar regresión de cuatro adaptadores; ver matriz de fabricantes |
| Alta | IPv6 es requisito oficial general; calculadora y plan actuales son IPv4 | Confirmar alcance para Corte 3; no ocultar la brecha ni atribuirle un peso independiente |
| Media | Interfaz mezcla español y francés; Correcciones pide tanto solo botones como traducción integral | Decidir parche localizado frente a i18n total antes de modificar; son tareas distintas |
| Media | README marca filtro Huawei pendiente; `configNodes` ya ofrece equivalencias cuando no hay nodos Huawei | Verificar específicamente selección alternativa, equipos manuales y mixtos; P5 solo prueba Comparación, no certifica ese filtro |
| Media | Código monolítico y normalización solicitada | Capturar salidas de referencia y JSON, después refactor autorizado sin alterar comportamiento |
| Alta | Entregables Corte 3 y evidencias faltantes por inventario | Completar pruebas reproducibles, informe, manual, seguridad, políticas y capturas reales; ver trazabilidad |

## Dependencias y riesgos técnicos

Flujo actual: proyecto/sedes → inventario → VLAN → plan VLSM → topología/interfaces → configuraciones → exportaciones y evidencias. Ciberdefensa y validaciones atraviesan todas las etapas; persistencia serializa el estado compartido.

`invalidate` aumenta revisión y vacía datos derivados según nivel. `confirmVlans` y `editGateway` eliminan topología y configuraciones previas para evitar salidas obsoletas. Cambiar VLAN puede afectar gateway, DHCP, OSPF, enlaces y ambos fabricantes. La conservación al eliminar VLAN está probada en I7. `saveSite()` mantiene su invalidación histórica de VLAN, plan y derivados al confirmar cambios; corregirla sigue pendiente. Persiste el desbordamiento histórico a 320 px del selector de sede; no se modificó en este PR.

El validador de importación acepta Cisco/Huawei, Fortinet para Firewall y MikroTik para Router, con interfaces separadas y validación v3. Fortinet 7.4 y RouterOS 7.x son supuestos autorizados, con validación textual y compatibilidad física pendiente. IPv6 sigue pendiente.

Las configuraciones son propuestas: no hay modelo/versión de equipo verificados. HSRP y VRRP no forman un grupo común; el programa advierte pares de cores de fabricantes distintos. En Cisco/Huawei, DHCP se configura solo en el core primario y no tiene replicación de concesiones. En Fortinet, DHCP/relay solo se generan en las LAN cuyo gateway asume el firewall, sin HA compartida. La WAN dibujada no aporta VPN, cifrado ni servicio de ISP; las ACL de administración no equivalen a aislamiento entre servicios. Estas advertencias existen por inspección; no se probó cada rama de validación.

El guardado local depende del origen, navegador y cuota. La imagen es referencia manual, sin OCR ni reconocimiento automático. I2/I6 verificaron JSON y restauración, e I9 presentación a 1440/390 px; otras descargas, portapapeles, accesibilidad integral, otros tamaños/navegadores y todos los casos de seguridad siguen sin validación completa. Las capturas 01–04 y el PDF Corte 2 existen, pero no se auditó su contenido ni vigencia frente al commit base. Falta `05-github-commits.png`; la base histórica tenía 22 commits alcanzables, lo que no demuestra calidad de mensajes ni 2FA. El conector GitHub confirmó en aquella revisión `visibility: public` y rama principal `main`; 2FA no se verificó.

## Próximas etapas recomendadas

1. Revisar esta documentación y usar la trazabilidad como lista de aceptación, sin tratarla como evidencia de cumplimiento completo.
2. Crear harness versionado y casos de conservación de estado, migración v2→v3, importación/exportación v3 y salidas Cisco/Huawei de referencia.
3. Revisar las propuestas MikroTik y su PR sin fusionarlo automáticamente; tratar `saveSite()` y el desbordamiento a 320 px en tareas separadas.
4. Resolver i18n, alcance IPv6 y versiones de fabricantes; pools DHCP y reservas editables requieren diseño y autorización posteriores.
5. Completar validación de plataforma y capturas 06/07 de Fortinet/MikroTik; conservar las referencias de los cuatro adaptadores.
6. Completar ciberdefensa, pruebas formales, documentos y capturas, y ensayar sustentación en vivo.

`AGENTS.md` contiene ahora las instrucciones permanentes que gobiernan el análisis, desarrollo, corrección, pruebas, documentación y publicación de WAN Architect. Sustituye el instructivo temporal utilizado para crear esta documentación y aplica autorizaciones diferentes según el tipo de tarea. Su existencia no modifica por sí misma el código de la aplicación ni demuestra el cumplimiento de requisitos; cada resultado debe confirmarse mediante inspección y pruebas. Esta revisión documental no cambia `WAN_v4.html`.
