# Manual de usuario — WAN Architect, Corte 3

## Laboratorio completo compatible con el catálogo

En Datos del proyecto, **Cargar ejemplo de laboratorio** solicita autorización para sustituir el proyecto abierto. Construye y valida un escenario ficticio completo, sin sobrescribir automáticamente localStorage. Cancelar no cambia estado/DOM; si falla una validación, se restauran proyecto y borradores. No se usa al importar archivos de otros usuarios.

El flujo ejecuta `saveProject()`, `saveSite()`, `saveCounts()`, `proposeVlans()`, `confirmVlans()`, `saveVendorProfiles()` y `buildTopology()`, selecciona modelos y genera con los cuatro adaptadores. Las confirmaciones proceden de validadores reales, no de asignar banderas true. El resultado vuelve a Datos del proyecto con campos confirmados/Editar; puede recorrer Estimación, VLAN/VLSM, Topología, Configuración, Comparación y Consola SSH sin nuevas confirmaciones artificiales.

| Elemento | Configuración del ejemplo | Capacidad documentada / uso |
| --- | --- | --- |
| Sede asistencial | `192.168.32.0/21`, 100 usuarios, tres pisos y cores redundantes | LAN dentro de su pool, crecimiento 20% y reservas de gateway/cores |
| Sede administrativa | `172.16.64.0/21`, 45 usuarios y dos pisos | Pool propio RFC1918; no pertenece al fallback ni se exige esa contención |
| Tránsito | `10.250.0.0/24` | Seis /30 independientes para router/core, firewall y WAN; sin solapamiento con LAN |
| Core Cisco | Tres C9200L-24T-4G | 28 puertos catalogados por equipo; hasta ocho enlaces en este ejemplo |
| Acceso Huawei | Nueve S5700-28P-LI-AC | Banco RJ45 de 24 puertos; hasta cinco enlaces por switch; sin usar SFP no verificados |
| Firewall Fortinet | Dos FortiGate 60F | Tres puertos asignables conservadores; un enlace por firewall, sin desmontar switch interno/FortiLink |
| Router MikroTik | Dos RB750Gr3 (hEX), RouterOS 7 | Cinco puertos físicos por equipo; cuatro y tres enlaces respectivamente |

Se elige de forma determinista el menor inventario documentado que admite el rol y los enlaces. La asignación comprueba medio/velocidad, modos y unicidad; los generadores vuelven a validar capacidades del adaptador. Si no hay modelo suficiente, se explica el error y no se inventan puertos. No se cambian fichas ni fuentes oficiales para ajustar el ejemplo.

Resultado de laboratorio: **21 redes (15 VLAN y seis tránsitos), 42 nodos, 48 enlaces y 16 configuraciones nativas**. Los AP permanecen con inventario, gestión, VLAN/IP y enlaces, excluidos de CLI genérica. El DNS se toma de un servidor realmente direccionado en el proyecto (`192.168.34.20` en esta ejecución determinista), no de un DNS público. Los bloques son RFC1918 alineados y se validan capacidad, crecimiento, gateway y solapamientos. OSPF IPv4 usa las interfaces de tránsito efectivas; no se inventa Internet, NAT ni una ruta por defecto. Esto no demuestra forwarding, conectividad ni compatibilidad física.

En las cuatro configuraciones, **Inventario físico de interfaces** muestra Equipo, Tipo, Fabricante, Modelo, Interfaz, Función y Conectado a. Agrupa por dispositivo y muestra cada enlace real, con nombres nativos del catálogo y pares reales. No repite selectores ni formularios; la CLI queda debajo. Modo genérico identifica proyectos sin modelo. En móvil, deslice horizontalmente la tabla para consultar las siete columnas; no se ocultan puertos asignados. Los puertos libres/reservados completos siguen consultables en la vista previa de modelo de Topología.

JSON v2/v3/v4, localStorage, IPv4/IPv6, ES/EN y SSH real conservan su contrato. La planificación IPv6 continúa opcional e independiente; los generadores permanecen IPv4. La consola simulada consulta solo propuestas/datos del proyecto. No se ejecutan las configuraciones.

