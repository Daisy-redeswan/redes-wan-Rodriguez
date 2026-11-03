# Trazabilidad del Corte 3

## Fuente y alcance

Fuente principal: [Guía Docente.html](<requisitos/Guía Docente.html>), secciones «Rúbrica de evaluación», «Actividades y entrega», «La herramienta» y «Uso de la IA y pruebas». Base inspeccionada: `6f45dc1e54051a2467241ee50f59fa18906cf23c`, archivo [WAN_v4.html](../WAN_v4.html).

La guía define seis criterios cuyos pesos suman 100%. Los pesos siguientes son oficiales; no son una calificación otorgada ni porcentaje de confianza. Los estados y pruebas ejecutadas se detallan en [estado-proyecto.md](estado-proyecto.md); los límites de plataformas en [matriz-fabricantes.md](matriz-fabricantes.md).

## Matriz de evaluación

| Criterio del docente | Peso oficial | Requisito funcional | Módulo | Estado actual | Prueba necesaria | Evidencia requerida | Documento de entrega | Observaciones y pendientes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Config Fortinet + 4.ª marca | 25% | Completar Cisco, Huawei, Fortinet y MikroTik desde el mismo plan/topología | Generadores y Comparación | Cisco/Huawei inspeccionados; P5 generó dos textos. Fortinet/MikroTik pendientes | Comprobar VLAN, IP, rutas, acceso y sintaxis de cada marca con casos reproducibles; revisar en plataforma/versiones confirmadas | `docs/capturas/06-config-fortinet.png` y `docs/capturas/07-config-mikrotik.png` | `docs/informe-corte3.pdf`; instrucciones en `docs/manual.md` | No existen adaptadores nuevos ni capturas 06/07; compatibilidad en equipos bloqueada por falta de modelos/versiones confirmados |
| Ciberdefensa integrada | 15% | No guardar secretos, validar entradas, advertir configuraciones inseguras y aplicar políticas anti-IA | Validadores, importación y Ciberdefensa | Controles inspeccionados; P2 conserva cálculo previo ante IPv4 inválida. Cumplimiento integral pendiente | Rechazo de entradas inválidas e inyección, JSON alterado, advertencias, revisión de secretos y mínimo privilegio | `docs/capturas/08-ciberdefensa.png`: rechazo o advertencia real | `docs/politicas-ia.md`, `docs/seguridad.md` e informe final | No existen esos documentos en la base ni `.gitignore`; documentar la política oficial y cómo se aplica a esta app sin backend; no introducir secretos o un `.env` innecesario |
| Pruebas y % de confianza | 20% | Ejecutar pruebas y reportar proporción superada; repetir en sustentación | Pruebas transversales | P1–P6 ejecutadas como prueba de humo; R1 reproduce defecto. Sin harness versionado ni reporte formal | Suite con datos, resultado esperado/real y contadores; casos normales, inválidos, límites y regresión; separar no ejecutados/bloqueados | `docs/capturas/09-pruebas.png` con pruebas corriendo y X de Y visible | `docs/pruebas.md` y resultados en informe final | No calcular porcentaje de confianza a partir de código existente o casos solo diseñados; no presentar R1 como comportamiento correcto |
| Documento + manual | 15% | Explicar mejoras, cuatro marcas, seguridad, resultados y uso paso a paso | Documentación y flujo completo | Hay PDF Corte 2; faltan informe y manual finales | Seguir manual en navegador limpio y cotejar informe con funciones y evidencia reales | Capturas pertinentes 06–10 insertadas en el informe | `docs/informe-corte3.pdf` y `docs/manual.md` | Estos cuatro archivos de esta tarea organizan trabajo futuro; no sustituyen informe, manual o políticas |
| Sustentación | 15% | Demostrar en vivo la herramienta, correr pruebas y explicar construcción y funcionamiento | Aplicación completa y pruebas | Pendiente; no se ha realizado una sustentación en esta tarea | Ensayo y ejecución en vivo de flujo completo, cuatro marcas y pruebas reproducibles | Demostración en vivo; no es un archivo exigido por este criterio | Apoyo: informe, manual y `docs/pruebas.md` | Fecha no fijada en la guía. Un ensayo futuro no debe registrarse como sustentación ya realizada |
| Repositorio y versiones | 10% | Historial limpio, uso de ramas y app final funcionando | Git/GitHub, README y aplicación | Base con 22 commits alcanzables; rama de documentación creada desde main; aplicación parcial probada | Revisar historial, rama, ausencia de secretos, acceso público y flujo final; confirmar ref remota después del push | `docs/capturas/10-app-final.png` con pantalla principal final | Repositorio público, `README.md` e informe final | No hay captura 10; visibilidad pública y 2FA no verificadas. No afirmar app Corte 3 final por haber publicado documentación |

