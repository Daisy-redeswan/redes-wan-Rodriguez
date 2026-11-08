# Estado de WAN Architect

## Alcance y referencia

Repositorio: `https://github.com/Daisy-redeswan/redes-wan-Rodriguez`.
Rama de esta documentación: `docs/instrucciones-codex`.
Base verificada de `origin/main`: `6f45dc1e54051a2467241ee50f59fa18906cf23c`.
Revisión y repetición de P1–P6/R1: 7 de noviembre de 2026, America/Bogota.
Antecedente conservado: commit de documentación `ce35714047c1e86a4823f5513b2a76867c06a188`, publicado sobre la misma base de main. La rama existente se reutiliza sin reescribir su historial; el adjunto coincide exactamente con su `AGENTS.md`.

Objetivo general: apoyar el diseño y la gestión de redes WAN por sedes, calcular direccionamiento, representar dispositivos y enlaces y generar propuestas de configuración por fabricante, con ciberdefensa integrada y evidencia académica reproducible. La aplicación genera texto; no aplica configuraciones a dispositivos.

Esta tarea incorpora exclusivamente cuatro documentos. No corrige código, modifica el esquema JSON, instala dependencias ni ejecuta configuraciones sobre redes. La guía docente define requisitos; el código define implementación; una inspección no demuestra funcionamiento.

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

`state = fresh()` centraliza proyecto, sedes, VLAN, plan, nodos, enlaces, opciones, configuraciones y revisión. `state.version` es 2. `render()` y `go()` presentan once etapas desde resumen hasta evidencias Corte 2. Los formularios editan valores visibles que se confirman mediante funciones específicas; el DOM y el estado confirmado pueden diferir.

La persistencia usa `localStorage` con clave `WAN-Architect-v2`. `exportJSON()` serializa `{ state, imageData }`; `validateImport()` exige versión 2 y valida entradas antes de `applyImport()`. Los datos permanecen en el navegador o archivos exportados. El JSON no es un mecanismo para ejecutar comandos.

| Módulo | Funciones de referencia | Confirmado por inspección |
| --- | --- | --- |
| Proyecto y estimación | `fresh`, `siteDefault`, `saveProject`, `saveSite`, `estimated`, `proposal` | Sedes, usuarios, inventario, crecimiento y redundancia |
| VLAN y VLSM | `proposeVlans`, `readVlans`, `allocate`, `confirmVlans`, `editGateway` | Segmentación por sede, asignación desde un bloque privado global, reservas y tránsitos /30 |
| Calculadora IPv4 | `ipNum`, `ipType`, `subnet`, `calculate` | CIDR, red, broadcast, máscara, hosts y clasificación de direcciones; no IPv6 |
| Topología | `buildTopology`, `editNode`, `editLink`, `validateLink`, `svgTopology` | Generación y edición de nodos/enlaces, ISP, VLAN, interfaces, imagen manual de referencia y exportación SVG |
| Fabricantes | `configNodes`, `assertReady`, `generate`, `generateCompare` | Cisco/Huawei para routers y switches compatibles con los tipos del programa; no adaptadores Fortinet/MikroTik |
| Ciberdefensa | `esc`, `hostname`, `interfaceName`, `topologyIssues`, `securityWarnings` | Escape de textos, validación, advertencias y marcadores de secretos; no auditoría integral |
| Persistencia y entregas | `saveLocal`, `loadLocal`, `importJSON`, `exportJSON`, `downloadPlan`, `downloadReport` | Guardado, importación validada, exportación JSON, CSV y resumen HTML |

## Pruebas ejecutadas en esta tarea

P1–P6 y R1 se repitieron en esta revisión con Python/Playwright ya disponibles y Chromium 154.0.8037.57, contexto de navegador nuevo y datos ficticios. Se sirvió el checkout por HTTP local temporal con `http.server`; GET de `WAN_v4.html` devolvió 200. El servidor y el navegador se cerraron al terminar. No se instalaron dependencias ni se aplicaron configuraciones de red. El antecedente `ce35714` registra bloqueo de `file://` por política del navegador (`ERR_BLOCKED_BY_ADMINISTRATOR`); esa modalidad no se repitió en esta revisión y no demuestra un fallo del HTML.

| Caso | Acción y comprobación ejecutada | Resultado y límite |
| --- | --- | --- |
| P1 | En Subnetting IPv4, introducir `192.168.10.50/26` y pulsar Calcular | Red `192.168.10.0`, broadcast `192.168.10.63`, máscara `255.255.255.192` y 62 hosts visibles |
| P2 | Tras P1, calcular `999.1.1.1/24` | `state.calc` conserva el valor válido anterior; no se verificaron todos los mensajes ni todas las entradas inválidas |
| P3 | Cargar ejemplo de laboratorio, ir a Estimación, proponer segmentación y confirmar VLAN/VLSM | Plan aprobado con 19 subredes; comprobación por pares de ausencia de solapamientos y capacidad disponible mayor o igual a hosts solicitados |
| P4 | Desde P3, generar topología desde el plan | SVG presente, 28 nodos y 34 enlaces; no valida operación de una red real |
| P5 | Desde P4, Comparación → generar las dos sintaxis | Dos bloques de texto: Cisco contiene `hostname`, Huawei contiene `sysname`; no valida toda la sintaxis ni ejecución en hardware |
| P6 | Guardar proyecto después de P5 | Existe una entrada en `localStorage`; no se probó restauración, persistencia tras reinicio ni ida y vuelta de JSON |
| R1 | En VLAN, editar sin confirmar el nombre de la primera fila y eliminar la tercera | **Defecto reproducido:** el nombre visible vuelve al confirmado anterior; no se conserva la edición pendiente |

