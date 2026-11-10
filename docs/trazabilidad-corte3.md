# Trazabilidad del Corte 3

## Fuente y versión

Fuente normativa: [Guía Docente.html](<requisitos/Guía Docente.html>), rúbrica Corte 3, actividades, plantilla README y políticas IA. Base main `6ac46f9257143f88ec8cb7b47c020bb3739adbfa`; código bilingüe `71d56cb469a1f9049d24fc0bf2804adefdd256db`, rama `feature/i18n-evidencias-finales`. Revisión: 9 de noviembre de 2026, America/Bogota.

Los seis pesos oficiales suman 100%; **no son una nota asignada ni el porcentaje de pruebas**. Resultado local vigente: C01–C31, 31/31 = 100% del conjunto ejecutado, con límites en [pruebas.md](pruebas.md) y [estado-proyecto.md](estado-proyecto.md). Las matrices y cantidades históricas quedan en Git y no se suman a este conjunto.

## Matriz de evaluación vigente

| Criterio del docente | Peso oficial | Requisito funcional | Módulo | Estado actual | Prueba necesaria / ejecutada | Evidencia requerida | Documento de entrega | Observaciones y pendientes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Config Fortinet + 4.ª marca | 25% | Completar Cisco, Huawei, Fortinet y MikroTik desde plan/topología comunes | Cuatro adaptadores y Comparación | Implementado y probado como texto; sin certificación física | C12–C16/C26: redes, interfaces, DHCP/relay, rutas/OSPF y separación; CLI exactas frente a base en ES/EN | Capturas 06 y 07; apoyo 03/04 | Informe Corte 3, manual y matriz de fabricantes | FortiOS 7.4 y RouterOS 7.x genéricos; modelo/firmware y tráfico real sin validar. No se adjudica puntaje automáticamente |
| Ciberdefensa integrada | 15% | No guardar secretos, validar entradas, advertir riesgos y documentar políticas IA | Validadores, importador y Ciberdefensa | Controles y documentos presentes; `.gitignore` verificado | C08/C10/C17: rechazo atómico; revisión de secretos, exclusiones y texto de configuraciones | Captura 08 real | `politicas-ia.md`, `seguridad.md` e informe | No es auditoría exhaustiva. Marcadores técnicos intencionales; no `.env` innecesario en frontend |
| Pruebas y % de confianza | 20% | Suite reproducible y porcentaje real; ejecución durante sustentación | Python/Playwright | 31/31 ejecutadas/superadas; 0 fallidas/bloqueadas/no ejecutadas | `python tests/test_corte3.py`; 20 casos previos + 11 de idiomas/controles/regresión | Captura 09 y reporte real | `pruebas.md`, reporte HTML e informe | Denominador solo ejecutadas; repetir ante evaluación sin simular resultados |
| Documento + manual | 15% | Explicar mejoras, cuatro marcas, ciberdefensa, resultados y uso | Documentación y evidencias | Informe, manual, políticas y seguridad presentes; capturas corregidas e insertadas | PDF renderizado completo, pdfinfo/texto y revisión visual; enlaces y datos académicos autorizados | Capturas 01–10; 06–10 exigidas para Corte 3 | `informe-corte3.pdf`, `manual.md` | Estudiante e institución autorizados; no se incluyen campos académicos sin datos. Corte 2 se conserva |
| Sustentación | 15% | Demostrar en vivo la herramienta, pruebas y comprensión | Flujo completo | **No realizada** en esta tarea | Demostrar proyecto, IPv4/IPv6, topología, cuatro marcas, idioma y suite | Presentación en vivo | Informe, manual y pruebas como apoyo | Preparación y evidencia local no equivalen a sustentación realizada |
| Repositorio y versiones | 10% | Historial limpio, ramas y app final funcionando | GitHub, README y app | Repositorio público e historial de más de cinco commits; rama de trabajo y autoevaluación verificable | Revisión remota antes/después de push, alcance, archivos y ausencia de secretos/temporales | Capturas 05 y 10 | README y repositorio público | 05 es GitHub real, HTTPS 200, render sin estilos externos bloqueados; no se fabricaron mensajes. PR para revisión, sin merge automático |

