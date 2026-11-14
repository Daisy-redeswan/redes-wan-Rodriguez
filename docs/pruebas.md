# Pruebas reproducibles de WAN Architect — Corte 3 y revisión integral

## Catálogo local de interfaces: estado vigente

Base `6466c9494cefdb5423d95e1bc04175304a4e248d`, rama `feature/catalogo-interfaces-fabricantes`. Verificación documental y pruebas: **14 de noviembre de 2026**. Se incorporan doce fichas, tres por fabricante, contrastadas con fuentes oficiales y límites explícitos en [catálogo de modelos](catalogo-modelos.md). No es certificación física.

**Implementado:** selección fabricante/modelo filtrada por tipo en el editor normal y selección de modelo en Topología/configuración; inventario local, asignación determinista de puertos por enlace/medio/velocidad, conservación de nombres válidos, bloqueo de capacidad/roles/funciones incompatibles y validación de importaciones. No se pide escribir interfaces, versión ni URL. Los cuatro adaptadores leen nombres reales de los enlaces para el modelo elegido. Huawei LI incluye solo banco RJ45 verificado; Fortinet reserva switch interno y FortiLink. No hay consultas de red durante uso normal.

**Confirmado por pruebas:** 73 casos anteriores + 23 casos K01–K23 = **96/96 aplicación**; **26/26 SSH local**, total **122/122 = 100%** del conjunto ejecutado, 0 fallidas/bloqueadas/no ejecutadas dentro de las matrices. Reportes reales: [aplicación](../tests/reporte-catalogo.html) y [SSH](../tests/reporte-catalogo-ssh.json). Se conservan las ocho comparaciones exactas de CLI (cuatro marcas × ES/EN) para proyectos sin modelo, los 99 casos previos, IPv4/IPv6, JSON v2/v3/v4 y exclusión CLI de AP. Datos ficticios, contextos limpios, HTTP local y SSH real exclusivamente loopback; no se aplica CLI.

**Persistencia:** `nodes[].modelId` es una extensión opcional de v4; ausencia conserva comportamiento genérico y aviso de modelo no especificado. Las interfaces permanecen en campos de enlaces existentes. La carga valida sin reasignar; no cambia versión, migración, claves locales, planes, IP ni configuración SSH. La ruta fija del servicio SSH opcional sirve solo el script local del catálogo.

**Pendiente/límites:** comprobar equipos reales, firmware/licencias, transceptores, puertos renombrados y configuración previa. SFP Huawei excluidos hasta completar nomenclatura por variante. No se amplían los adaptadores a roles/funciones no respaldados, IPv6 CLI ni pools/reservas editables. Revisión visual 1440/390 px satisfactoria; `file://` fue bloqueado por política del navegador del entorno y se declara como una exploración bloqueada aparte, no como caso superado. El modo sin internet se verificó mediante HTTP local con la red del contexto desactivada. Los apartados siguientes conservan evidencia histórica, no sustituyen este resultado.