No hubo errores de página JavaScript en el flujo HTTP ejecutado. Los resultados P1–P6/R1 de la tabla corresponden a la repetición actual, no solo al registro histórico. R1 confirma una incidencia pendiente; no equivale a que el comportamiento requerido pase. Las verificaciones se ejecutaron como comandos de sesión, sin incorporar un harness al repositorio. No se generaron capturas ni un reporte académico formal. No se calcula porcentaje de confianza con esta prueba de humo.

Reproducción manual: abrir el HTML servido localmente en un navegador limpio, ejecutar P1–P6 en el orden indicado y después R1. Para repetir las comprobaciones internas usar `state.plan`, `state.nodes`, `state.links` y `state.configs` en la consola; el código conserva estas variables en el contexto del script. Probar JSON, descargas, todos los fabricantes y límites requiere casos adicionales.

## Correcciones y brechas pendientes

| Prioridad | Estado y fuente | Trabajo siguiente y aceptación |
| --- | --- | --- |
| Alta | R1 reproducido; `deleteVlan` usa `state.vlans` y vuelve a renderizar sin leer previamente otras ediciones DOM | Corregir en tarea de código separada: conservar otras filas editadas, eliminar solo la elegida e invalidar únicamente dependencias; comprobar también cancelar y eliminar última VLAN |
| Alta | Rangos por sede/VLAN solicitados en Correcciones; código ofrece bloque global y gateway editable | Definir alcance de rangos y asignaciones manuales; comprobar capacidad, pertenencia, reservas y solapamientos antes de cambiar el modelo |
| Alta | Fortinet/MikroTik ausentes; guía exige cuatro marcas | Confirmar modelos/versiones y diseñar adaptadores coherentes con plan/topología; ver matriz de fabricantes |
| Alta | IPv6 es requisito oficial general; calculadora y plan actuales son IPv4 | Confirmar alcance para Corte 3; no ocultar la brecha ni atribuirle un peso independiente |
| Media | Interfaz mezcla español y francés; Correcciones pide tanto solo botones como traducción integral | Decidir parche localizado frente a i18n total antes de modificar; son tareas distintas |
| Media | README marca filtro Huawei pendiente; `configNodes` ya ofrece equivalencias cuando no hay nodos Huawei | Verificar específicamente selección alternativa, equipos manuales y mixtos; P5 solo prueba Comparación, no certifica ese filtro |
| Media | Código monolítico y normalización solicitada | Capturar salidas de referencia y JSON, después refactor autorizado sin alterar comportamiento |
| Alta | Entregables Corte 3 y evidencias faltantes por inventario | Completar pruebas reproducibles, informe, manual, seguridad, políticas y capturas reales; ver trazabilidad |

## Dependencias y riesgos técnicos

Flujo actual: proyecto/sedes → inventario → VLAN → plan VLSM → topología/interfaces → configuraciones → exportaciones y evidencias. Ciberdefensa y validaciones atraviesan todas las etapas; persistencia serializa el estado compartido.

`invalidate` aumenta revisión y vacía datos derivados según nivel. `confirmVlans` y `editGateway` eliminan topología y configuraciones previas para evitar salidas obsoletas. Cambiar VLAN puede afectar gateway, DHCP, OSPF, enlaces y ambos fabricantes. El defecto DOM/estado expone riesgo de pérdida de ediciones no confirmadas.

El validador de importación solo acepta fabricantes Cisco/Huawei. Añadir marcas o IPv6 necesita un diseño de compatibilidad y pruebas de migración antes de tocar el esquema v2. No se ha autorizado ese cambio aquí.

Las configuraciones son propuestas: no hay modelo/versión de equipo verificados. HSRP y VRRP no forman un grupo común; el programa advierte pares de cores de fabricantes distintos. DHCP se configura solo en el core primario y no tiene replicación de concesiones. La WAN dibujada no aporta VPN, cifrado ni servicio de ISP; las ACL de administración no equivalen a aislamiento entre servicios. Estas advertencias existen por inspección; no se probó cada rama de validación.

El guardado local depende del origen, navegador y cuota. La imagen es referencia manual, sin OCR ni reconocimiento automático. No se verificaron importación/exportación, descargas, portapapeles, accesibilidad, móviles o todos los casos de seguridad. Las capturas 01–04 y el PDF Corte 2 existen, pero no se auditó su contenido ni vigencia frente al commit base. Falta `05-github-commits.png`; la base tiene 22 commits alcanzables, lo que no demuestra calidad de mensajes ni 2FA. El conector GitHub confirmó en esta revisión `visibility: public` y rama principal `main`; 2FA no se verificó.

## Próximas etapas recomendadas

1. Revisar esta documentación y usar la trazabilidad como lista de aceptación, sin tratarla como evidencia de cumplimiento completo.
2. Crear harness versionado y casos de conservación de estado, importación/exportación v2 y salidas Cisco/Huawei de referencia.
3. Corregir R1 en rama de código separada con pruebas de caso normal, cancelación y límites.
4. Resolver rangos, i18n, alcance IPv6 y versiones de fabricantes; documentar decisiones antes de modificar el modelo.
5. Implementar Fortinet y MikroTik por separado con pruebas y revisión de sintaxis por plataforma.
6. Completar ciberdefensa, pruebas formales, documentos y capturas, y ensayar sustentación en vivo.

`AGENTS.md` se incorporó byte por byte desde el adjunto autorizado. Su texto describe una tarea local y prohíbe commit/push; esta solicitud actual autoriza expresamente el commit y push de los cuatro documentos. Se conserva esa contradicción sin reescribir el adjunto. Para futuras tareas debe leerse junto con la autorización vigente del usuario; no es una especificación completa de desarrollo permanente.
