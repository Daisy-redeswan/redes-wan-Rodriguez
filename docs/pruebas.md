# Pruebas reproducibles de WAN Architect — Corte 3

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