## Correcciones funcionales del PR #11

Base `89a5a2a948c965129ca28f40cb57f5f303f587b2`. Esta sección sustituye los comportamientos históricos que se describen más adelante.

1. **Datos del proyecto:** confirmar valida y guarda, muestra Datos confirmados y bloquea campos; Editar datos recupera la edición. `project.confirmed` opcional v4 se conserva al guardar/importar, sin inferirlo en v2/v3/v4 antiguos. Confirmar igualdad conserva cálculos, topología y configuraciones. Cambios de metadatos no borran redes; cambiar el nombre retira textos CLI que incluyen ese nombre. Estructura/segmentación/interconexión conservan su invalidación vigente. Aplicar número de sedes es una acción explícita previa.
2. **Fabricantes:** confirmar permanece en Topología y bloquea el resumen con Editar fabricantes. `sites[].vendorsConfirmed` opcional conserva la confirmación. Un cambio solo de marca no reasigna ni desconfirma VLAN/VLSM/IPv6; actualiza equipos automáticos sin override individual y retira únicamente cachés dependientes, incluyendo vecinos afectados. Modelos incompatibles se rechazan sin borrar su selección; cámbielos mediante el editor normal del equipo. Activar una función física nueva puede requerir nuevas /30: se agregan con validación atómica y sin modificar redes previas.
3. **Catálogo autónomo:** el HTML anterior dependía de `data/catalogo-interfaces.js`; copiar/abrir solo el HTML dejaba el catálogo vacío. El empaquetador ahora inserta las doce fichas verificadas en un script local del propio HTML, antes de la inicialización. `--check` comprueba JSON, JS distribuible y copia embebida. Sin fetch ni carpeta data durante ejecución; no se cambiaron datos ni fuentes oficiales. El modo HTTP con recursos data bloqueados y red desactivada está probado; la comprobación file:// se informa por separado si la política del navegador la bloquea.
4. **Selección única:** fabricante/modelo se eligen exclusivamente en Topología/editor de equipo. Cisco/Huawei/Fortinet/MikroTik muestran inventario guardado de solo lectura y consumen los mismos enlaces. Un rol sin ficha explica su ausencia; no ofrece modelos de otro tipo para forzar compatibilidad. Los AP siguen sin CLI genérica.
5. **Comparación:** cinco funciones (interfaces IPv4, VLAN/LAN, OSPF, DHCP/relay y administración) × cuatro marcas. Se extraen líneas de los adaptadores de equipos reales compatibles; no se fabrican equipos ni se cambia state/configuraciones. Cada tarjeta explica diferencias o ausencia/limitación. Los extractos no son configuraciones completas. Se conserva adicionalmente la comparación IOS/VRP por rol lógico cuando es válida, con advertencia de interfaces genéricas para la marca alternativa.
6. **Simulación y manual SSH:** comandos de lectura normalizados en espacios/capitalización, listas cerradas por marca y 19 comandos anunciados probados. `show running-config` y equivalentes muestran CLI vigente guardada o una propuesta actual generada sin guardarla, nunca running-config remoto. Las consultas no abren red ni modifican el proyecto. Interfaces/VLAN/rutas son del plan, no estado operativo; comandos desconocidos/de otra marca/escritura/inyección se rechazan. El manual es un diálogo integrado, consultable sin Python, archivos Markdown externos ni internet. La conexión SSH real y sus límites de seguridad permanecen sin cambios.

## Versión y límites de esta edición

Actualizado 2026-11-15, contrastado con main `1b46af32c8217a1f9bcea686151b1f070ac38352`. Daisy Jurleny Rodriguez · Fundación Universitaria Compensar. El formulario obligatorio de interfaces del PR #10 permanece retirado. Ahora se selecciona modelo solo en Topología; el catálogo asigna los puertos sin pedir nombres manuales. Los proyectos antiguos sin modelo conservan modo genérico con advertencia. El código de producción no cambia en esta edición documental.