### Reproducción y entorno del catálogo

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tools/build_catalogo.py --check
python tests/test_corte3.py --report tests/reporte-catalogo.html
# Solo los casos nuevos, cuando se necesita aislar un diagnóstico:
python tests/test_catalogo.py
# Entorno SSH opcional, separado de la app estática:
python -m pip install -r ssh_service/requirements.txt
python tests/test_ssh_service.py
```

No hay dependencias nuevas. El runner inicia/cierra servidor y contextos, imprime casos y porcentaje y devuelve fallo si un caso falla. `test_corte3.py` registra los 73 casos originales sin modificar sus cuerpos y añade K01–K23. Las fichas de contraste en `tests/fixtures/catalogo-verificado.json` contienen conteos/rangos/velocidades y fuentes oficiales; no se cambiaron fixtures CLI históricas para hacer pasar el catálogo.

Ejecución final de aplicación: `2026-11-14T13:28:08-05:00`; Linux-6.18.57-x86_64-with-glibc2.41; Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57; 126.5 s. SSH: 2026-11-14T18:25:55.304550+00:00, AsyncSSH 2.24.1, aiohttp 3.14.5; 10.4 s. Los reportes registran el HEAD base y los hashes del árbol de trabajo probado **antes de los commits de publicación**; no se atribuye a otro commit una ejecución que no ocurrió.

- SHA-256 aplicación: `e915447fa14dfbcf82bcb36d85b3567b291793c47603854c83ed1811f44ca400`.
- SHA-256 catálogo: `0d1a18afbf51c5a5eb7be79d8d85d1a1b5182fee68d87867d423f4ab535ab050`.
- SHA-256 runner: `9d43744efb4cb7920be2f3987c5afcc3df2cb1c7938b281067b2d28a1d2c7335`.
- SHA-256 casos nuevos: `7a99e7e78767331cddb328b0db7d0ae6ee99077cee7c61fbbbecead88df06ea2`.
- SHA-256 servidor SSH: `81eff1af1894668d980d172346648b1d2ea0ab68f5432226c8cdf3690f182dba`.

### Casos nuevos: esperado, obtenido y estado

| Caso | Esperado | Obtenido | Estado |
| --- | --- | --- | --- |
| K01 · Catálogo contra fichas oficiales | Doce modelos; cantidades, nombres, velocidades y fuentes contrastan con fichas verificadas. | 12 fichas (3 por marca), conteos/rangos/velocidades y fuentes oficiales; JSON y JS empaquetado coinciden. | Superada |
| K02 · Fabricante y modelos filtrados | Editor filtra fabricante/tipo, sin modelo para AP; cancelación no cambia datos. | Listas por marca/rol; AP y roles no soportados sin modelos; cancelación intacta. | Superada |
| K03 · Carga automática de inventario | Seleccionar modelo muestra interfaces documentadas, sin escribir nombres ni guardar datos preliminares. | 28 puertos de ficha visibles inmediatamente; guardar equipo asigna enlaces; sin entrada manual de puertos. | Superada |
| K04 · Cisco con modelo | Catalyst seleccionado usa nombres reales en toda la CLI física, conservando IPv4/HSRP. | Catalyst: 8 puertos de ficha en CLI, HSRP/IP conservados; cero nombres físicos genéricos. | Superada |
| K05 · Huawei con modelo | Switch L2 seleccionado usa banco RJ45 de la variante, sin atribuirle L3 ni SFP no verificados. | Huawei L2: nombres del banco RJ45 de ficha; sin SFP no verificados ni routing de core. | Superada |
| K06 · Fortinet con modelos | 60F/61F/70F usan wan1/wan2/dmz y excluyen puertos de switch interno/FortiLink. | Tres modelos FortiGate: puertos exactos de tablas oficiales; internal1–5 y a/b no asignados automáticamente. | Superada |
| K07 · MikroTik con modelos | hEX, hEX S y CCR2004 usan puertos de sus fichas con sintaxis RouterOS 7. | Tres routers RouterOS 7: nombres en guardas Ethernet, bridge e interfaces OSPF; sin sintaxis ajena. | Superada |
| K08 · Asignación determinista | Orden de filas/ejecuciones no cambia la asociación puerto–enlace; sin duplicados. | Mismas asociaciones al repetir/invertir nodos y enlaces; puertos físicos únicos. | Superada |
| K09 · Puertos insuficientes y atomicidad | ISR4321 de dos GE rechaza tres enlaces sin inventar puertos ni perder proyecto/DOM. | Tres enlaces frente a dos GE reales: rechazo atómico, sin puerto ficticio ni pérdida de plan, CLI, DOM o localStorage. | Superada |
| K10 · Duplicados y referencias importadas | Importador rechaza puertos repetidos/no existentes del modelo sin reasignar ni sustituir estado. | Puerto duplicado y puerto 99 inexistente rechazados sin asignación automática durante importación. | Superada |
| K11 · Cambio de modelo | Cambiar 24T por 48T conserva puertos válidos, enlaces, VLAN, direcciones y otras sedes. | 24T→48T mantiene puertos válidos y todo el direccionamiento/identidad; cambia únicamente modelo e invalida CLI derivada. | Superada |
| K12 · Regeneración con modelos | Reconstruir topología conserva modelo, IDs y puertos válidos de nodos automáticos. | Modelo, identificadores, puertos y plan conservados al reconstruir desde el mismo plan. | Superada |
| K13 · JSON v4 y almacenamiento | Guardar/cargar/importar conserva modelId y puertos; cero llamadas a asignadores IPv4/IPv6. | v4/CLI/modelId/enlaces exactos en JSON y localStorage; no se reasignan redes al cargar. | Superada |
| K14 · Proyectos antiguos y advertencia | v2/v3/v4 sin modelo preservan datos y generación genérica, con advertencia visual. | v2/v3 migran a v4 sin modelo inferido; CLI genérica permanece y aviso exacto visible; referencias históricas en C26. | Superada |
| K15 · Fabricantes mixtos con catálogo | Cuatro marcas reales usan modelos compatibles de la misma topología y plan común. | Cisco core, Huawei acceso, Fortinet firewall y MikroTik router con modelos documentados; cuatro CLI y plan común intacto. | Superada |
| K16 · AP excluidos con vecinos modelados | AP mantiene IP/VLAN/enlaces; ningún adaptador ni modelo ofrece CLI genérica para AP. | AP sin modelos/CLI genéricos; nodos/IP/VLAN/enlaces siguen intactos al seleccionar modelos vecinos. | Superada |
| K17 · Funcionamiento sin internet | Catálogo cargado localmente; seleccionar, asignar, generar y exportar funciona desconectado. | Selección, VLSM, topología, asignación, CLI y JSON operan con red desactivada tras cargar activos locales; cero consultas externas. | Superada |
| K18 · Catálogo ES/EN y responsive | Controles, mensajes e inventario traducidos; modelo y CLI intactos a 1440/390 px. | Catálogo y avisos en ES/EN, 1440/390 sin desborde nuevo; modelo, redes y CLI conservados. | Superada |
| K19 · Entradas inseguras y modelos incompatibles | Modelo desconocido/inyección/tipo incorrecto rechazados atómicamente en selección e importación. | Selección de ID desconocido, inyección y fabricante/tipo incompatible bloqueados; JSON inválido conserva estado. | Superada |
| K20 · ISR4321 y función no respaldada | Dos GE físicos generan en router compatible; funciones fuera del perfil se bloquean con causa específica. | ISR4321 usa sus dos GE sin switchport; LACP no respaldado en perfil Huawei bloquea generación con mensaje concreto. | Superada |
| K21 · Medios y velocidades compatibles | Uplink óptico entre modelos conocidos usa puertos/velocidad común; medio incompatible se rechaza al importar. | SFP1↔uplink SFP Catalyst con 1G común; fibra↔RJ45 incoherente rechazada sin inventar transceptor ni cambiar estado. | Superada |
| K22 · Catálogo ausente y modo legado | Sin archivo de catálogo los proyectos sin modelo siguen funcionando con aviso; no se consulta internet. | Sin catálogo: flujo genérico y CLI permanecen; aviso local visible, sin descarga ni consulta externa. | Superada |
| K23 · Crear enlaces sin escribir puertos | Enlaces nuevos reciben puertos del modelo; las asociaciones válidas previas quedan reservadas. | Enlace Fortinet↔Catalyst añadido sin escribir puertos; conserva enlaces anteriores y no duplica interfaces. | Superada |

El reporte HTML contiene también los 73 casos conservados, tiempos y evidencia observable; el JSON SSH conserva los 26 resultados individuales. Durante desarrollo se detectaron y corrigieron un sombreado de nombre en el editor y la validación indebida de la columna alternativa de un enlace con modelo; el conjunto final se ejecutó completo tras esas correcciones. Un ID erróneo en un caso nuevo se corrigió sin rebajar la validación de producción. No se cuentan repeticiones como casos nuevos.

**Comprobaciones complementarias:** `node --check` para script principal y catálogo, compilación Python en memoria, parser HTML5 sin errores, `git diff --check`, enlaces locales y escaneo de secretos/temporales. Revisión visual de selector/inventario a 1440 px ES y 390 px EN, sin desbordes nuevos. Las imágenes de revisión son scratch, no reemplazan las capturas académicas históricas. No se ejecutaron pruebas Windows ni validación física; la exploración `file://` bloqueada se informa aparte. La seguridad/conectividad real no se deduce del 100% local.

Para sustentación: ejecutar el comando completo; abrir la app por HTTP, generar plan/topología, elegir fabricante/modelo y revisar puertos; demostrar mensaje atómico al elegir un modelo insuficiente y guardar/exportar/importar v4. Mostrar los límites por modelo y que AP permanece sin CLI. Toda propuesta se revisa manualmente; nunca ejecutarla desde la prueba.

## Registro anterior del PR #10: interfaces automáticas y orden del menú

