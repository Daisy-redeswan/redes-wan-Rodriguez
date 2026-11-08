# Seguridad aplicada y límites — Corte 3

Base inspeccionada: main `f7ed2b907d6edad6f1ed7bd5274c49956a7a77d8`. Esta entrega documenta controles existentes y evidencia local; no modifica `WAN_v4.html`, no añade mecanismos de seguridad al código y **no declara una auditoría completa**.

## Modelo de uso y datos

La app es un HTML autónomo que procesa proyecto, sedes, direcciones y textos de configuración en el navegador. No solicita cuentas ni claves, no conecta con routers y no envía datos a una IA. Los enlaces técnicos son consultas opcionales externas; no son APIs de generación. Las pruebas bloquean solicitudes fuera del origen local y usan datos ficticios.

Se recomienda abrir por HTTP local con `--bind 127.0.0.1`, trabajar en un navegador confiable y exportar respaldos JSON. LocalStorage y JSON **no están cifrados**: cualquier persona con acceso al perfil/archivo puede leerlos. No introducir topologías confidenciales, credenciales, IP sensibles ni información personal. No publicar el servidor de desarrollo ni el directorio del proyecto en una red ajena.

## Validación y manejo de contenido

Confirmado por inspección: `hostname`, validadores de interfaces, `enumVal`, `idVal`, `text` y los parsers de IP/CIDR restringen datos que alimentan configuración o referencias. `esc()` convierte contenido a texto seguro antes de insertarlo en las vistas pertinentes. Fabricantes y roles se validan mediante listas permitidas; no se trata un fabricante desconocido como Cisco/Huawei.

`validateImport()` reconstruye el contrato conocido, verifica tipos, límites y relaciones y solo después permite `applyImport()`. Hay límites de tamaño de archivo JSON, listas y datos de imagen; no se usa `eval` para ejecutar el contenido importado. Las CLI importadas se comparan con la salida regenerada antes de conservarse. Estas comprobaciones no equivalen a un fuzzer exhaustivo ni a la ausencia de vulnerabilidades.

Los cálculos comprueban alineación, contención, capacidad, solapamientos y gateways. Confirmaciones e importaciones inválidas conservan el último estado y texto visible según los flujos probados. El parser IPv6 usa 128 bits en memoria y persiste cadenas; el plan ULA está separado del plan IPv4 y no abre servicios ni activa protocolos.

## Acceso y propuestas de red

| Plataforma | Controles propuestos por el generador | Límite |
| --- | --- | --- |
| Cisco/Huawei | SSH/STelnet y restricción administrativa desde Gestión según opciones; marcadores de credenciales; privilegio inicial limitado en la propuesta Cisco | Confirmar modelo/versión, autorización del usuario, claves, prompts y soporte real; ACL administrativa no es segmentación entre servicios |
| Fortinet | HTTPS/SSH limitados a Gestión mediante local-in; interfaces, objetos y rutas del plan; sin permisos de tránsito o NAT inventados | FortiOS 7.4 genérico sin multi-VDOM; cuentas/certificados, objetos/IDs y configuración existente requieren revisión; sin HA/LACP |
| MikroTik | SSH fuerte restringido a Gestión; Telnet/FTP/WWW/APIs/Winbox y MAC deshabilitados; input controlado y drop inicial en forward | RouterOS 7.x genérico; definir intención explícita de tráfico antes de permitir tránsito; sin VRF/CAPsMAN/LACP/VRRP |

Una ruta por defecto requiere siguiente salto y justificación; no implica Internet, NAT ni permiso de tránsito. La WAN dibujada no proporciona VPN/cifrado. HSRP y VRRP no forman un grupo común entre fabricantes. El DHCP del core primario no replica concesiones por sí mismo. Las cuatro salidas son **IPv4**, no comandos IPv6.

## Secretos y marcadores

`<CAMBIAR_EN_PRODUCCION>` es un marcador, **no una contraseña válida**. Debe sustituirse por un procedimiento externo seguro, después de revisar la propuesta y únicamente en un laboratorio autorizado. No introducir secretos reales en el código, JSON, capturas, conversaciones de IA, historial Git ni documentos.

La guía establece `.env` protegido por `.gitignore` para secretos. En esta app estática no se necesitan ni se crean secretos o `.env`; un `.env` servido por HTTP o incluido en un frontend no es un almacén seguro. El repositorio base no contiene una política `.gitignore` que pueda declararse implementada aquí. Si se añade un backend/integración futura, gestionar secretos fuera del contenido público, añadir exclusiones antes de trabajar con ellos y obtener autorización para ese cambio de alcance. No se creó `.env` ni se modificó `.gitignore` en esta entrega documental.

## Evidencia ejecutada

- **C08/C10:** errores IPv4/IPv6 conservan estado, derivados, almacenamiento y formulario en los escenarios probados.
- **C17:** cuatro payloads inseguros/futuros de hostname, interfaz, CIDR y versión se rechazan sin sustituir el estado.
- **C18 y revisión por caso:** compilación JavaScript en Chromium; sin errores de página/consola ni solicitudes externas en el conjunto ejecutado.
- **C14/C15/C16:** estructura y separación de gramáticas FortiOS/RouterOS, controles propuestos y aislamiento de cuatro fabricantes, como texto.
- **[Captura 08](capturas/08-ciberdefensa.png):** el formulario contiene `192.168.10.999/26`, muestra «IPv4 inválida» y conserva el resultado de `192.168.10.50/26` (red .0, broadcast .63, 62 hosts).
- **[Captura 09](capturas/09-pruebas.png):** 20/20 del conjunto identificado en [pruebas.md](pruebas.md), ratificado en el main actual. El 100% no mide toda la seguridad ni la cobertura de cada rama del código.

La revisión documental y de publicación comprueba secretos conocidos, nombres/rutas, hashes, diff y temporales. No es un escáner de vulnerabilidades certificado ni asegura que un usuario nunca introduzca un dato sensible.

## Riesgos y operación responsable

Revisar siempre la configuración existente, interfaces reales, retornos, adyacencias, certificados, credenciales, redundancia y permisos. Las propuestas no son respaldos completos ni aplicaciones idempotentes. No copiar comandos a un equipo por el solo hecho de que una prueba de texto pase.

No se probaron hardware, firmware, convergencia, comportamiento de firewall en tráfico real, resistencia a ataques, todos los navegadores ni todas las combinaciones. Persisten pendientes históricos como `saveSite()` y desbordamientos de interfaz fuera de los casos verificados. La sustentación debe explicar estas limitaciones y las [políticas IA](politicas-ia.md), sin presentar cumplimiento total o certificación física.