Menú real 00–13: Resumen; Datos del proyecto; Estimación e infraestructura; VLAN y VLSM; Subnetting IPv4/IPv6; Topología; Cisco; Huawei; Fortinet; MikroTik; Comparación; Ciberdefensa y uso de IA; Planificación IPv6; Consola SSH. No existe el módulo Evidencias Corte 2; los archivos académicos sí se conservan.

## 1. Instalación y apertura

Descargar/clonar el repositorio completo. Para usar la app basta un navegador actualizado: abrir `WAN_v4.html`, no los nombres antiguos `WAN.html` o `Versión3.html`. No hay backend, cuentas ni paquetes que instalar para su funcionamiento principal. La carga HTTP aislada fue verificada; file:// quedó bloqueada por política administrativa en este entorno, sin certificar su apertura local. No desactive políticas de seguridad para eludir ese bloqueo.

Para reproducir el entorno de las capturas y disponer de un origen estable:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:8000/WAN_v4.html`. Cerrar con Ctrl+C. No publicar el servidor en Internet. Los enlaces a documentación oficial necesitan conexión; los datos del proyecto se procesan localmente. Cambiar de navegador, puerto o de `file://` a HTTP cambia el origen del almacenamiento: exportar JSON antes de hacerlo.

## 2. Proyecto, sedes e inventario

1. En **Datos del proyecto**, introducir nombre, empresa ficticia, actividad, infraestructura, segmentación y número de sedes. Aplicar el número de sedes y confirmar datos del proyecto; se muestra Datos confirmados y Editar datos.
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

Supuesto autorizado: FortiGate genérico de laboratorio, FortiOS 7.4, sin multi-VDOM. Crear un nodo **Firewall / Fortinet**, con IP/red del nodo vacíos: los enlaces y el plan aportan las direcciones. Elegir el modelo en Topología; FortiGate 60F/61F/70F usa únicamente los puertos asignables documentados `wan1`, `wan2` y `dmz`. Sin modelo, revisar los nombres genéricos antes de aplicar CLI. Usar /30 existentes para routed. Un trunk a switch puede hacer que el firewall asuma los gateways LAN, por lo que no debe competir con cores u otros gateways; no hay HA/LACP modelados.

En **Configuración Fortinet**, generar la propuesta y revisar interfaces/VLAN, IP, objetos, administración restringida, DHCP/relay y rutas/OSPF. `root` es el contexto interno de VLAN, no la habilitación de multi-VDOM. No se inventan NAT ni permisos de tránsito; revisar políticas, objetos e IDs antes de una futura aplicación autorizada. La [captura 06](capturas/06-config-fortinet.png) muestra el FortiGate 60F del laboratorio público actual, conectado mediante tránsito /30; no reclama gateways de los cores.

### MikroTik RouterOS

Supuesto: router genérico RouterOS 7.x, sin VRF/CAPsMAN. Crear **Router / MikroTik**, IP/red del nodo vacíos, puertos propios `am`/`bm`, por ejemplo `ether1`/`ether2`. No usar roles o redundancia no modelados. Para LAN, el adaptador genera bridge y filtrado VLAN a partir de enlaces reales; routed usa las /30 del plan. No asignar los mismos gateways a MikroTik y cores/firewalls.

En **Configuración MikroTik**, revisar identidad, puertos, bridge/VLAN, IPv4, rutas, OSPF v7 y DHCP/relay. SSH se restringe a Gestión; servicios innecesarios y acceso MAC se deshabilitan. **Forward queda bloqueado por defecto** hasta definir permisos explícitos. No se supone NAT/Internet ni se entrega una configuración de producción lista sin revisión. La [captura 07](capturas/07-config-mikrotik.png) no demuestra compatibilidad física.

Un escenario alternativo donde firewall/router termina VLAN no debe duplicar gateways de cores. El ejemplo público utiliza cores Cisco, acceso Huawei, firewall Fortinet en tránsito y routers MikroTik; cada rol conserva sus límites.

## 7. Guardar, importar y exportar

