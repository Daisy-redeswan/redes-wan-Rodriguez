# Manual de usuario — WAN Architect, Corte 3

## Ajuste vigente del PR #10: generación automática y menú

- **VLAN/VLSM sigue requiriendo un plan válido y confirmado** antes de Topología, fabricantes o Comparación. Revertir borradores reconoce la aprobación anterior. Subnetting, Ciberdefensa, IPv6 y SSH manual conservan su acceso independiente y sus validaciones.
- **Se retiró el formulario Confirmar interfaces físicas** y sus campos obligatorios. Tras generar la topología y seleccionar marcas compatibles, pulse Generar equipo o Generar todos: no se solicitan modelo, versión, URL ni confirmación adicional de puertos. Las interfaces se derivan automáticamente de los enlaces por fabricante. El editor normal de enlaces sigue disponible para ajustar sus nombres y valida entradas inseguras/duplicadas.
- Los nombres son propuestas de laboratorio: **verifique puertos, modelo, versión y configuración existente antes de aplicar CLI a un equipo físico**. Es una advertencia visual, no un requisito de generación ni una certificación física.
- **AP**: permanecen en inventario, topología, VLAN y enlaces, con IP, máscara y gateway de gestión en su editor. Ninguno de los cuatro adaptadores genera CLI genérica para AP; sus comandos específicos requieren modelo, firmware y modalidad de administración. El switch vecino conserva su puerto hacia el AP.
- **Menú consecutivo**: 06 Configuración Cisco, 07 Configuración Huawei, 08 Configuración Fortinet, 09 Configuración MikroTik, 10 Comparación, 11 Ciberdefensa y uso de IA. Los demás módulos permanecen; IPv6 conserva 12 y SSH 13. Numeración desde 00, flechas y progreso usan ese mismo orden en Español/English.
- **Comparación** produce ambas sintaxis automáticamente sin pedir perfiles ni cambiar el fabricante real. La selección de fabricantes mixtos por sede/función/dispositivo continúa disponible.
- **Guardado y carga**: JSON v2/v3/v4 y localStorage conservan sus migraciones. Si un v4 anterior contiene perfiles de interfaces, se preservan como metadatos históricos, pero no dirigen la CLI nueva. Sus textos canónicos archivados pueden restaurarse sin perderlos; al regenerar se usan los puertos del enlace. No se asignan redes durante la carga.