Base de trabajo `9675ce7f1c553e1225609772cbb6a500822fa2f0`; main conservado en `1956d1872363c88399f5e8240abb1d7a13bca340`. Ejecución 2026-11-11T13:02:18-05:00: **73/73 aplicación + 26/26 SSH local = 99/99 (100%)**, 0 fallidas/bloqueadas/no ejecutadas dentro de las matrices. Se mantienen los 58 casos C/N/P y los 26 SSH; Q04–Q13 cambian sus expectativas porque se retiró expresamente el formulario físico, y Q15 verifica el nuevo menú. No se alteraron fixtures ni hashes CLI de referencia. [Resultados y límites](pruebas-interfaces.md), [reporte real](../tests/reporte-interfaces.html).

Se elimina la confirmación manual de interfaces: los cuatro adaptadores vuelven a tomar puertos automáticamente de los enlaces, sin pedir modelo/versión/URL/perfil. El aviso de revisar hardware es visual. AP conserva inventario, topología y administración, excluido de CLI genérica. El menú agrupa Cisco → Huawei → Fortinet → MikroTik → Comparación → Ciberdefensa; permanecen las demás vistas, ES/EN, flechas y progreso. La confirmación del plan VLAN/VLSM, fabricantes mixtos, IPv4/IPv6, JSON v2/v3/v4 y SSH se conservan. Los perfiles v4 antiguos permanecen como metadatos/CLI archivada, sin controlar propuestas nuevas ni exigir confirmaciones.

## Registro anterior: confirmaciones y consola SSH (84 casos)

Código sobre el HEAD de referencia PR #10 `194a43e`; véanse [manual SSH](manual-ssh.md), [servicio opcional](../ssh_service/README.md) y [pruebas actuales](pruebas-ssh.md). **58/58 UI + 26/26 SSH local = 84/84 ejecutadas**; una comprobación exploratoria file:// bloqueada por política se declara aparte. Windows y fabricantes físicos no ejecutados.

Sedes: confirmed opcional v4 validado, resumen verde/Editar y protección contra cambios accidentales; ausencia en proyectos antiguos no se interpreta como confirmación. Se conserva invalidación selectiva. VLAN: previsualización pendiente/efectiva por sede, mensajes de capacidad y aprobación efectiva; errores preservan estado y formulario.

Consola SSH: módulo 14 con simulación autónoma de comandos cerrados y conexión real opcional HTTP/WS→AsyncSSH con PTY/xterm local. La conexión manual es independiente de VLSM. Origen/Host, autorización local, allowlist, claves de host, timeouts, cuotas, buffers/ACK y limpieza de sesiones verificados. Credenciales/historial real nunca entran en JSON o localStorage. No se envían configuraciones automáticamente.

**El contenido restante conserva el registro de la revisión anterior de 50 casos; no es el resultado actual ni se suma dos veces.**

## Registro anterior: revisión integral de las nueve correcciones

- Base main: `1956d1872363c88399f5e8240abb1d7a13bca340`; rama `fix/revision-integral-wan-architect`.
- Código ejecutado: `8a27f672e03b6e777b077a8910915d13adeb7127`; suite identificada por hash antes de su commit separado.
- Fecha: 2026-11-09T23:32:21-05:00 · America/Bogota; Linux-6.18.57-x86_64-with-glibc2.41; Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57.
- **50/50 = 100% del conjunto ejecutado**: 0 fallidas, 0 bloqueadas y 0 no ejecutadas. C01–C31 anteriores y N01–N19 nuevas. Duración de casos: 50.9 s.
- [Reporte actual real](../tests/reporte-revision-integral.html); HTTP local y un contexto limpio por caso. Ninguna configuración se ejecuta en equipos.
- Aplicación SHA-256: `8f70a30e21a2c47677a0f0f0e29b40153391cbe872eb8f7c07a9b8848debb19a`.
- Suite SHA-256: `f0f87a84b095a636017b9158ee42cec2fb590a3be691d91b1649245e000d8221`.
- Fixture histórica v4 SHA-256: `5c7297c10ff21f837d1cfabaca762968e51b01745a759d41603b54e701cdade2`.

