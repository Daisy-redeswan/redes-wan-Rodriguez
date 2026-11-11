# Pruebas de confirmaciones y consola SSH — PR #10

## Resultado actual y procedencia

Base revisada: `194a43eaa3e894351e6f5a720baa4d69bbb8907e`, rama `fix/revision-integral-wan-architect`, main conservado en `1956d1872363c88399f5e8240abb1d7a13bca340`. Estas ejecuciones preceden a los commits de las nuevas fases; identifican exactamente el árbol probado por hashes, no atribuyen código nuevo al blob del commit base.

- UI/regresión: **58/58 = 100%**, 0 fallidas/bloqueadas/no ejecutadas en su matriz; 63.6 s de casos, Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57; 2026-11-11T11:35:07-05:00 (America/Bogota).
- SSH real local: **26/26 = 100%**, 0 fallidas/bloqueadas/no ejecutadas en su matriz; aproximadamente 11 s; Python 3.12.14, AsyncSSH 2.24.1, aiohttp 3.14.5; 2026-11-11T11:35:19.997021-05:00.
- Agregado de ambas matrices: **84 superadas / 84 ejecutadas × 100 = 100%**. No es cobertura absoluta ni certificación.
- Comprobación exploratoria adicional **bloqueada**: navegación directa `file://` devuelve `ERR_BLOCKED_BY_ADMINISTRATOR` en Chromium administrado. No se deshabilitó esa política ni se contó como superada. El HTML en contexto inline aislado sí ejecutó simulación/aviso de indisponibilidad con cero peticiones HTTP/WS; además se probó HTTP estático sin servicio SSH.
- No ejecutadas fuera de esas matrices: ejecución en Windows y conexiones físicas a fabricantes. Se documentan instrucciones Windows y límites; no se infieren resultados.

[Reporte UI real](../tests/reporte-ssh-ui.html) y [reporte SSH real](../tests/reporte-ssh-servicio.json). Los 50 casos anteriores permanecen registrados, incluidos ocho hashes CLI ES/EN; fixtures y hashes de referencia no cambiaron. Las expectativas de navegación incorporan el módulo 14, y N14 reconoce el nuevo booleano de confirmación sin omitir datos del plan. No se borraron casos para mejorar el porcentaje.

## Reproducción

