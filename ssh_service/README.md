# Servicio SSH local opcional de WAN Architect

Solo hace falta para **Conexión real**. HTML, simulación, direccionamiento y generadores funcionan sin Python ni estas dependencias. No aplica configuraciones: abre un shell remoto para que el usuario escriba manualmente en un equipo autorizado.

## Arquitectura y elección

`WAN_v4.html → HTTP/WebSocket 127.0.0.1:8765 → AsyncSSH → destino SSH:22`

HTTP y WS comparten puerto configurable. El servicio escucha exclusivamente en 127.0.0.1; no hay opción de bind público, CORS ni listado de directorios. Solo sirve WAN_v4.html, tres recursos de terminal y el manual SSH. AsyncSSH 2.24.1 aporta SSH/PTY asíncrono y evita hilos de lectura por sesión; aiohttp 3.14.5 sirve HTTP/WS en el mismo bucle. xterm.js 6.0.0 y addon-fit 0.11.0 son recursos **locales** con licencias originales en [static](static/). El navegador no abre TCP SSH directamente.

## Windows: instalación desde la raíz del repositorio

Python 3.10+ (recomendado 3.11 o posterior). PowerShell, sin activar scripts ni cambiar ExecutionPolicy:

```powershell
py -m venv .venv-ssh
.\.venv-ssh\Scripts\python.exe -m pip install -r ssh_service\requirements.txt
Copy-Item ssh_service\config.example.json ssh_service\config.json
```

Editar `config.json` para registrar **solo destinos autorizados**. Ejemplo de documentación, no predeterminado (192.0.2.10 es una dirección de documentación: sustituirla por el equipo autorizado):

```json
{
  "http_port": 8765,
  "max_sessions": 4,
  "idle_seconds": 900,
  "connect_seconds": 12,
  "targets": [
    {"host": "192.0.2.10", "port": 22, "addresses": ["192.0.2.10"]}
  ]
}
```

`config.example.json` tiene targets vacíos: **ningún destino autorizado por defecto**. Para un hostname, enumerar todas las IP aprobadas; una resolución DNS diferente se bloquea. No usar comodines. Nunca escribir contraseñas o claves privadas en configuración.

```powershell
.\.venv-ssh\Scripts\python.exe -m ssh_service.server --config ssh_service\config.json
```

Abrir `http://127.0.0.1:8765/WAN_v4.html`, Consola SSH → Conexión real. Alternativa de puerto: añadir `--http-port 8766` y abrir esa misma URL/puerto. El WS es `/ssh/ws` en **ese mismo puerto**, no un segundo servicio; TCP/22 es el destino remoto, no el listener local. Ctrl+C cierra el servicio y las sesiones.

Linux/macOS: `python -m venv .venv-ssh`, `.venv-ssh/bin/python -m pip install -r ssh_service/requirements.txt` y `.venv-ssh/bin/python -m ssh_service.server --config ssh_service/config.json`. No requiere permisos de administrador para el puerto 8765.

## Claves de host: verificar antes de autenticar

La primera conexión falla si la clave no es conocida. Consultar su huella pública (reemplazar IP y puerto):

```powershell
.\.venv-ssh\Scripts\python.exe -m ssh_service.server --config ssh_service\config.json --probe-host 192.0.2.10 --port 22
```

Compararla **fuera de banda** con la consola del equipo o su administrador. No confiar solo en lo que devuelve la red. Tras verificar, registrar usando la huella exacta:

```powershell
.\.venv-ssh\Scripts\python.exe -m ssh_service.server --config ssh_service\config.json --trust-host 192.0.2.10 --port 22 --fingerprint SHA256:HUELLA_VERIFICADA_EXTERNAMENTE
```

El marcador es intencional, no una huella real. Una discrepancia o cambio de clave se rechaza; no existe AutoAddPolicy, aceptación silenciosa ni opción de omitir verificación. Una rotación legítima exige detener el servicio, verificar fuera de banda y revisar manualmente la entrada antigua de `ssh_service/state/known_hosts` antes de registrarla. El archivo guarda confianza pública, nunca credenciales; para DNS se registra la IP fijada y su puerto.