Instalación y comando continúan iguales:

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
```

No se añaden dependencias del proyecto. El runner inicia/cierra servidor y navegador, devuelve no cero si falla y produce reporte temporal por defecto. Para registrar expresamente esta revisión: `python tests/test_corte3.py --report tests/reporte-revision-integral.html`. No sustituir la captura 09 histórica con un resultado no renderizado.

### Esperado, obtenido y estado de la ejecución actual

| Caso | Esperado | Obtenido / evidencia | Estado |
| --- | --- | --- | --- |
| C01 · Calculadora IPv4 | 192.168.10.50/26: red .0, broadcast .63 y 62 hosts; /31 y /32 correctos. | Red 192.168.10.0/26, broadcast .63, 62 hosts; límites /31 y /32 verificados. | Superada |
| C02 · Calculadora IPv6 | 128 bits exactos, forma canónica, clasificación y broadcast no aplicable. | 6 vectores frente a ipaddress, 8 categorías y /64 = 18446744073709551616 direcciones. | Superada |
| C03 · Migración v2 → v3 → v4 | Migrar sin reasignar ni perder plan, topología, opciones o CLI válidas. | v2→v4 sin asignar; 15 VLAN, 28 nodos, 34 enlaces y 4 CLI preservados. | Superada |
| C04 · Migración v3 → v4 y JSON | Migrar v3 y exportar/importar v4 sin cambiar datos ni llamar asignadores. | v3→v4 e ida/vuelta JSON exactos; cero llamadas a allocate/allocateIPv6. | Superada |
| C05 · Persistencia local v2/v3/v4 | Priorizar v4, migrar fallbacks y no sobrescribir claves antiguas. | v4 prioritario y restaurado; fallback v3/v2 en memoria; contenido antiguo intacto. | Superada |
| C06 · Eliminar VLAN sin perder ediciones | Conservar nombre/hosts pendientes; cancelar o validar mal no debe eliminar/renderizar. | Solo se eliminó la tercera VLAN; nombre/hosts conservados; cancelar e inválido atómicos. | Superada |
| C07 · IPv4 por sede y CIDR manual | Asignar dentro de pools, respetar manuales y separar /30 sin solapamientos. | 19 redes disjuntas; manuales 10.20.20.0/24 y 10.20.35.0/24 conservadas. | Superada |
| C08 · Error IPv4 atómico | Entrada incompatible debe conservar estado, derivados, almacenamiento y texto. | CIDR fuera del bloque rechazado: estado/CLI/DOM/localStorage intactos. | Superada |
| C09 · Planificación IPv6 | Asignar /48→/56→/64 de modo estable, con reservas según redundancia. | 15 /64 disjuntas; /56 manual reservado; orden estable, reservas e ida/vuelta exactos. | Superada |
| C10 · Error IPv6 atómico | Insuficiencia o solapamiento no deben reemplazar planes ni formulario. | Capacidad /56 insuficiente y sedes solapadas rechazadas sin pérdidas. | Superada |
| C11 · Topología e interfaces | Los enlaces routed deben usar las /30 y extremos reales del plan confirmado. | 40 nodos, 46 enlaces; 4 /30 coherentes y sin bloqueos. | Superada |
| C12 · Cisco IOS / IOS XE (texto) | Generar VLAN/SVI, IP, DHCP y OSPF del plan sin mezclar fabricantes. | 14 textos Cisco; VLAN, gateways, OSPF y DHCP del plan, sin gramáticas ajenas. | Superada |
| C13 · Huawei VRP (texto) | Generar Vlanif, IP, DHCP y OSPF del plan en gramática VRP separada. | 14 textos Huawei; VLAN, gateways, OSPF y DHCP del plan, sin gramáticas ajenas. | Superada |
| C14 · Fortinet FortiOS 7.4 (texto) | Interfaces/VLAN/IP, DHCP o relay, rutas y administración restringida desde datos reales. | IP/máscaras reales; estructura CLI balanceada; DHCP, relay, OSPF, rutas y local-in verificados. | Superada |
| C15 · MikroTik RouterOS 7 (texto) | Bridge/VLAN/IP, OSPF v7, DHCP/relay y forward bloqueado por defecto. | Bridge/VLAN y gateways reales; OSPF v7, DHCP/relay, servicios/MAC y forward drop verificados. | Superada |
| C16 · Separación de cuatro fabricantes | Cada adaptador usa su gramática; los nuevos equipos no caen en IOS/VRP. | IOS, VRP, FortiOS y RouterOS separados; MikroTik excluido de equivalencias Cisco/Huawei. | Superada |
| C17 · Entradas inseguras e importación | Rechazar hostname, puertos, CIDR y versión peligrosos sin sustituir el estado. | 4 payloads inseguros/futuros rechazados; estado y almacenamiento intactos. | Superada |
| C18 · Sintaxis JavaScript y consola | Compilar los scripts, cargar la app y no registrar errores JS ni solicitudes externas. | 1 script compilado por Chromium; consola/página limpias; sin solicitudes externas. | Superada |
| C19 · Descargas reales | Descargar JSON v4, una propuesta y el conjunto sin alterar su texto. | CLI individual exacta, 14 propuestas en descarga conjunta y JSON v4 exacto. | Superada |
| C20 · Responsive 1440 / 390 px | Calculadora y planificación IPv6 caben en página y muestran límites IPv4. | 12 combinaciones etapa/viewport sin desbordamiento de página; avisos IPv4 visibles. | Superada |
| C21 · Español predeterminado | Contexto limpio: lang=es, selector Español y navegación española. | Español inicial, selector accesible y preferencia todavía no escrita. | Superada |
| C22 · Vistas ES/EN | Las 13 vistas y editores muestran títulos, etiquetas y controles traducidos. | 13 vistas × 2 idiomas y 4 variantes de editor × 2; títulos y navegación con Enter. | Superada |
| C23 · Mensajes y confirmaciones bilingües | Errores, guardado y confirmación nativa traducidos sin cambiar datos introducidos. | Validación IPv4/IPv6, guardado, cancelación y advertencias dinámicas comprobados en ES/EN. | Superada |
| C24 · Persistencia independiente del idioma | Idioma persiste tras recargar sin entrar en JSON ni borrar proyectos. | Clave WAN-Architect-language independiente; recarga/carga/nuevo conservan la preferencia. | Superada |
| C25 · Cambio de idioma atómico | Estado, CLI, JSON, campos pendientes y nombres permanecen exactamente iguales. | Estado e imageData idénticos; nombres iguales a claves de catálogo, CLI y ediciones inválidas conservados. | Superada |
| C26 · Salidas de cuatro fabricantes contra main | Hashes de CLI idénticos a main 6ac46f9 en español e inglés. | 8 comparaciones exactas: 4 fabricantes × ES/EN, referencias de main 6ac46f9. | Superada |
| C27 · Inventario de controles | Todo button tiene handler; importadores accesibles y controles sin acción ausentes. | 62 plantillas button con handler; 2 importadores de archivo y 1 selector de idioma accesibles; 0 controles decorativos detectados. | Superada |
| C28 · Acciones observables de botones | Cada familia de botones ejecuta render, estado, validación, diálogo, copia, descarga o impresión. | 56 familias/objetivos activados con Enter; 38 handlers, descargas, impresión invocada y validaciones observables. | Superada |
| C29 · Portapapeles e importadores con teclado | Copia real, descarga intacta y file chooser accesible; fallback selecciona CLI. | Clipboard/CLI exactos; fallback e importadores por teclado; HTML, CSV y SVG con interfaz/nombres en inglés. | Superada |
| C30 · Responsive bilingüe | Navegación, idioma y controles caben a 1440 y 390 px en ES/EN. | 48 combinaciones vista/idioma/ancho sin desbordamiento de página; selector visible. | Superada |
| C31 · Catálogo y atributos traducibles | Todas las claves literales t() y atributos de formulario tienen traducción; opciones conservan valores internos. | 520 claves literales cubiertas; placeholder, aria-label y valores de opciones comprobados. | Superada |
| N01 · Pools RFC1918 independientes | Dos sedes en rangos privados distintos y tránsito independiente, LAN contenidas y redes disjuntas. | 15 VLAN en 192.168.64.0/22 y 10.20.0.0/22; /30 en 192.168.200.0/24; JSON conserva el plan. | Superada |
| N02 · Errores de bloque atómicos | Rechazar solapamiento, red desalineada, pública y capacidad insuficiente sin mutaciones. | CIDR desalineado/público/prefijo inválido y solapamiento rechazados; insuficiencia /24 conserva estado. | Superada |
| N03 · VLAN manual independiente y fallback | Manual dentro de sede, fallback global sin invasión; error manual conserva texto y plan. | Manual en sede independiente, automáticas en pools correctos; manual exterior rechazada sin perder texto/plan. | Superada |
| N04 · Inventario confirmado sin invalidación superflua | Formulario inicial, resumen, editar y confirmar cantidades idénticas conservando plan/topología/CLI. | Formulario→resumen→editar; mismas cantidades conservan plan, nodos y CLI. | Superada |
| N05 · Inventario editado y borradores | Conservar borrador al navegar; cambio real invalida únicamente sede afectada. | Borrador conservado al navegar; cambio s1 conserva VLAN, LAN y equipos de s2. | Superada |
| N06 · Restauración de inventario confirmada | Cancelar restauración conserva cantidades; aceptar restaura estimación y su disponibilidad. | Cancelación intacta; restauración explícita vuelve a 100 PCs estimados. | Superada |
| N07 · Confirmación VLAN y dependencias | Sin cambios conserva derivados; borrador bloquea generación, conserva valores al navegar y permite confirmar. | Confirmación idéntica conserva todo; edición pendiente bloquea dependencias y conserva formulario. | Superada |
| N08 · Componentes retirados y navegación | 13 módulos, sin Evidencias Corte 2 ni explicaciones retiradas; calculadoras intactas. | 13 módulos navegables, explicaciones ausentes; red/broadcast /26 correctos. | Superada |
| N09 · Topología mixta real | Cisco router, Huawei core/switch, Fortinet firewall y MikroTik router secundario con puertos reales. | Cuatro fabricantes reales generados; perfiles, autoKey, puertos y equipos conservados en JSON. | Superada |
| N10 · Perfiles y roles inválidos | Sin elección no genera; roles incompatibles/importación arbitraria se rechazan atómicamente. | Sin perfil explícito no genera; firewall/switch, core/RouterOS y campos arbitrarios rechazados. | Superada |
| N11 · Regeneración estable y equipos manuales | Reorganizar/regenerar no elimina manuales ni cambia IDs de nodos/enlaces automáticos. | Manual conservado; IDs automáticos y enlaces estables tras regenerar y reorganizar. | Superada |
| N12 · Lienzo, zoom, arrastre y SVG | Iconos autónomos, cajas separadas, zoom/arrastre y exportación SVG funcionales. | Sin cajas superpuestas; zoom y arrastre reales; SVG con iconos inline; 1440/390 sin desborde de página. | Superada |
| N13 · Bilingüismo de nuevos controles | Nuevos perfiles, inventario, aprobación y diagrama traducidos sin cambiar datos. | Perfiles, zoom/reorganización y confirmación en inglés; proyecto intacto. | Superada |
| N14 · Sede sin cambios y dependencias locales | Confirmar ficha idéntica no borra nada; cambiar bloque conserva datos de otra sede. | Guardar sin cambios conserva todo; nuevo pool solo invalida dependencias de la sede. | Superada |
| N15 · Recalcular sin renumerar otra sede | Cambiar hosts s1 conserva redes, tránsito, nodos y CLI válidas s2, incluso tras JSON. | Redes/tránsito, IDs y CLI no afectadas de s2 idénticas; vecino WAN se invalida por enlace afectado, JSON conserva las restantes. | Superada |
| N16 · Nombres únicos y gran diagrama | Códigos de sedes sin colisiones, 100 equipos sin cajas superpuestas, reorganización determinista. | 140 equipos sin superposición de cajas; códigos desambiguados y posiciones deterministas. | Superada |
| N17 · Borradores aislados entre proyectos | Cargar laboratorio o proyecto nuevo elimina borradores anteriores sin cambiar idioma. | Borradores preservados en navegación y eliminados solo al reemplazar proyecto; idioma conservado. | Superada |
| N18 · Editar sede conserva intención manual válida | Cambio de bloque incompatible con CIDR manual se rechaza sin sustituir estado ni formulario. | Cambio de pool incompatible con manual rechazado; estado, plan y texto conservados. | Superada |
| N19 · Repropuesta parcial conserva otras sedes | Cambiar inventario y completar VLAN faltantes conserva CIDR, claves y plan de otra sede. | Solo se completaron VLAN de s1; claves/CIDR manual/plan de s2 intactos y VLSM válido. | Superada |

### Integridad de las referencias y límites

Los hashes de `tests/fixtures/generator-reference.json` permanecen intactos. La nueva fixture `pre-revision-v4.json` se capturó realmente desde el HTML de main 1956d18 y el mismo laboratorio de C26; conserva IDs/nombres/plan previos. C26 importa ese proyecto y verifica plan IPv4, IPv6, topología histórica y ocho CLI (cuatro marcas × ES/EN). No se regeneraron hashes para esconder cambios: nombres, posiciones y terminales representativos de las nuevas topologías sí cambian por autorización explícita.

Las pruebas de Huawei distinguen asignación real y equivalencia: C13 selecciona Huawei; los escenarios monofabricante que comparan gramáticas usan Comparación expresamente, no un fallback implícito de `configNodes()`. Se actualizan índices 10/11/12, etiquetas de confirmación y cantidad de vistas conforme a la eliminación autorizada; no se omiten casos anteriores.

Verificaciones adicionales: `node --check`, compilación Python, diff-check y revisión de secretos/enlaces. html5lib 1.1, instalado solo como herramienta temporal fuera del repositorio, analizó el documento y 26 fragmentos originales de vistas ES/EN sin errores; el SVG exportado se verificó como XML. No se añade html5lib al runner ni se afirma certificación W3C/WCAG.

Revisión visual con Playwright: resumen de inventario, topología mixta de 44 nodos/51 enlaces y vista English a 390 px; diagramas con iconos originales, rutas fuera de cajas, hover/tablas para detalles y scroll. N16 comprueba 140 cajas sin superposición tras organizar. No se garantiza ausencia de todos los cruces de enlaces ni de superposiciones introducidas manualmente. C20/C30/N12 mantienen validación 1440/390 px.

Confirmación sin cambios conserva diseño; el borrador bloquea dependencias sin sustituir el estado confirmado. N15 conserva CLI no afectadas de otra sede; el vecino WAN pierde su CLI cuando cambia su enlace, por coherencia. N18 rechaza pools incompatibles con manuales guardadas y N19 completa VLAN faltantes sin reemplazar otras sedes.

Este 100% es `50 superadas / 50 ejecutadas × 100`, no cobertura absoluta, auditoría completa, interoperabilidad ni validación física. Los generadores continúan siendo IPv4. IPv6, ciberdefensa, JSON v2/v3/v4, localStorage, botones, portapapeles y descargas permanecen en la regresión. Las capturas 01–10, el reporte anterior y los PDF no se modifican: corresponden a la entrega histórica anterior.

## Registro histórico: entrega bilingüe fusionada en main 1956d18

**Las secciones restantes conservan su fecha, versión, reporte de 31 casos y capturas anteriores. No describen la ejecución actual ni se suman al denominador de 50.**


## Fuente, entorno y resultado registrado

- Rama: `feature/i18n-evidencias-finales`; base main `6ac46f9257143f88ec8cb7b47c020bb3739adbfa`.
- Commit del código ejecutado: `71d56cb469a1f9049d24fc0bf2804adefdd256db`. La suite actualizada se identifica por hash y se publica en el commit de pruebas; esta ejecución precede a ese commit.
- Fecha real: **2026-11-09T22:16:36-05:00**, America/Bogota.
- Entorno: Linux-6.18.57-x86_64-with-glibc2.41; Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57.
- HTTP en 127.0.0.1 con puerto libre; contexto limpio por caso, sin datos ni infraestructura reales.
- **31/31 = 100% del conjunto ejecutado**; superadas 31, fallidas 0, bloqueadas 0, no ejecutadas 0.
- Duración del reporte: 38.8 s; aproximadamente 39 s en esta ejecución con capturas. No se suman repeticiones como casos nuevos.
- [Reporte HTML real](../tests/reporte-corte3.html) y [captura 09 nueva](capturas/09-pruebas.png), producidos por la misma ejecución. No se editaron resultados o imagen manualmente.

## Instalación y comando

Python 3.10+ y las dependencias de [tests/requirements.txt](../tests/requirements.txt); solo Playwright fijado, sin Node/pytest ni servicios externos para ejecutar la suite:

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
```