Desde la raíz, la suite tradicional sigue sin dependencia SSH:

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
```

Para SSH opcional, en el entorno virtual del servicio instalar ambos requirements y Chromium; ejecutar `python tests/test_ssh_service.py`. En Windows usar `.\.venv-ssh\Scripts\python.exe` como explica el [README](../ssh_service/README.md). El runner SSH imprime caso/resultado, X/Y y porcentaje y devuelve no cero ante fallo. Crea HTTP, WS y servidor SSH reales en puertos loopback libres, con claves/contraseñas efímeras en RAM, sin procesos del sistema ni equipos externos.

Para guardar reportes expresamente:

```bash
python tests/test_corte3.py --report tests/reporte-ssh-ui.html
```

La variable opcional `WAN_SSH_REPORT` indica dónde el runner SSH escribe JSON de resultados y hashes; `WAN_SSH_EVIDENCE` permite una captura de la sesión de eco ya autenticada, con credenciales vacías. No son requisitos para ejecutar pruebas. No se versionan imágenes de revisión ni estado local de confianza. La captura 09 y los PDF anteriores permanecen históricos e intactos.

## Nuevos casos UI, esperado y obtenido

| Caso | Esperado | Obtenido | Estado |
| --- | --- | --- | --- |
| P01 · Sede confirmada, edición y persistencia | Resumen verde/Editar sede, campos bloqueados, edición sin pérdida y JSON/localStorage conservan confirmación. | Confirmada/resumen/bloqueo, Editar, navegación, JSON y localStorage; plan/nodos conservados. | Superada |
| P02 · Previsualización y pools de dos sedes | Automática pendiente antes de cálculo; redes reales en bloques independientes tras VLSM. | LAN en 192.168.32.0/22 y 172.16.0.0/22; tránsito separado; placeholder pendiente/efectivo correctos. | Superada |
| P03 · Capacidad detallada y bloqueo de dependencias | Error identifica sede/VLAN/pool/hosts/reservas; estado pendiente y foco corregible sin perder plan/texto. | Error contextual completo, estado pendiente/foco hosts, plan intacto; topología bloqueada y SSH manual accesible. | Superada |
| P04 · Simulación basada en proyecto | CLI/interfaces/VLAN reales del proyecto, comandos cerrados, limpiar/reiniciar y sin conexiones. | Configuración exacta, interfaces del proyecto, comando no soportado rechazado, reinicio/limpieza sin mutar ni conectar. | Superada |
| P05 · Consola sin Python y bilingüe | Simulación local sin servicio; conexión real indica indisponibilidad, sin alterar datos al traducir. | Help/simulación sin servicio; conexión real deshabilitada e informativa ES/EN, proyecto intacto. | Superada |
| P06 · Gestión explícita y credenciales efímeras | No inferir gestión desde gateway/WAN/endpoint; no serializar secretos y borrarlos al abandonar la vista. | No infiere gestión; campo secreto fuera de JSON/localStorage y eliminado al cambiar idioma/vista. | Superada |
| P07 · Importación antigua y confirmación estricta | Archivo sin flag permanece editable; tipo inválido de confirmación se rechaza atómicamente. | v2 sin flag no se confirma por inferencia; cadena true rechazada sin sustituir estado. | Superada |
| P08 · Edición sin cambios y bloqueo selectivo | Editar sin cambios conserva aprobación; cambios pendientes bloquean derivados sin impedir navegación independiente. | Sede pendiente bloquea topología; revertir/confirmar conserva diseño y calculadora permanece independiente. | Superada |

## Casos SSH real local

Cada fila corresponde a un método ejecutado en el reporte JSON. “SSH real” significa negociación/autenticación/shell/PTY a un servidor local genuino, no simulación de protocolo ni certificación de hardware. Su shell controlado devuelve eco; no ejecuta comandos OS. Las credenciales de prueba se generan por ejecución y no son credenciales reales ni valores predeterminados de la aplicación.

| Caso | Comprobación y resultado observado | Estado |
| --- | --- | --- |
| `test_authorization_deadline` | WS sin primer mensaje autorizado vence a los cinco segundos y libera sesión. | Superada |
| `test_bootstrap_and_host_boundary` | Bootstrap sin cabecera/origen válido, Host falso y archivos ajenos bloqueados; sin CORS permisivo. | Superada |
| `test_browser_xterm_real` | Navegador→HTTP/WS→SSH real: xterm representa ANSI/eco; teclas llegan, contraseña queda vacía, modelo/storage intactos y resize móvil correcto. | Superada |
| `test_cancel_during_negotiation` | Cerrar WS durante negociación cancela TCP/SSH y libera cupo, sin PTY posterior. | Superada |
| `test_changed_host_key` | Host con clave diferente rechazado antes de autenticar. | Superada |
| `test_closed_port_network_error` | Puerto TCP cerrado devuelve error de red. | Superada |
| `test_credentials_never_persist_or_log` | Contraseña y entrada marcada no aparecen en logs ni archivos del estado local. | Superada |
| `test_destination_and_dns_pinning` | Host fuera de allowlist y resolución fuera de IP fijadas rechazados. | Superada |
| `test_invalid_password` | Contraseña incorrecta rechazada con código authentication; no se muestra conectado. | Superada |
| `test_key_registration_never_replaces_changed_key` | Registro no reemplaza silenciosamente una clave anterior distinta. | Superada |
| `test_malformed_and_input_limits` | Usuario con salto de línea, endpoint exec y entrada >16 KiB rechazados. | Superada |
| `test_network_timeout` | TCP local que no negocia SSH vence por timeout y se limpia. | Superada |
| `test_output_backpressure` | Sin ACK no se envía segundo fragmento; al confirmar llega fragmento ≤4096 bytes. | Superada |
| `test_password_interactive_and_unicode` | Autenticación real, salida ANSI, entrada/salida UTF-8 y Ctrl+C recibidos por el canal SSH. | Superada |
| `test_peer_drop_and_cleanup` | Cierre abrupto de canal remoto avisa y limpia sesión WS. | Superada |
| `test_private_key_authentication` | Clave efímera válida autentica y abre PTY/shell. | Superada |
| `test_pty_refusal_never_marks_connected` | Rechazo PTY devuelve terminal_unsupported; no inventa terminal ni marca conectado. | Superada |
| `test_pty_resize_disconnect_reconnect` | Resize 100×40 recibido; desconexión limpia y reconexión autenticada. | Superada |
| `test_register_key_requires_exact_fingerprint` | Huella incorrecta no modifica confianza; huella exacta permite conexión. | Superada |
| `test_scalar_and_oversized_frames` | JSON escalar rechazado, frame >64 KiB cerrado 1009 y cupo liberado. | Superada |
| `test_service_shutdown_closes_ssh` | Apagar servicio cierra canales SSH del laboratorio. | Superada |
| `test_session_token_isolation` | Token de otra autorización de navegador no permite abrir sesión. | Superada |
| `test_simultaneous_session_isolation_and_limit` | Dos sesiones aisladas, salida de una no llega a otra, tercera sesión rechazada 429. | Superada |
| `test_stderr_and_remote_eof` | Salida stderr se representa y EOF remoto termina sesión. | Superada |
| `test_unknown_host_key` | Host desconocido rechazado antes de enviar credenciales (contador de autenticaciones 0). | Superada |
| `test_ws_requires_origin_cookie_and_csrf` | Orígenes externo/null/otro puerto, falta de cookie y CSRF inválido rechazados. | Superada |

## Hashes y verificaciones adicionales

| Archivo probado | SHA-256 |
| --- | --- |
| WAN_v4.html | `e2076b9d4e66fc60624dcd869cefdac001b8dbb30f20e109ce37ae56f56ac58e` |
| tests/test_corte3.py | `45ac6b79e80313cb7c933d7491441ab8d3416c47ef7796ea8f1d7e6c74abc871` |
| ssh_service/server.py | `b4a2a974703100355c6f11ea37c4f48d21cc41c6bc0e77cf04094b1feb8c6efa` |
| tests/test_ssh_service.py | `0d2db268b356330b16caa95eda275913241f080ea023ac8d6172118bc4901be3` |

Sintaxis JS/Python/JSON y diff-check revisados. HTML5 del documento y 30 fragmentos de vistas ES/EN (incluidas ambas modalidades SSH) sin errores de parseo mediante herramienta temporal fuera del repositorio. Revisión visual de sede confirmada, simulación ES/EN a 1440/390 px y terminal SSH local auténtica. Sin errores JS en casos limpios. Fallos de red/autenticación esperados se muestran en UI, no como éxito.

La apertura file:// bloqueada y Windows no ejecutado son límites separados, no se ocultan en el 100% de las matrices. No se certifican conectividad WAN, firmware de fabricantes, seguridad exhaustiva, accesibilidad completa ni funcionamiento en todo navegador. No se aplicaron las configuraciones generadas.