## Autorización y límites de seguridad

- Solo origen `http://127.0.0.1:PUERTO` y Host exactos; rechaza `null`, otros puertos, hosts de rebinding y orígenes externos. No usar file:// para conexión real.
- Bootstrap requiere cabecera no simple del cliente y mismo origen; entrega cookie HttpOnly/SameSite Strict y token CSRF efímero en RAM. El WS exige cookie, origen y token en el primer mensaje, con plazo de cinco segundos. No se pone token en URL ni localStorage.
- El operador confirma la conexión en la interfaz y el backend exige allowlist de host/puerto/IP fijadas. La autorización local no es una cuenta multiusuario: solo debe usarse en un equipo/usuario local confiable. No protege frente a malware con los mismos permisos del sistema operativo.
- Autenticación remota por contraseña o clave privada, con frase opcional. No usa agente SSH ni archivos SSH personales/configuración externa. Datos de autenticación se descartan tras el uso; Python/JavaScript no garantizan borrado criptográfico inmediato de cadenas inmutables en RAM.
- Límites: cuatro sesiones por defecto (máximo configurable 16), 32 autorizaciones de navegador/hora, conexión 12 s (configurable), inactividad de entrada 900 s, frame WS 64 KiB, entrada 16 KiB, clave 32 KiB, salida 4 KiB por fragmento y un fragmento en vuelo con ACK al representar. Sin ACK durante 10 s, cierra. Ventana SSH de canal 64 KiB y scrollback de terminal de 1000 líneas.
- No registra credenciales, cuerpos, comandos, transcript ni access logs. Se muestran códigos estables en errores. `config.json`, estado y `.venv-ssh/` se excluyen de Git. Proteja sus permisos/ACL locales; no copie claves privadas al repositorio.
- Desconectar/cerrar pestaña/cambiar vista o idioma cierra WS/SSH. Cancelar cierra también la negociación en curso, sin abrir un PTY posterior; no inicia comandos. EOF/error SSH y apagado del servicio limpian recursos.
- La entrada se envía como bytes al shell SSH remoto: **no** a subprocess, eval o shell del equipo local. No hay endpoint exec ni aplicación automática del generador.

## Pruebas y alcance

Instalar también `tests/requirements.txt` y Chromium para la prueba de navegador:

```powershell
.\.venv-ssh\Scripts\python.exe -m pip install -r tests\requirements.txt
.\.venv-ssh\Scripts\python.exe -m playwright install chromium
.\.venv-ssh\Scripts\python.exe tests\test_ssh_service.py
```

El laboratorio usa un servidor AsyncSSH auténtico en loopback, claves y credenciales efímeras en RAM y un shell de eco que **no ejecuta procesos**. No son respuestas de fabricantes físicos. Un servidor que rechace shell/PTY muestra error explícito; no se sustituye por ejecución de comandos aislados. La regresión tradicional sigue con `python tests/test_corte3.py`, sin requerir AsyncSSH/aiohttp.

Resultado real, entorno y límites: [pruebas SSH](../docs/pruebas-ssh.md). Se valida en Linux/Chromium; las instrucciones y código evitan dependencias Unix, pero no se afirma una ejecución en Windows ni compatibilidad física certificada con Cisco, Huawei, Fortinet o MikroTik.

## Fuentes oficiales

- [AsyncSSH: API y verificación de servidores](https://asyncssh.readthedocs.io/en/latest/api.html).
- [Código oficial AsyncSSH](https://github.com/ronf/asyncssh).
- [aiohttp: servidor y WebSocket](https://docs.aiohttp.org/en/stable/web_reference.html).
- [xterm.js](https://xtermjs.org/docs/) y [repositorio oficial](https://github.com/xtermjs/xterm.js).
- [Versiones y SHA-256 de recursos locales](static/SOURCES.json); licencias originales junto a los recursos.