El runner inicia y cierra automáticamente el servidor local, imprime cada caso y devuelve código no cero si falla o queda bloqueado. Guarda el reporte normal fuera del repositorio e imprime su ruta. Puede usar Chromium del sistema automáticamente o mediante `--browser /ruta/chromium` / `CHROMIUM_EXECUTABLE`.

Para actualizar expresamente la evidencia versionada, tras revisar el resultado:

```bash
python tests/test_corte3.py --report tests/reporte-corte3.html --capture docs/capturas/09-pruebas.png
```

Este comando sí sustituye ambos artefactos; la ejecución normal no los sobrescribe. La prueba compila JavaScript en Chromium y revisa errores de consola/página y solicitudes externas en cada contexto.

## Casos, esperado, obtenido y estado

C01–C20 conservan la regresión anterior; C21–C31 cubren la nueva interfaz y sus controles. Cada fila es un caso ejecutado, no una estimación basada en existencia de código.

| Caso | Esperado | Obtenido / evidencia observable | Estado |
| --- | --- | --- | --- |
| C01 · Calculadora IPv4 | 192.168.10.50/26: red .0, broadcast .63 y 62 hosts; /31 y /32 correctos. | Red 192.168.10.0/26, broadcast .63, 62 hosts; límites /31 y /32 verificados. | Superada |
| C02 · Calculadora IPv6 | 128 bits exactos, forma canónica, clasificación y broadcast no aplicable. | 6 vectores frente a ipaddress, 8 categorías y /64 = 18446744073709551616 direcciones. | Superada |
| C03 · Migración v2 → v3 → v4 | Migrar sin reasignar ni perder plan, topología, opciones o CLI válidas. | v2→v4 sin asignar; 15 VLAN, 28 nodos, 34 enlaces y 4 CLI preservados. | Superada |
| C04 · Migración v3 → v4 y JSON | Migrar v3 y exportar/importar v4 sin cambiar datos ni llamar asignadores. | v3→v4 e ida/vuelta JSON exactos; cero llamadas a allocate/allocateIPv6. | Superada |
| C05 · Persistencia local v2/v3/v4 | Priorizar v4, migrar fallbacks y no sobrescribir claves antiguas. | v4 prioritario y restaurado; fallback v3/v2 en memoria; contenido antiguo intacto. | Superada |
| C06 · Eliminar VLAN sin perder ediciones | Conservar nombre/hosts pendientes; cancelar o validar mal no debe eliminar/renderizar. | Solo se eliminó la tercera VLAN; nombre/hosts conservados; cancelar e inválido atómicos. | Superada |
| C07 · IPv4 por sede y CIDR manual | Asignar dentro de pools, respetar manuales y separar /30 sin solapamientos. | 19 redes disjuntas; manuales 10.20.20.0/24 y 10.20.35.0/24 conservadas. | Superada |
| C08 · Error IPv4 atómico | Entrada incompatible debe conservar estado, derivados, almacenamiento y texto. | CIDR fuera del bloque rechazado: estado/CLI/DOM/localStorage intactos. | Superada |
| C09 · Planificación IPv6 | Asignar /48→/56→/64 de modo estable, con reservas según redundancia. | 15 /64 disjuntas; /56 manual reservado; orden estable, reservas e ida/vuelta exactos. | Superada |
| C10 · Error IPv6 atómico | Insuficiencia o solapamiento no deben reemplazar planes ni formulario. | Capacidad /56 insuficiente y sedes solapadas rechazadas sin pérdidas. | Superada |
| C11 · Topología e interfaces | Los enlaces routed deben usar las /30 y extremos reales del plan confirmado. | 28 nodos, 34 enlaces; 4 /30 coherentes y sin bloqueos. | Superada |
| C12 · Cisco IOS / IOS XE (texto) | Generar VLAN/SVI, IP, DHCP y OSPF del plan sin mezclar fabricantes. | 14 textos Cisco; VLAN, gateways, OSPF y DHCP del plan, sin gramáticas ajenas. | Superada |
| C13 · Huawei VRP (texto) | Generar Vlanif, IP, DHCP y OSPF del plan en gramática VRP separada. | 14 textos Huawei; VLAN, gateways, OSPF y DHCP del plan, sin gramáticas ajenas. | Superada |
| C14 · Fortinet FortiOS 7.4 (texto) | Interfaces/VLAN/IP, DHCP o relay, rutas y administración restringida desde datos reales. | IP/máscaras reales; estructura CLI balanceada; DHCP, relay, OSPF, rutas y local-in verificados. | Superada |
| C15 · MikroTik RouterOS 7 (texto) | Bridge/VLAN/IP, OSPF v7, DHCP/relay y forward bloqueado por defecto. | Bridge/VLAN y gateways reales; OSPF v7, DHCP/relay, servicios/MAC y forward drop verificados. | Superada |
| C16 · Separación de cuatro fabricantes | Cada adaptador usa su gramática; los nuevos equipos no caen en IOS/VRP. | IOS, VRP, FortiOS y RouterOS separados; MikroTik excluido de equivalencias Cisco/Huawei. | Superada |
| C17 · Entradas inseguras e importación | Rechazar hostname, puertos, CIDR y versión peligrosos sin sustituir el estado. | 4 payloads inseguros/futuros rechazados; estado y almacenamiento intactos. | Superada |
| C18 · Sintaxis JavaScript y consola | Compilar los scripts, cargar la app y no registrar errores JS ni solicitudes externas. | 1 script compilado por Chromium; consola/página limpias; sin solicitudes externas. | Superada |
| C19 · Descargas reales | Descargar JSON v4, una propuesta y el conjunto sin alterar su texto. | CLI individual exacta, 14 propuestas en descarga conjunta y JSON v4 exacto. | Superada |
| C20 · Responsive 1440 / 390 px | Calculadora y planificación IPv6 caben en página y muestran límites IPv4. | 12 combinaciones etapa/viewport sin desbordamiento de página; avisos IPv4 visibles. | Superada |
| C21 · Español predeterminado | Contexto limpio: lang=es, selector Español y navegación española. | Español inicial, selector accesible y preferencia todavía no escrita. | Superada |
| C22 · Vistas ES/EN | Las 14 vistas y editores muestran títulos, etiquetas y controles traducidos. | 14 vistas × 2 idiomas y 4 variantes de editor × 2; títulos y navegación con Enter. | Superada |
| C23 · Mensajes y confirmaciones bilingües | Errores, guardado y confirmación nativa traducidos sin cambiar datos introducidos. | Validación IPv4/IPv6, guardado, cancelación y advertencias dinámicas comprobados en ES/EN. | Superada |
| C24 · Persistencia independiente del idioma | Idioma persiste tras recargar sin entrar en JSON ni borrar proyectos. | Clave WAN-Architect-language independiente; recarga/carga/nuevo conservan la preferencia. | Superada |
| C25 · Cambio de idioma atómico | Estado, CLI, JSON, campos pendientes y nombres permanecen exactamente iguales. | Estado e imageData idénticos; nombres iguales a claves de catálogo, CLI y ediciones inválidas conservados. | Superada |
| C26 · Salidas de cuatro fabricantes contra main | Hashes de CLI idénticos a main 6ac46f9 en español e inglés. | 8 comparaciones exactas: 4 fabricantes × ES/EN, referencias de main 6ac46f9. | Superada |
| C27 · Inventario de controles | Todo button tiene handler; importadores accesibles y controles sin acción ausentes. | 58 plantillas button con handler; 2 importadores de archivo y 1 selector de idioma accesibles; 0 controles decorativos detectados. | Superada |
| C28 · Acciones observables de botones | Cada familia de botones ejecuta render, estado, validación, diálogo, copia, descarga o impresión. | 54 familias/objetivos activados con Enter; 38 handlers, descargas, impresión invocada y validaciones observables. | Superada |
| C29 · Portapapeles e importadores con teclado | Copia real, descarga intacta y file chooser accesible; fallback selecciona CLI. | Clipboard/CLI exactos; fallback e importadores por teclado; HTML, CSV y SVG con interfaz/nombres en inglés. | Superada |
| C30 · Responsive bilingüe | Navegación, idioma y controles caben a 1440 y 390 px en ES/EN. | 52 combinaciones vista/idioma/ancho sin desbordamiento de página; selector visible. | Superada |
| C31 · Catálogo y atributos traducibles | Todas las claves literales t() y atributos de formulario tienen traducción; opciones conservan valores internos. | 536 claves literales cubiertas; placeholder, aria-label y valores de opciones comprobados. | Superada |