- **Guardar proyecto:** escribe `WAN-Architect-v4` en localStorage del origen actual; no es almacenamiento cifrado ni respaldo remoto.
- **Cargar guardado:** prioriza v4; si no existe, busca v3 y luego v2. Un v4 corrupto se rechaza, no se oculta cargando silenciosamente otra copia.
- **Exportar JSON:** guarda `{ state, imageData }` en esquema v4. Conservarlo además del guardado local. Los proyectos v4 no son compatibles con apps anteriores.
- **Importar JSON:** admite v2/v3 mediante migración v2→v3→v4. Conserva datos válidos de IPv4, plan, gateways, nodos, enlaces y opciones; no llama a asignadores y deja IPv6 vacío al migrar. V4 valida intenciones y coherencia del plan IPv6 recibido, sin recalcularlo.
- La importación es atómica: archivo inválido no reemplaza el estado. Los textos CLI importados solo se conservan si coinciden con su regeneración validada. No se evalúan instrucciones del JSON.
- Descargar configuraciones, SVG o CSV produce archivos; nunca conecta con routers. El CSV del plan actual sigue siendo IPv4; IPv6 está incluido en JSON v4.

## 8. Pruebas, seguridad y evidencia

Resultado vigente registrado: **114/114 aplicación + 26/26 SSH loopback = 140/140 (100%)**. En esta auditoría no se repitió la suite. [Pruebas y entorno](pruebas.md), [resumen verificable](resumen-pruebas.html) y captura 09 distinguen las dos ejecuciones reales, sus fechas y el bloqueo FILE01 separado.

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
# Para las 26 pruebas del servicio opcional, instalar sus dependencias:
python -m pip install -r ssh_service/requirements.txt
python tests/test_ssh_service.py
```

El runner UI abre/cierra HTTP y contextos limpios, imprime casos y porcentaje y devuelve no cero ante fallos. El segundo comando prueba SSH real solo contra loopback controlado; no exige equipos físicos. Para usar la aplicación o su simulador no hace falta instalar Python/SSH. No presentar los reportes existentes como resultados de una ejecución nueva.

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

## 11. Evidencias actuales y procedencia

Las diez rutas y sus hashes, fechas, escenarios y métodos se registran en [auditoria-entrega-final.md](auditoria-entrega-final.md). 01: cálculo /26; 02: laboratorio completo de dos sedes, 42 nodos y 48 enlaces; 03: core Cisco C9200L; 04: acceso Huawei S5700 con IP de Gestión; 06: FortiGate 60F; 07: router MikroTik hEX; 08: rechazo IPv4 real; 09: síntesis documental 114+26, sin ejecutar de nuevo; 10: resumen actual con selector de idioma.

En 03/04 se desmarcaron SSH/OSPF/DHCP para mostrar interfaces; no son plantillas de seguridad recomendadas. Se expandió temporalmente el contenedor desplazable de CLI/SVG solo para capturar su contenido íntegro, sin cambiar código, datos ni resultados. Las propuestas completas y sus restricciones siguen en la app. 05 conserva la página auténtica de GitHub de la entrega anterior: cinco o más commits legibles, sin CSS externo; es evidencia histórica, no del HEAD nuevo.

Los AP permanecen en inventario, topología, VLAN, IP/máscara/gateway de Gestión y enlaces. Los cuatro adaptadores los excluyen de CLI genérica; el switch vecino conserva su interfaz. La tabla física tiene siete columnas y usa dispositivos, modelos, enlaces y vecinos reales; desplácela horizontalmente en móvil.

La [consola SSH](manual-ssh.md) ofrece dos modalidades independientes. Simulación: seleccionar un equipo, `help`, consultar comandos de lectura y propuestas del proyecto, sin conexión real. Manual integrado accesible sin Python. Real: instalar el servicio opcional según su README, configurar destinos autorizados y huellas, abrir su HTTP local, autenticar expresamente y escribir comandos manualmente. Credenciales solo en memoria, no en JSON/localStorage. No hay envío automático de configuraciones.

La sustentación sigue pendiente. Ensayar el recorrido público, explicar cálculos y adaptadores, ejecutar ambos runners ante el docente y registrar el resultado real. No declarar conectividad o certificación física. Los conteos históricos de botones que siguen se refieren a sus commits; el número de instancias dinámicas depende del proyecto y no constituye un inventario estático vigente.

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
