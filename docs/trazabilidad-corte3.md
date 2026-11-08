# Trazabilidad del Corte 3

## Fuente y alcance

Fuente principal: [Guía Docente.html](<requisitos/Guía Docente.html>), secciones «Rúbrica de evaluación», «Actividades y entrega», «La herramienta» y «Uso de la IA y pruebas». Código Fortinet auditado: `5d87d76d3e78ded591220f75e2960f736fcf28ce`, base main `c33859758c717b1f777174183409dcdf5376aaab`; la auditoría anterior del PR #3 se conserva como antecedente, archivo [WAN_v4.html](../WAN_v4.html).

La guía define seis criterios cuyos pesos suman 100%. Los pesos siguientes son oficiales; no son una calificación otorgada ni porcentaje de confianza. Los estados y pruebas ejecutadas se detallan en [estado-proyecto.md](estado-proyecto.md); los límites de plataformas en [matriz-fabricantes.md](matriz-fabricantes.md).

## Matriz de evaluación

| Criterio del docente | Peso oficial | Requisito funcional | Módulo | Estado actual | Prueba necesaria | Evidencia requerida | Documento de entrega | Observaciones y pendientes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Config Fortinet + 4.ª marca | 25% | Completar Cisco, Huawei, Fortinet y MikroTik desde el mismo plan/topología | Generadores y Comparación | Fortinet implementado y probado estáticamente (F1–F18); Cisco/Huawei sin regresión. MikroTik pendiente; ninguna marca certificada físicamente | Comprobar VLAN, IP, rutas, acceso y sintaxis de cada marca con casos reproducibles; revisar en plataforma/versiones confirmadas | `docs/capturas/06-config-fortinet.png` y `docs/capturas/07-config-mikrotik.png` | `docs/informe-corte3.pdf`; instrucciones en `docs/manual.md` | Existe adaptador Fortinet separado bajo supuesto FortiGate genérico/FortiOS 7.4/sin VDOM adicionales; capturas 06/07 y compatibilidad física pendientes. MikroTik no implementado; criterio de cuatro marcas aún incompleto |
| Ciberdefensa integrada | 15% | No guardar secretos, validar entradas, advertir configuraciones inseguras y aplicar políticas anti-IA | Validadores, importación y Ciberdefensa | Controles inspeccionados; P2 conserva cálculo previo ante IPv4 inválida. Cumplimiento integral pendiente | Rechazo de entradas inválidas e inyección, JSON alterado, advertencias, revisión de secretos y mínimo privilegio | `docs/capturas/08-ciberdefensa.png`: rechazo o advertencia real | `docs/politicas-ia.md`, `docs/seguridad.md` e informe final | No existen esos documentos en la base ni `.gitignore`; documentar la política oficial y cómo se aplica a esta app sin backend; no introducir secretos o un `.env` innecesario |
| Pruebas y % de confianza | 20% | Ejecutar pruebas y reportar proporción superada; repetir en sustentación | Pruebas transversales | Fortinet F1–F18 más I1–I9: 27/27 superadas; revisión crítica previa a publicación: 14/14 repetidas, sin duplicar el porcentaje. Sin harness versionado ni reporte académico formal | Suite con datos, resultado esperado/real y contadores; casos normales, inválidos, límites y regresión; separar no ejecutados/bloqueados | `docs/capturas/09-pruebas.png` con pruebas corriendo y X de Y visible | `docs/pruebas.md` y resultados en informe final | No calcular porcentaje de confianza a partir de código existente o casos solo diseñados; distinguir reproducción histórica R1 de la conservación actual comprobada en I7 |
| Documento + manual | 15% | Explicar mejoras, cuatro marcas, seguridad, resultados y uso paso a paso | Documentación y flujo completo | Hay PDF Corte 2; faltan informe y manual finales | Seguir manual en navegador limpio y cotejar informe con funciones y evidencia reales | Capturas pertinentes 06–10 insertadas en el informe | `docs/informe-corte3.pdf` y `docs/manual.md` | Los documentos de orientación organizan el trabajo; no sustituyen informe, manual o políticas |
| Sustentación | 15% | Demostrar en vivo la herramienta, correr pruebas y explicar construcción y funcionamiento | Aplicación completa y pruebas | Pendiente; no se ha realizado una sustentación en esta tarea | Ensayo y ejecución en vivo de flujo completo, cuatro marcas y pruebas reproducibles | Demostración en vivo; no es un archivo exigido por este criterio | Apoyo: informe, manual y `docs/pruebas.md` | Fecha no fijada en la guía. Un ensayo futuro no debe registrarse como sustentación ya realizada |
| Repositorio y versiones | 10% | Historial limpio, uso de ramas y app final funcionando | Git/GitHub, README y aplicación | IPv4 v3 integrado en main; rama Fortinet con commits de código y orientación, pruebas locales y PR para revisión; sin certificar app Corte 3 final | Revisar historial, rama, ausencia de secretos, acceso público y flujo final; confirmar ref remota después del push | `docs/capturas/10-app-final.png` con pantalla principal final | Repositorio público, `README.md` e informe final | No hay captura 10; 2FA no verificada. No afirmar app Corte 3 final por haber publicado documentación |

## Requisitos oficiales transversales

Estos requisitos no tienen un peso independiente en la rúbrica Corte 3; no se redistribuyen los seis pesos anteriores.