El porcentaje se calcula únicamente como `superadas / ejecutadas × 100`: 31 / 31 × 100 = 100%. No hay casos definidos bloqueados o no ejecutados en este conjunto; los límites físicos y de cobertura se explican aparte.

## Inventario y compatibilidad comprobada

58 plantillas `<button>` estáticas/dinámicas, dos importadores con rol de botón y un selector: 61 controles de esas clases. Las instancias crecen con filas/nodos; no se presenta 61 como un número fijo de botones DOM. **0 controles decorativos detectados/eliminados**. Se mantienen controles válidos con requisitos previos, se corrige disponibilidad y validación, y se documenta el [manifiesto de las 58 plantillas](manual.md).

C28 activó 54 familias/objetivos con Enter, cubriendo 38 handlers y las acciones inline de imagen/ejemplo. C29 verifica portapapeles real, descarga CLI exacta, fallback cuando las APIs no están disponibles, selección/cierre y ambos importadores con Enter/Espacio; además HTML/CSV/SVG en inglés. La prueba de impresión sustituye la API para comprobar su invocación; no demuestra impresión física.

C26 utiliza [generator-reference.json](../tests/fixtures/generator-reference.json), calculado desde el código de main 6ac46f9 y los mismos datos ficticios deterministas. Compara plan IPv4, topología, plan IPv6 y ocho hashes de CLI (cuatro fabricantes × ES/EN). La fixture no requiere scripts temporales ni infraestructura externa. La [fixture v2](../tests/fixtures/laboratorio-v2.json) permite migración v2/v3→v4 y comparación de datos; v3 se construye explícitamente desde v2, no se presenta como archivo histórico independiente.