Detalle del contrato: [perfiles históricos y compatibilidad](documentacion-codigo.md#perfiles-físicos-opcionales-y-compatibilidad). Resultados y límites: [pruebas del ajuste](pruebas-interfaces.md).

Versión documental de la interfaz bilingüe; base main `6ac46f9257143f88ec8cb7b47c020bb3739adbfa`, aplicación `WAN_v4.html`, esquema v4. Estudiante: Daisy Jurleny Rodriguez · Fundación Universitaria Compensar. Las configuraciones son propuestas para revisión manual; **no se ejecutan sobre equipos**. Usar exclusivamente datos ficticios o infraestructura de laboratorio autorizada.

## 1. Instalación y apertura

Descargar/clonar el repositorio completo. Para usar la app basta un navegador actualizado: abrir `WAN_v4.html`, no los nombres antiguos `WAN.html` o `Versión3.html`. No hay backend, cuentas ni paquetes que instalar para su funcionamiento principal.

Para reproducir el entorno de las capturas y disponer de un origen estable:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:8000/WAN_v4.html`. Cerrar con Ctrl+C. No publicar el servidor en Internet. Los enlaces a documentación oficial necesitan conexión; los datos del proyecto se procesan localmente. Cambiar de navegador, puerto o de `file://` a HTTP cambia el origen del almacenamiento: exportar JSON antes de hacerlo.

## 2. Proyecto, sedes e inventario

1. En **Datos del proyecto**, introducir nombre, empresa ficticia, actividad, infraestructura, segmentación y número de sedes. Confirmar datos del proyecto y aplicar el número de sedes.
2. Seleccionar cada sede, registrar pisos, usuarios, áreas, servicios y redundancia; confirmar su ficha. El bloque IPv4 de sede es opcional y debe estar alineado, ser privado, poder ser independiente del predeterminado y no solaparse con otras sedes/tránsito.
3. Revisar **Estimación e infraestructura**. Las cantidades son estimaciones preliminares; no sustituyen estudios RF, inventarios físicos ni dimensionamiento profesional.
4. Confirmar fichas e inventario. Una confirmación idéntica conserva el diseño; un cambio real invalida dependencias locales y vecinos WAN afectados. El inventario confirmado muestra resumen y **Editar inventario**; restaurar estimación solicita confirmación.

El ejemplo integrado es ficticio. Se puede usar para aprender el flujo sin introducir datos sensibles. No reutilizar su nombre de empresa, DNS o cantidades como si fueran requisitos de una organización real.

## 3. VLAN y direccionamiento IPv4

Proponer VLAN y revisar sede, ID, nombre, servicio, hosts y DHCP de cada fila. Se permite repetir ID entre sedes, pero no dentro de una sede. Mantener una VLAN de Gestión por sede. Los hosts y el crecimiento afectan la capacidad calculada.

En **VLAN y VLSM**, confirmar el bloque predeterminado privado, el bloque opcional de tránsito, crecimiento y DNS. Los bloques propios de sede pueden ser independientes del predeterminado; todos deben ser privados, alineados y no solapados. Vacío en **Subred IPv4 / CIDR (opcional)** mantiene asignación automática; una red manual, por ejemplo `10.20.20.0/24`, no es el gateway ni el pool DHCP. Debe estar alineada, tener capacidad y respetar el bloque de sede o el espacio global libre. LAN /31 y /32 se rechazan. El bloque de tránsito `project.transitBase` tiene control visible y persistencia v4. Una sede sin bloque utiliza el fallback libre excluyendo reservas de otras sedes y tránsito.

Pulsar **Confirmar VLAN y calcular VLSM**. Primero se reservan manuales/bloques de sede/tránsito; las automáticas buscan huecos CIDR alineados. Si falta capacidad o hay solapamiento, no se sustituye el plan anterior ni se pierden las entradas visibles. No ampliar redes manuales silenciosamente.

El plan muestra redes, prefijos, máscaras, rangos, broadcast IPv4 y gateways. El gateway se edita por separado; debe ser utilizable y no duplicar un endpoint o reservas. Cambiarlo invalida topología/configuraciones para evitar salidas obsoletas. DHCP sigue siendo automático; no hay pools ni reservas manuales editables.

Al eliminar una VLAN se leen antes las ediciones válidas de las otras filas. Cancelar no altera el diseño; una fila inválida bloquea la eliminación sin reconstruir el formulario. Una eliminación confirmada invalida los planes/derivados dependientes; volver a confirmar antes de generar topología.

## 4. Calculadora y planificación IPv6

**Subnetting IPv4 / IPv6** admite IP/CIDR o IPv6/prefijo, por ejemplo `192.168.10.50/26` o `2001:db8:1234:5678::9/64`. Muestra representación canónica, red/prefijo, rango y clasificación. IPv6 no tiene broadcast y su capacidad matemática no descuenta red/broadcast. La clasificación no acredita enrutabilidad ni equivale a una lista de hosts asignables.

En **Planificación IPv6**, habilitar la opción. La app propone un ULA /48 con identificador pseudoaleatorio; confirmar para guardarlo. El proyecto admite ULA local fd00::/8 con prefijo /48–/56; cada sede recibe /56 manual o automático y cada VLAN una /64. No se asigna una dirección pública por generar ULA. La sede sin bloque recibe un /56 del global, excluyendo los bloques manuales reservados. El orden depende de claves estables y no del orden visual de las filas.

Con una sede /56 se pueden planificar hasta 256 VLAN /64. El router se propone como **dirección completa de red + 1**, no como la IP literal `::1`: con redundancia, ::1 virtual y ::2/::3 físicas; sin redundancia, ::1 física. Son reservas, no configuración de protocolos. Confirmar IPv6 no altera el plan IPv4 ni las CLI. Desactivar y confirmar vacía solo la intención y el plan IPv6.

Las VLAN utilizadas son las del estado confirmado; guardar antes sus cambios en la pantalla VLAN/VLSM. Los errores de prefijo, alineación, capacidad, contención o solapamiento conservan formulario, estado y planes anteriores. No hay tránsitos IPv6, DHCPv6, SLAAC avanzado, NAT66 ni políticas IPv6. **Los cuatro generadores siguen siendo IPv4** hasta aclaración docente.

## 5. Topología e interfaces

Antes de generar, elegir **Fabricantes por sede y función** y confirmar. Router, core, acceso y distribución activa exigen elección; firewall Fortinet y router secundario son opcionales y requieren recalcular tránsitos. Genérico identifica terminales sin CLI; no se asigna Cisco automáticamente. Los dos cores redundantes deben compartir fabricante. Editores permiten asignación individual y exigen puertos de destino válidos.

**Reorganizar diagrama** cambia solo coordenadas; zoom y desplazamiento permiten inspeccionar lienzos grandes. Iconos originales diferencian equipos, colores diferencian WAN/routed/trunk/access y hover/tablas muestran detalles completos. Regenerar conserva IDs automáticos y equipos manuales; los equipos antiguos sin autoKey se conservan sin inferir autoría. Nombres/elecciones individuales explícitas se mantienen.


Tras confirmar IPv4, ir a **Topología → Generar desde el plan**. Revisar roles, sedes, enlaces y puertos. La WAN dibujada es un laboratorio enrutado: no constituye VPN, cifrado ni conexión real con un ISP. Arrastrar nodos solo modifica su posición; generar de nuevo reconstruye el diseño.

Para editar/agregar equipos, usar hostname seguro, tipo y fabricante compatibles. Para cada enlace indicar extremos, tipo, red de tránsito /30 existente y puertos de cada fabricante. Los campos Cisco, Huawei, Fortinet y MikroTik son separados. No repetir un puerto en dos enlaces. Access, trunk y routed tienen validaciones distintas. Una imagen importada se usa como referencia manual; no reconoce automáticamente equipos ni enlaces.

## 6. Generación por fabricante

Las opciones compartidas de OSPF, DHCP/relay y ruta por defecto pueden invalidar propuestas previas al modificarse. No seleccionar simultáneamente DHCP local y relay. Una ruta por defecto exige siguiente salto conectado y justificación; no implica Internet ni NAT. Copiar o descargar texto no lo ejecuta.

### Cisco IOS/IOS XE y Huawei VRP

La topología automática sirve para el flujo de routers/switches y cores. Elegir fabricante, equipo y opciones; generar un equipo o todos. Huawei muestra solo equipos realmente asignados a Huawei; las equivalencias IOS/VRP se solicitan exclusivamente en Comparación. **Comparación** no convierte hardware ni certifica interoperabilidad. Las propuestas incluyen VLAN, SVI/Vlanif, IP, OSPF, DHCP o relay y funciones según rol/opciones. HSRP y VRRP no forman un mismo grupo interoperable; no mezclar cores de distinta marca para suponer redundancia común.

### Fortinet FortiOS

Supuesto autorizado: FortiGate genérico de laboratorio, FortiOS 7.4, sin multi-VDOM. Crear un nodo **Firewall / Fortinet**, con IP/red del nodo vacíos: los enlaces y el plan aportan las direcciones. Mapear puertos propios `af`/`bf`, por ejemplo `port1` y `port2`. Usar /30 existentes para routed. Un trunk a switch puede hacer que el firewall asuma los gateways LAN, por lo que no debe competir con cores u otros gateways; no hay HA/LACP modelados.

En **Configuración Fortinet**, generar la propuesta y revisar interfaces/VLAN, IP, objetos, administración restringida, DHCP/relay y rutas/OSPF. `root` es el contexto interno de VLAN, no la habilitación de multi-VDOM. No se inventan NAT ni permisos de tránsito; revisar políticas, objetos e IDs antes de una futura aplicación autorizada. La [captura 06](capturas/06-config-fortinet.png) corresponde a este escenario perimetral independiente, sin cores en su sede.

### MikroTik RouterOS

Supuesto: router genérico RouterOS 7.x, sin VRF/CAPsMAN. Crear **Router / MikroTik**, IP/red del nodo vacíos, puertos propios `am`/`bm`, por ejemplo `ether1`/`ether2`. No usar roles o redundancia no modelados. Para LAN, el adaptador genera bridge y filtrado VLAN a partir de enlaces reales; routed usa las /30 del plan. No asignar los mismos gateways a MikroTik y cores/firewalls.

En **Configuración MikroTik**, revisar identidad, puertos, bridge/VLAN, IPv4, rutas, OSPF v7 y DHCP/relay. SSH se restringe a Gestión; servicios innecesarios y acceso MAC se deshabilitan. **Forward queda bloqueado por defecto** hasta definir permisos explícitos. No se supone NAT/Internet ni se entrega una configuración de producción lista sin revisión. La [captura 07](capturas/07-config-mikrotik.png) no demuestra compatibilidad física.

No combinar el laboratorio automático con cores y el escenario perimetral que reclama sus gateways. Son alternativas de laboratorio compatibles con el mismo modelo, no un único diseño de gateways duplicados.

## 7. Guardar, importar y exportar

- **Guardar proyecto:** escribe `WAN-Architect-v4` en localStorage del origen actual; no es almacenamiento cifrado ni respaldo remoto.
- **Cargar guardado:** prioriza v4; si no existe, busca v3 y luego v2. Un v4 corrupto se rechaza, no se oculta cargando silenciosamente otra copia.
- **Exportar JSON:** guarda `{ state, imageData }` en esquema v4. Conservarlo además del guardado local. Los proyectos v4 no son compatibles con apps anteriores.
- **Importar JSON:** admite v2/v3 mediante migración v2→v3→v4. Conserva datos válidos de IPv4, plan, gateways, nodos, enlaces y opciones; no llama a asignadores y deja IPv6 vacío al migrar. V4 valida intenciones y coherencia del plan IPv6 recibido, sin recalcularlo.
- La importación es atómica: archivo inválido no reemplaza el estado. Los textos CLI importados solo se conservan si coinciden con su regeneración validada. No se evalúan instrucciones del JSON.
- Descargar configuraciones, SVG o CSV produce archivos; nunca conecta con routers. El CSV del plan actual sigue siendo IPv4; IPv6 está incluido en JSON v4.

## 8. Pruebas, seguridad y evidencia

Revisión integral actual: **50/50**, C01–C31 y N01–N19, en [reporte actual](../tests/reporte-revision-integral.html). Los reportes/capturas académicos anteriores siguen siendo históricos, sin sobrescribirlos. La navegación tiene 13 módulos: Fortinet 10, MikroTik 11, IPv6 12; se retiró exclusivamente la pantalla Evidencias Corte 2.


Seguir [docs/pruebas.md](pruebas.md) para instalar Playwright/Chromium y ejecutar:

```bash
python tests/test_corte3.py
```

El runner abre/cierra HTTP local y contextos limpios, imprime C01–C31/N01–N19 y el porcentaje real. Detener la publicación si devuelve no cero. El 50/50 actual es del conjunto ejecutado, no certificación de toda la app ni hardware. La captura 09 y el reporte anterior conservan el resultado histórico de 31 casos, con su commit y hashes originales.

Antes de compartir: usar datos ficticios, revisar nombres/IP/configuraciones, no introducir secretos y conservar `<CAMBIAR_EN_PRODUCCION>` como marcador externo. Consultar [seguridad](seguridad.md) y [políticas IA](politicas-ia.md). La [captura 08](capturas/08-ciberdefensa.png) muestra una IPv4 rechazada conservando el último resultado válido.

## 9. Idioma y conservación de datos

En la barra superior, **Idioma / Language → Español / English**. El primer uso inicia en español; la selección se conserva en `WAN-Architect-language`, independiente de `WAN-Architect-v4`. Nueva/carga de proyecto no borra el idioma. Cambiar idioma conserva estado, planes, topología, CLI y ediciones visibles pendientes (incluidas entradas inválidas y selección de opciones); no confirma formularios. Navegar a otra vista sigue el flujo histórico: confirmar primero los datos que corresponda.

El catálogo central `I18N` y `t()` traducen navegación, etiquetas, botones, ayudas, placeholders, tooltips, tablas, mensajes y confirmaciones. Los valores de las opciones conservan sus códigos originales. Los nombres del usuario, hostnames, interfaces, JSON y propuestas CLI **no se traducen**. Es normal que una sede llamada «Nombre» o un comentario CLI siga igual en English. Los nombres oficiales de fabricantes/protocolos se conservan.

Usar Tab para enfocar y Enter para activar botones nativos; Espacio/Enter activa los importadores visibles. Escape cierra el diálogo. Los botones de eliminar equipo/enlace tienen nombre accesible y tooltip. «Anterior»/«Siguiente» se deshabilitan en los extremos; «Vista automática» se deshabilita cuando la imagen no está activa. Una generación sin requisitos o descarga sin datos muestra validación. Copiar usa el portapapeles real; si el navegador lo bloquea, ofrece copia manual con seleccionar todo/cerrar. Revisar la CLI antes de cualquier uso autorizado.

## 10. Inventario y auditoría de controles

La revisión actual verifica **62 plantillas button** con handler, dos importadores y selector de idioma. Se mantienen acciones de edición de inventario, confirmación de fabricantes, zoom/reorganización, teclado, validación y bloqueos reales. Ver C27/C28 y N04/N09/N12/N13. El detalle anterior y su manifiesto se conservan como antecedente; las acciones exclusivas del módulo de evidencias ya no están en la interfaz.


La auditoría histórica de main 1956d18 inventarió **58 plantillas `<button>` estáticas/dinámicas**, dos importadores con rol de botón y un selector de idioma: 61 controles de estas clases. No es un conteo fijo de instancias: cada fila VLAN, equipo, enlace o configuración puede crear botones. **0 eliminados**: todos tenían función real; se conservaron los que requieren datos. Se corrigió la disponibilidad de Vista automática y se añadieron validaciones explícitas a copia/descarga sin configuración. C28 activó 54 familias/objetivos con Enter; C29 cubre selección manual y ambos importadores, y C21–C25/C30–C31 el selector/idiomas.

| Vista / controles | Acción observable o validación | Evidencia automatizada |
| --- | --- | --- |
| Navegación 00–13, Anterior, Siguiente, Continuar, Ver sección | Abre la etapa indicada; extremos deshabilitados | C22/C27/C28 |
| Guardar / Cargar / Nuevo | Persistir, restaurar o confirmar sustitución; cancelar conserva datos | C05/C23/C24/C28 |
| Importar / Exportar JSON | Selector de archivo accesible, validación atómica y descarga JSON | C03–C05/C17/C19/C28/C29 |
| Idioma / Language | Cambia la interfaz y persiste solo la preferencia | C21–C26/C30/C31 |
| Confirmar proyecto / Aplicar sedes / Cargar ejemplo | Guarda datos, ajusta sedes con confirmación o carga laboratorio ficticio | C28 |
| Confirmar sede / Eliminar sede | Guarda solo cambios reales y conserva dependencias no afectadas | C28; límite explicado en §2 |
| Confirmar inventario / Restaurar estimación | Guarda cantidades o restaura cálculo con confirmación | C28 |
| Proponer segmentación / Volver a proponer / Agregar VLAN | Crea propuesta revisable, solicita confirmación o añade fila | C06/C07/C28 |
| Confirmar VLAN/VLSM / Eliminar fila | Calcula o valida antes de sustituir; elimina solo seleccionada y conserva otras ediciones | C06–C08/C28 |
| Gateway / Validar / Validar red del proyecto | Prompt de gateway y validación; lleva subred a calculadora | C07/C08/C28 |
| Calcular / Ejemplo /26 | Resultado válido o error sin perder cálculo previo | C01/C02/C23/C28 |
| Confirmar IPv6 | Plan ULA separado o validación atómica | C09/C10/C26/C28 |
| Generar topología / Agregar equipo / Crear enlace | Construye desde plan o abre editor | C11/C28 |
| Editar / Confirmar equipo o enlace / Eliminar × / Cancelar | Diálogo, validación, modificación o confirmación/cierre | C11/C17/C25/C28 |
| Descargar SVG / Cargar imagen / Ver-ocultar / Vista automática | Descarga real, referencia manual y alternancia; sin OCR | C28/C29 |
| Generar equipo / Generar todos (cuatro marcas) | Genera texto del plan o explica requisitos faltantes | C12–C16/C26–C28 |
| Generar ambas sintaxis | Compara Cisco/Huawei sin cambiar fabricante del nodo | C28 |
| Copiar / Seleccionar todo / Cerrar | Copia exacta o fallback manual seleccionable | C28/C29 |
| Descargar / Descargar todos | CLI individual/conjunto exacto, o validación si falta generar | C19/C28/C29 |
| Descargar CSV / Resumen HTML / Imprimir-PDF | Exporta columnas/resumen en el idioma activo; invoca impresión del navegador | C28; CLI/JSON intactos en C19/C25/C26 |

La prueba de impresión comprueba la llamada al navegador mediante un sustituto de la API; no afirma haber impreso una hoja física. Las opciones checkbox/select editan valores; no son botones decorativos. El inventario no certifica todas las combinaciones de datos posibles.

## 11. Evidencias históricas 01–10 y laboratorios

| Archivo | Lectura correcta |
| --- | --- |
| [01-subnetting.png](capturas/01-subnetting.png) | Calculadora actual con IP /26, red .0, broadcast .63 y 62 hosts |
| [02-topologia.png](capturas/02-topologia.png) | Laboratorio pequeño: dos sedes, dispositivos/enlaces completos |
| [03-config-cisco.png](capturas/03-config-cisco.png) | Core Cisco real: hostname, VLAN y direcciones visibles |
| [04-config-huawei.png](capturas/04-config-huawei.png) | Core Huawei equivalente: sysname, VLAN e IP visibles |
| [05-github-commits.png](capturas/05-github-commits.png) | Página HTTPS real de commits de main, al menos cinco mensajes |
| [06-config-fortinet.png](capturas/06-config-fortinet.png) | Propuesta perimetral real FortiOS; no forwarding probado |
| [07-config-mikrotik.png](capturas/07-config-mikrotik.png) | Propuesta perimetral real RouterOS; no comandos ejecutados |
| [08-ciberdefensa.png](capturas/08-ciberdefensa.png) | Rechazo real de IPv4 conservando resultado válido anterior |
| [09-pruebas.png](capturas/09-pruebas.png) | Nueva ejecución de 31 casos con X/Y y porcentaje reales |
| [10-app-final.png](capturas/10-app-final.png) | Resumen funcionando y selector de idioma visible |

01–04 usan una calculadora o un laboratorio reducido de dos sedes con 12 usuarios por sede, sin WiFi/voz/CCTV/impresión/servidor y sin redundancia: permite mostrar el diagrama completo y ambos cores con VLAN e IP. En 03/04 SSH, OSPF y DHCP se desmarcaron para destacar interfaces; **no son plantillas de seguridad listas para producción**. 06/07 usan el laboratorio perimetral alternativo explicado en §6. 10 usa el laboratorio integrado de 15 VLAN, plan IPv4 por pools y plan IPv6. Cada escenario consume el mismo contrato v4; no se mezclan gateways duplicados.

05 se obtuvo de `https://github.com/Daisy-redeswan/redes-wan-Rodriguez/commits/main/`, respuesta 200; TLS verificado mediante el proxy de confianza del entorno. Chromium renderizó los bytes auténticos recibidos. Recursos externos de estilos/avatares bloqueados: la imagen conserva el render nativo legible y no reconstruye mensajes ni DOM. Las capturas de la app usan HTTP local y contextos limpios; el informe identifica fuentes y resultados.

Pendientes: modelos/firmware y validación física, aclaración de configuraciones IPv6, pools DHCP/reservas editables y cobertura completa de combinaciones masivas. La revisión responsive 1440/390 px no certifica todos los anchos o dispositivos. No se aplicaron configuraciones a infraestructura real.

## Anexo histórico: 58 plantillas de la base main 1956d18

Cada fila identifica una plantilla del HTML/JavaScript. «…» representa datos o parámetros dinámicos; no otra acción sin implementar. Los importadores JSON/imagen y el selector de idioma se contabilizan por separado y se prueban en C29/C21–C25.

| N.º | Origen | Etiqueta / dato | Handler o acción |
| --- | --- | --- | --- |
| 1 | `barra superior` | Guardar proyectoCargar guardadoExportar JSONImportar JSONNuevo | `saveLocal()` |
| 2 | `barra superior` | Cargar guardadoExportar JSONImportar JSONNuevo | `loadLocal()` |
| 3 | `barra superior` | Exportar JSONImportar JSONNuevo | `exportJSON()` |
| 4 | `barra superior` | Nuevo | `newProject()` |
| 5 | `render` | …… | `go(${i})` |
| 6 | `render` | ← Anterior | `go(${page - 1})` |
| 7 | `render` | Siguiente → | `go(${page + 1})` |
| 8 | `projectView` | Confirmar datos del proyecto | `saveProject()` |
| 9 | `projectView` | Aplicar número de sedes | `resizeSites()` |
| 10 | `projectView` | Cargar ejemplo de laboratorio | `demo()` |
| 11 | `projectView` | Eliminar sede | `removeSite()` |
| 12 | `projectView` | Confirmar esta sede | `saveSite()` |
| 13 | `estimateView` | Confirmar inventario de esta sede | `saveCounts(${i})` |
| 14 | `estimateView` | Restaurar estimación | `resetCounts(${i})` |
| 15 | `estimateView` | Proponer segmentación y continuar → | `proposeVlans()` |
| 16 | `vlanView` | Volver a proponer | `proposeVlans()` |
| 17 | `vlanView` | Agregar VLAN | `addVlan()` |
| 18 | `vlanView` | Confirmar VLAN y calcular VLSM | `confirmVlans()` |
| 19 | `vlanView` | Eliminar | `deleteVlan(${i})` |
| 20 | `planTable` | Descargar CSV | `downloadPlan()` |
| 21 | `planTable` | … | `editGateway('${r.key}')` |
| 22 | `planTable` | Validar | `inspectSubnet(${i})` |
| 23 | `subnetView` | Calcular | `calculate()` |
| 24 | `subnetView` | Ejemplo obligatorio /26 | `state.calc='192.168.10.50/26';render()` |
| 25 | `subnetView` | … · … · …/… | `inspectSubnet(${i})` |
| 26 | `ipv6View` | Confirmar planificación IPv6 | `confirmIPv6()` |
| 27 | `topologyView` | Generar desde el plan | `buildTopology()` |
| 28 | `topologyView` | Agregar equipo | `editNode()` |
| 29 | `topologyView` | Crear enlace | `editLink()` |
| 30 | `topologyView` | Descargar topología SVG | `downloadSVG()` |
| 31 | `topologyView` | Vista automática | `imageMode=false;render()` |
| 32 | `topologyView` | Ver / ocultar imagen | `imageMode=!imageMode;render()` |
| 33 | `topologyView` | Editar | `editNode('${n.id}')` |
| 34 | `topologyView` | × | `deleteNode('${n.id}')` |
| 35 | `topologyView` | Editar | `editLink('${l.id}')` |
| 36 | `topologyView` | × | `deleteLink('${l.id}')` |
| 37 | `editNode` | Confirmar equipo | `saveNode('${id}')` |
| 38 | `editNode` | Cancelar | `closeModal()` |
| 39 | `editLink` | Confirmar enlace | `saveLink('${id}')` |
| 40 | `editLink` | Cancelar | `closeModal()` |
| 41 | `configView` | Generar equipo | `generateSelected('${vendor}')` |
| 42 | `configView` | Generar todos los … | `generateAll('${vendor}')` |
| 43 | `configView` | Descargar todos | `downloadAll('${vendor}')` |
| 44 | `fortinetView` | Generar equipo | `generateSelected('Fortinet')` |
| 45 | `fortinetView` | Generar todos los Fortinet | `generateAll('Fortinet')` |
| 46 | `fortinetView` | Descargar todos | `downloadAll('Fortinet')` |
| 47 | `mikrotikView` | Generar equipo | `generateSelected('MikroTik')` |
| 48 | `mikrotikView` | Generar todos los MikroTik | `generateAll('MikroTik')` |
| 49 | `mikrotikView` | Descargar todos | `downloadAll('MikroTik')` |
| 50 | `configBlock` | Copiar configuración | `copyConfig('${n.id}','${v}')` |
| 51 | `configBlock` | Descargar | `downloadConfig('${n.id}','${v}')` |
| 52 | `compareView` | Generar ambas sintaxis | `generateCompare(id)` |
| 53 | `copyConfig` | Seleccionar todo | `$('manualcopy').select()` |
| 54 | `copyConfig` | Cerrar | `closeModal()` |
| 55 | `dashboard` | Continuar diseño → | `go(1)` |
| 56 | `dashboard` | Descargar resumen HTML | `downloadReport()` |
| 57 | `dashboard` | Imprimir / PDF | `window.print()` |
| 58 | `evidenceView` | Ver sección | `go(${i})` |