| Requisito de la guía | Relación con módulos/criterios | Situación y aceptación pendiente |
| --- | --- | --- |
| Subnetting IPv4/IPv6, público/privado y plan por sede o piso | Base de las configuraciones y del flujo completo | IPv4 v3 implementado: global, sede/tránsito opcionales y CIDR manual por VLAN; automático/mixto probado en I1/I3/I4. Gateway independiente; DHCP automático vigente. IPv6, pools DHCP y reservas editables pendientes; no declarar cumplimiento IPv6 |
| Ingresar/importar dispositivos, roles, enlaces WAN e ISP | Topología y generación multimarca | Generación comprobada en I8; migración/ida y vuelta JSON v2→v3 probadas en I2/I6. Edición manual de todos los tipos de nodos/enlaces sin cobertura integral. Imagen es referencia manual, no reconocimiento automático |
| Repositorio público, mínimo cinco commits, al menos una rama y datos de laboratorio | Repositorio y versiones | Historial local suficiente en cantidad, sin auditoría de calidad; verificar publicación, acceso público y protección de datos. 2FA es requisito de cuenta que esta tarea no verifica |
| Conservar entrega Corte 2 y nombres exactos | Continuidad de entrega | Existen informe Corte 2 y capturas 01–04; falta `docs/capturas/05-github-commits.png`; contenido de evidencias históricas sin auditar |
| Política de secretos y revisión de lo generado por IA | Ciberdefensa | Guía exige `.gitignore` con `.env`; ausente en base. Revisar en una tarea autorizada: no crear archivos fuera de los tres documentos permitidos en esta revisión |

## Inventario de entregables del Corte 3

Inventario de rutas previo a este cambio, sin validar resultados por existencia:

| Ruta exacta oficial | Estado en la base | Trabajo requerido |
| --- | --- | --- |
| `docs/informe-corte3.pdf` | Ausente | Informe final con mejoras, cuatro marcas, seguridad, pruebas y capturas |
| `docs/manual.md` | Ausente | Ejecución y uso verificados paso a paso |
| `docs/seguridad.md` | Ausente | Medidas realmente aplicadas y límites |
| `docs/politicas-ia.md` | Ausente | Política de la guía y aplicación comprobable |
| `docs/pruebas.md` | Ausente | Casos reales, resultados, X/Y y porcentaje trazable |
| `docs/capturas/06-config-fortinet.png` | Pendiente | Captura oficial de generación del adaptador Fortinet; las capturas temporales de pruebas no sustituyen esta entrega |
| `docs/capturas/07-config-mikrotik.png` | Ausente | Generación MikroTik real |
| `docs/capturas/08-ciberdefensa.png` | Ausente | Entrada rechazada o advertencia insegura |
| `docs/capturas/09-pruebas.png` | Ausente | Ejecución y resultado visible de pruebas |
| `docs/capturas/10-app-final.png` | Ausente | Pantalla principal de versión final funcionando |

## Registro de resultados y mantenimiento

Para cada prueba futura registrar identificador, commit, datos ficticios, entorno, pasos, expectativa, resultado real y evidencia. Distinguir aprobada, fallida, bloqueada y no ejecutada. El porcentaje debe usar un conjunto definido y resultados ejecutados; informar aparte la cobertura pendiente. Los ejemplos numéricos de la guía son plantillas y no resultados de WAN Architect.

Las seis comprobaciones P1–P6 y la reproducción R1 se repitieron el 7 de noviembre de 2026 (America/Bogota) y están documentadas en estado-proyecto con sus límites. No hay captura 09 de esta ejecución ni informe formal: esta matriz no adjudica puntajes ni certifica Corte 3.

Actualización del 8 de noviembre de 2026 (America/Bogota): I1–I9 se ejecutaron en clon limpio y contextos nuevos, con Python/Playwright, Chromium 154.0.8037.57 y HTTP local. Datos, esperado/obtenido y límites se registran en [estado-proyecto.md](estado-proyecto.md). No hubo errores de consola/página ni desbordamiento de página a 1440/390 px. Evidencias temporales de sesión, sin nueva captura 09 oficial ni informe formal. Las matrices históricas M/S/A/C/V se conservaron como antecedentes, sin repetirlas completas ni sumarlas al 9/9.

La persistencia usa `WAN-Architect-v3`, con prioridad sobre v2; el fallback migra sin reasignar ni sobrescribir v2. El JSON exporta v3 y conserva intención y plan efectivo; las importaciones se validan antes de sustituir estado. Estas pruebas aportan evidencia técnica y no cambian los pesos de la rúbrica ni certifican compatibilidad física. Siguen pendientes `saveSite()` (invalidación histórica), desbordamiento a 320 px, compatibilidad física/captura 06 de Fortinet, MikroTik, IPv6, pools DHCP/reservas editables y entregables académicos del inventario.

Actualización Fortinet (8 de noviembre de 2026): adaptador separado con hostname, interfaces/VLAN/IPv4, administración restringida, DHCP o relay, rutas/OSPF y objetos del plan; tránsito marcado para revisión sin permisos ni NAT implícitos. Supuesto FortiGate genérico, FortiOS 7.4, sin multi-VDOM (contexto interno root solo para VLAN). Las 27/27 pruebas registradas y las 14/14 críticas repetidas son locales y de texto, no una certificación física ni una nota del criterio 25%. Se conservan los pesos oficiales; MikroTik, IPv6 y captura 06 siguen pendientes. Detalle y límites en [estado-proyecto.md](estado-proyecto.md) y [matriz-fabricantes.md](matriz-fabricantes.md).

Actualizar la matriz después de cambios y pruebas autorizados, contrastando la guía vigente. Como apoyo técnico consultar [Arquitectura_Agente_WAN_Architect.docx](requisitos/Arquitectura_Agente_WAN_Architect.docx) y [Correcciones Pendientes.txt](<requisitos/Correcciones Pendientes.txt>); no reemplazan los criterios del docente.