La importación normaliza el contrato heredado: `subnetOK` es un indicador transitorio que el importador existente no reconstruye. El roundtrip de teclado usa un proyecto canonicalizado, sin cambiar ese comportamiento. Cambiar idioma, por su parte, conserva exactamente estado, imageData, campos pendientes, CLI y JSON (C25).

## Hashes y procedencia

- Aplicación, `WAN_v4.html`: `83ee8828e76848e83cd37ccb7f0c183e2cc4c34c5a81589a1e2cc6bd00ca6176`.
- Suite, `tests/test_corte3.py`: `41733e437257e7fbf9ca761c2d99752656ad90cb0dcf5ae27d787ec8840f3ba7`.
- Fixture v2, `tests/fixtures/laboratorio-v2.json`: `ac1b430c4f5cf9034495ada9462571c65810e3f50fc59a0f8fb2187c4a03551f`.
- Referencias de planes/CLI, `tests/fixtures/generator-reference.json`: `7dbee4554f5351d91e27476dc6d72b58108af0631389c282ee77d9531d9c4731`.
- Reporte, `tests/reporte-corte3.html`: `6d272c01f3fa5f073d3c69f53a8826440c6d9f65587c2a57aadcf46c57bc0531`.
- Informe PDF, `docs/informe-corte3.pdf`: `db3f5bd2336127d920412c32d8d79fd06c3156622ed481df56ac8cddf2872501`.