## Requisitos oficiales transversales

Estos requisitos no tienen un peso independiente en la rúbrica Corte 3; no se redistribuyen los seis pesos anteriores.

| Requisito de la guía | Relación con módulos/criterios | Situación y aceptación pendiente |
| --- | --- | --- |
| Subnetting IPv4/IPv6, público/privado y plan por sede o piso | Base de las configuraciones y del flujo completo | IPv4 probado en P1/P3; clasificación por inspección. IPv6 pendiente; definir alcance académico con docente sin declarar cumplimiento |
| Ingresar/importar dispositivos, roles, enlaces WAN e ISP | Topología y generación multimarca | Generación probada en P4; importación JSON y edición manual existen por inspección, sin prueba ejecutada aquí. Imagen es referencia manual, no reconocimiento automático |
| Repositorio público, mínimo cinco commits, al menos una rama y datos de laboratorio | Repositorio y versiones | Historial local suficiente en cantidad, sin auditoría de calidad; verificar publicación, acceso público y protección de datos. 2FA es requisito de cuenta que esta tarea no verifica |
| Conservar entrega Corte 2 y nombres exactos | Continuidad de entrega | Existen informe Corte 2 y capturas 01–04; falta `docs/capturas/05-github-commits.png`; contenido de evidencias históricas sin auditar |
| Política de secretos y revisión de lo generado por IA | Ciberdefensa | Guía exige `.gitignore` con `.env`; ausente en base. Revisar en una tarea autorizada: no crear archivos fuera de los cuatro permitidos en esta tarea |

## Inventario de entregables del Corte 3

Inventario de rutas previo a este cambio, sin validar resultados por existencia:

| Ruta exacta oficial | Estado en la base | Trabajo requerido |
| --- | --- | --- |
| `docs/informe-corte3.pdf` | Ausente | Informe final con mejoras, cuatro marcas, seguridad, pruebas y capturas |
| `docs/manual.md` | Ausente | Ejecución y uso verificados paso a paso |
| `docs/seguridad.md` | Ausente | Medidas realmente aplicadas y límites |
| `docs/politicas-ia.md` | Ausente | Política de la guía y aplicación comprobable |
| `docs/pruebas.md` | Ausente | Casos reales, resultados, X/Y y porcentaje trazable |
| `docs/capturas/06-config-fortinet.png` | Ausente | Generación Fortinet real |
| `docs/capturas/07-config-mikrotik.png` | Ausente | Generación MikroTik real |
| `docs/capturas/08-ciberdefensa.png` | Ausente | Entrada rechazada o advertencia insegura |
| `docs/capturas/09-pruebas.png` | Ausente | Ejecución y resultado visible de pruebas |
| `docs/capturas/10-app-final.png` | Ausente | Pantalla principal de versión final funcionando |

## Registro de resultados y mantenimiento

Para cada prueba futura registrar identificador, commit, datos ficticios, entorno, pasos, expectativa, resultado real y evidencia. Distinguir aprobada, fallida, bloqueada y no ejecutada. El porcentaje debe usar un conjunto definido y resultados ejecutados; informar aparte la cobertura pendiente. Los ejemplos numéricos de la guía son plantillas y no resultados de WAN Architect.

Las seis comprobaciones P1–P6 y la reproducción R1 están documentadas en estado-proyecto con sus límites. No hay captura 09 de esta ejecución ni informe formal: esta matriz no adjudica puntajes ni certifica Corte 3.

Actualizar la matriz después de cambios y pruebas autorizados, contrastando la guía vigente. Como apoyo técnico consultar [Arquitectura_Agente_WAN_Architect.docx](requisitos/Arquitectura_Agente_WAN_Architect.docx) y [Correcciones Pendientes.txt](<requisitos/Correcciones Pendientes.txt>); no reemplazan los criterios del docente.