## Requisitos transversales

| Requisito | Implementado y probado | Límite |
| --- | --- | --- |
| IPv4/IPv6, público/privado y plan por sede | C01/C02/C07/C09/C26: calculadoras, VLSM por pools y CIDR manual; IPv6 ULA /48–/56–/64 separado | Los cuatro generadores continúan IPv4; alcance de comandos IPv6 por aclarar |
| Estado y migraciones | V4; v2→v3→v4 sin reasignar; JSON y localStorage v4 con fallback v3/v2 | Almacenamiento local sin cifrar; no se convierten proyectos v4 hacia apps antiguas |
| Dispositivos, enlaces e interfaces | C11/C28: generar, editar, validar, eliminar y exportar | Imagen solo de referencia, sin OCR; no conectividad real |
| Español/English sin alterar datos | C21–C26/C30/C31: catálogo, mensajes, atributos, persistencia independiente y CLI intactas | Nombres de usuario/CLI/JSON no se traducen; no equivale a cobertura lingüística de datos introducidos |
| Botones y accesibilidad de teclado | 58 plantillas con acciones, dos importadores y selector; 54 familias/objetivos con Enter, fallback y archivo con Enter/Espacio | 0 botones decorativos detectados/eliminados; no certifica accesibilidad completa |
| Entrega Corte 2 y nombres exactos | Informe Corte 2 conservado; capturas 01–05 presentes y verificadas, incluidos commits reales | No se reescribió el informe histórico ni se declara una calificación del corte anterior |
| Secretos | `.env`/`.env.*` excluidos; `.env.example` permitido; sin secretos detectados | Frontend sin secretos; no se creó `.env` ni un backend |

## Inventario de entregables

README sigue el orden de la plantilla, contiene identidad autorizada, funciones, ejecución, pruebas, documentos, diez evidencias y autoevaluación Sí/No. Solo se marca Sí con evidencia local concreta; la sustentación permanece No.

| Rutas exactas | Estado / evidencia |
| --- | --- |
| `docs/informe-corte2.pdf` | Conservado sin cambios |
| `docs/informe-corte3.pdf` | Actualizado, renderizado completo y texto extraíble; páginas y revisión en pruebas |
| `docs/manual.md` | Flujo, idiomas, controles, escenarios y manifiesto de 58 plantillas |
| `docs/seguridad.md` y `docs/politicas-ia.md` | Controles, siete políticas y límites comprobables |
| `docs/pruebas.md` y `tests/reporte-corte3.html` | Esperado/obtenido/estado C01–C31, entorno, hashes y porcentaje |
| `01-subnetting.png` | IP, prefijo, red, broadcast y hosts visibles |
| `02-topologia.png` | Diagrama completo con dispositivos y enlaces |
| `03-config-cisco.png` y `04-config-huawei.png` | Hostname/sysname, VLAN e IP visibles |
| `05-github-commits.png` | Cinco o más mensajes reales de GitHub |
| `06-config-fortinet.png` y `07-config-mikrotik.png` | Propuestas reales de adaptadores separados |
| `08-ciberdefensa.png` | Rechazo real conservando cálculo previo |
| `09-pruebas.png` | Nueva ejecución 31/31 = 100% |
| `10-app-final.png` | Aplicación y selector de idioma visibles |

Las rutas PNG están bajo `docs/capturas/`; enlaces y escenarios en el [manual](manual.md). Las capturas pequeñas/de perímetro/integradas son laboratorios alternativos, no un diseño con gateways duplicados. Los antecedentes siguen disponibles en el [historial de trazabilidad de la base](https://github.com/Daisy-redeswan/redes-wan-Rodriguez/blob/6ac46f9257143f88ec8cb7b47c020bb3739adbfa/docs/trazabilidad-corte3.md).