Las capturas 01–04/06–08/10 se regeneraron porque la interfaz y/o los recortes anteriores quedaron desactualizados; la 05 faltaba y la 09 cambió de total. Capturas de app: Playwright, HTTP local, contextos limpios y datos ficticios; mismos bytes de aplicación que la ejecución registrada. Ver escenarios concretos en el manual.

| Archivo | Fecha / fuente real | SHA-256 del PNG |
| --- | --- | --- |
| [01-subnetting.png](capturas/01-subnetting.png) | 2026-11-09T22:16:37-05:00 | `b83d830e9c31921e79c31284c575f135d56382cf81de4030e36a5156f6304e5d` |
| [02-topologia.png](capturas/02-topologia.png) | 2026-11-09T22:16:45-05:00 | `fc3a569ea2237d30a6421264ad6184c2e0e08af516bb416ab0f781845a40bddb` |
| [03-config-cisco.png](capturas/03-config-cisco.png) | 2026-11-09T22:16:51-05:00 | `506f17cd771b5d4cda444b630e0cbd7d4e645adfa21f711f345e2290f7fde4b5` |
| [04-config-huawei.png](capturas/04-config-huawei.png) | 2026-11-09T22:16:57-05:00 | `f3d5bb1482a46dfd57354590302fc277314e27528edbda09670def7f6b9d6d02` |
| [05-github-commits.png](capturas/05-github-commits.png) | GitHub main 6ac46f9, captura de sesión 08/11/2026; acceso HTTPS 200 ratificado 09/11/2026 | `6eef39a7cd5292f521c140e9c7ac6ae156aa584f996d1ffd2fe97f9d5e777a90` |
| [06-config-fortinet.png](capturas/06-config-fortinet.png) | 2026-11-09T22:17:04-05:00 | `8196c4f2de3926e25c04b4caa48e67432d5d058d3475d3beeed2ceff2586b111` |
| [07-config-mikrotik.png](capturas/07-config-mikrotik.png) | 2026-11-09T22:17:11-05:00 | `310053fa6a347d23d709d02ae9a8be6e5c89412a0f7407d4d507857383175e3b` |
| [08-ciberdefensa.png](capturas/08-ciberdefensa.png) | 2026-11-09T22:17:12-05:00 | `a2daa89ccb8d11555215e21526c002629e66e606cc75d266c522dad23edc243d` |
| [09-pruebas.png](capturas/09-pruebas.png) | Ejecución 2026-11-09T22:16:36-05:00 | `842554e8f332fe630a8f9545449d3a81ded13964d470bd595ce7a396a46e6eb6` |
| [10-app-final.png](capturas/10-app-final.png) | 2026-11-09T22:17:19-05:00 | `bdc8bf8a61e7ef8dba722c48d7a59a0535573450a531cee30c5ed05a824d3d8c` |

05 corresponde a la página real `https://github.com/Daisy-redeswan/redes-wan-Rodriguez/commits/main/`. Se obtuvo respuesta HTTPS 200 con TLS verificado mediante el proxy de confianza y se renderizaron los bytes auténticos recibidos en Chromium. Los recursos externos de estilo/avatar fueron bloqueados: se conserva el render nativo sin reconstruir mensajes ni modificar el DOM. Hay al menos cinco mensajes claros; no se fabricaron commits ni una página a partir de datos de API.

## Revisión documental y visual

Se revisaron visualmente las diez capturas: IP/prefijo/red/broadcast/hosts en 01; diagrama completo en 02; hostname/sysname, VLAN e IP en 03/04; historial real en 05; generación Fortinet/MikroTik en 06/07; rechazo real en 08; X/Y/porcentaje en 09; aplicación y selector en 10. Los escenarios reducido, perimetral e integrado son alternativos; no se combinan gateways duplicados.

`docs/informe-corte3.pdf`: **23 páginas**. Se creó `document-plan.md` como scratch fuera del repositorio; se renderizaron y revisaron las 23 páginas, texto, tablas, márgenes, imágenes y enlaces. Se corrigió una frase de límites y se comprobó que las otras 22 páginas fueran idénticas; la página modificada se volvió a revisar. `pdfinfo` confirma estructura/páginas, `pdftotext` extrae texto y fuentes embebidas conservan acentos. Los detalles de 09 se dividen entre filas solo en el PDF para legibilidad; el PNG no se altera.

README sigue el orden de la plantilla e incluye autoevaluación Sí/No con evidencia. Identidad autorizada: Daisy Jurleny Rodriguez · Fundación Universitaria Compensar; sin campos académicos vacíos. `.gitignore` excluye .env/.env.* y cachés, permite .env.example y no oculta entregables. Revisión de alcance, enlaces, secretos y temporales antes de publicar; AGENTS.md e informe Corte 2 se conservan.

## Límites

Validación local de navegador y texto; nunca se ejecutó CLI en equipos/simuladores. No certifica modelos, firmware, forwarding, convergencia, conectividad, resistencia a ataques ni toda la gramática de cada SO. Cisco/Huawei no tienen modelo/versión físicos confirmados; FortiOS 7.4 genérico sin multi-VDOM y RouterOS 7.x sin VRF/CAPsMAN son supuestos autorizados.

Los cuatro generadores siguen siendo IPv4; IPv6 es cálculo/planificación ULA, sin DHCPv6/SLAAC avanzado/NAT66 ni políticas IPv6. El alcance de comandos IPv6 requiere aclaración académica. Pools DHCP/reservas editables e invalidación histórica de saveSite() quedan fuera de alcance. C30 cubre 1440/390 px; no certifica todos los anchos/navegadores ni accesibilidad completa. Las matrices históricas M/S/A/C/V no se repitieron ni sumaron al 31/31.

## Procedimiento de sustentación

1. Abrir el repositorio/versión e identificar estado v4 y cuatro adaptadores; explicar que las CLI son propuestas.
2. Mostrar español inicial, cambiar a English y comprobar que nombres, CIDR, planes y CLI no se traducen ni se pierden ediciones pendientes.
3. Demostrar cálculo IPv4/IPv6, VLAN/pools y topología; generar propuestas por fabricante usando escenarios compatibles del manual.
4. Ejecutar `python tests/test_corte3.py` en una terminal visible, esperar C01–C31 y explicar X/Y/porcentaje; ante fallo, exponer el diagnóstico y no reutilizar una imagen de éxito como resultado nuevo.
5. Abrir el reporte recién generado y contrastar esperado/obtenido. La captura 09 es evidencia fechada de su ejecución identificada, no un resultado permanente.
6. Mostrar informe/capturas y explicar límites físicos, políticas, marcadores y permisos. Esta preparación no equivale a una sustentación ya realizada.
