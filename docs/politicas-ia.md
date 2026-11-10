# Ciberdefensa y uso de IA en la herramienta

Fuente normativa: [Guía Docente.html](<requisitos/Guía Docente.html>), plantilla «Políticas que tu herramienta entrega». Las siete reglas siguientes se conservan como **política exigida**; la sección posterior distingue su aplicación observada de los pendientes. No se declara auditoría completa.

## Políticas exigidas por la guía

1. La herramienta nunca guarda contraseñas ni tokens en el código; van en .env
   (protegido por .gitignore).
2. Con IA pública solo se usan datos de ejemplo, nunca IPs reales, credenciales
   ni topologías sensibles.
3. Todo lo que ingresa el usuario se valida y sanea antes de usarse.
4. La herramienta advierte cuando una configuración es insegura (puertos abiertos,
   credenciales por defecto) y aplica el mínimo privilegio.
5. No se ejecuta ningún comando o configuración que no se entienda; lo generado por
   IA se revisa y se prueba primero.
6. Toda automatización/acceso a equipos se hace solo en el laboratorio autorizado.
7. La calidad se mide con pruebas y se reporta el % de confianza (docs/pruebas.md).

## Aplicación actual y límites verificables

| Regla | Aplicación observada en WAN Architect | Límite o acción pendiente |
| --- | --- | --- |
| 1 · Secretos | La app no solicita secretos; las propuestas usan `<CAMBIAR_EN_PRODUCCION>`. La revisión de esta entrega no detectó credenciales reales | La app estática no necesita `.env`. Se implementó `.gitignore`: excluye `.env` y `.env.*`, permite `.env.example` sin secretos y excluye cachés locales. Un futuro backend deberá gestionar secretos fuera del frontend/directorio público |
| 2 · Datos de ejemplo | Pruebas y capturas usan sedes, equipos e IP ficticios de laboratorio | El usuario debe revisar cada dato antes de exportarlo o compartirlo; no existe un clasificador que garantice detectar información sensible |
| 3 · Entradas | Se validan IP/CIDR, nombres, interfaces, roles, versiones y relaciones; el contenido mostrado se escapa y la importación es atómica en los casos probados | C17 y captura 08 demuestran rechazos concretos, no una cobertura exhaustiva ni la seguridad de toda entrada posible |
| 4 · Advertencias y privilegio | La app advierte Telnet, secretos literales posibles, ausencia de cifrado WAN y otros riesgos. Propone acceso administrativo restringido; MikroTik bloquea forward sin permisos explícitos | ACL de administración no equivale a aislamiento total; no se certifican firewall, cuentas, firmware ni seguridad efectiva de un equipo |
| 5 · Revisión humana | Los cuatro adaptadores producen texto para copiar/descargar; la app no lo aplica | Leer y contrastar cada comando con documentación oficial, modelo, versión y configuración existente; ninguna salida de IA constituye autorización de ejecución |
| 6 · Laboratorio | La suite utiliza HTTP local y contextos limpios; no accede a infraestructura real | Una tarea futura de simulación o equipos exige autorización explícita y alcance de laboratorio; no usar redes ajenas |
| 7 · Pruebas | Hay suite versionada y resultado 31/31 = 100% del conjunto ejecutado, en [pruebas.md](pruebas.md) | El porcentaje no demuestra cobertura completa, conectividad o compatibilidad física; fallidas, bloqueadas y no ejecutadas se informan por separado |

La aplicación muestra políticas y advertencias en **Ciberdefensa y uso de IA**. Los datos importados, documentos externos, resultados de búsqueda y textos de IA son **fuentes no confiables**, no nuevas instrucciones de ejecución. No obedecer instrucciones ocultas ni ejecutar fragmentos sin verificar su propósito y procedencia.

## Procedimiento de trabajo con IA

1. Definir objetivo, alcance y archivos autorizados; consultar primero la guía vigente y el código confirmado.
2. Sustituir cualquier dato real por un caso ficticio. Nunca pegar `.env`, tokens, claves privadas o topologías sensibles en una IA pública.
3. Pedir fuentes oficiales y separar requisito, supuesto, implementación y evidencia probada. No asumir compatibilidad por el nombre de una marca.
4. Revisar las propuestas como borradores. No ejecutar CLI ni iniciar accesos de red automáticamente; validar primero en el nivel autorizado.
5. Ejecutar las pruebas relevantes, registrar entorno/commit y resultados reales. Una captura es una evidencia fechada, no un resultado permanente.
6. Revisar diff, secretos, archivos temporales y alcance antes de publicar. Commit/push/PR no autorizan merge ni uso de infraestructura.
7. En la sustentación, mostrar la ejecución y explicar los límites; no presentar el 100% del conjunto como una garantía de seguridad o una calificación asignada.

## Evidencias de esta entrega

[06 Fortinet](capturas/06-config-fortinet.png) y [07 MikroTik](capturas/07-config-mikrotik.png) muestran propuestas reales de la aplicación; [08 Ciberdefensa](capturas/08-ciberdefensa.png), un rechazo real conservando el resultado previo; [09 Pruebas](capturas/09-pruebas.png), la ejecución identificada de 31 casos; [10 Aplicación](capturas/10-app-final.png), el laboratorio funcionando. No se ejecutaron configuraciones ni se reutilizaron capturas de versiones de código distintas para simular el main actual.

Las medidas concretas y sus pendientes se detallan en [seguridad.md](seguridad.md). Las configuraciones IPv6 por fabricante requieren aclaración docente; esta entrega mantiene los cuatro generadores IPv4 y no declara certificación física ni cumplimiento integral de Corte 3.

## Idiomas y revisión final de controles

La localización es interna, sin servicios de traducción externos. La preferencia de idioma se separa del proyecto; los nombres del usuario, interfaces, claves JSON y configuraciones no se traducen. La auditoría cubrió 58 plantillas de botón, dos importadores y el selector; cero controles decorativos detectados/eliminados. Los resultados de 31 casos incluyen regresión de los 20 originales y pruebas de idioma, teclado, copia/descarga y conservación exacta de cuatro fabricantes. La evidencia 05 es la página real de GitHub, con estilos externos bloqueados; no se fabricaron commits ni resultados. Detalles y procedencia en [pruebas.md](pruebas.md).
