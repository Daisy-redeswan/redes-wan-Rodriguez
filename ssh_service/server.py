"""HTTP/WebSocket local -> AsyncSSH. No ejecuta procesos del sistema ni CLI automática.

Arranque explícito: python -m ssh_service.server --config ssh_service/config.json
El mismo puerto sirve HTML, recursos y WS; solo 127.0.0.1, sin CORS.
"""
from __future__ import annotations

import argparse
import asyncio
import contextlib
import ipaddress
import json
import re
import secrets
import socket
import time
from pathlib import Path

try:
    import asyncssh
    from aiohttp import web, WSMsgType
except ImportError:
    raise SystemExit("Dependencias opcionales ausentes: python -m pip install -r ssh_service/requirements.txt") from None

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
DEFAULT_STATE = Path(__file__).resolve().parent / "state"
COOKIE = "wan_ssh_session"


class PolicyError(ValueError):
    """Error de política con código público; nunca incluye secretos ni comandos."""


def integer(value, low, high):
    """Exige entero real en límites; bool y cadenas no son puertos/tamaños válidos."""
    if type(value) is not int or not low <= value <= high:
        raise PolicyError("invalid_request")
    return value


def load_config(path=None):
    """Valida la configuración local. Lista vacía prohíbe TODOS los destinos.

    Cada target fija host, puerto y direcciones IP exactas aprobadas. No hay
    comodines ni redes abiertas; un hostname que cambie a otra IP se rechaza.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8")) if path else {}
    if not isinstance(raw, dict) or set(raw) - {"http_port", "max_sessions", "idle_seconds", "connect_seconds", "targets"}:
        raise PolicyError("invalid_config")
    config = dict(http_port=integer(raw.get("http_port", 8765), 1024, 65535),
                  max_sessions=integer(raw.get("max_sessions", 4), 1, 16),
                  idle_seconds=integer(raw.get("idle_seconds", 900), 5, 3600),
                  connect_seconds=integer(raw.get("connect_seconds", 12), 1, 60), targets=[])
    targets = raw.get("targets", [])
    if not isinstance(targets, list) or len(targets) > 100:
        raise PolicyError("invalid_config")
    for target in targets:
        if not isinstance(target, dict) or set(target) != {"host", "port", "addresses"}:
            raise PolicyError("invalid_config")
        host = target["host"]
        if not isinstance(host, str) or len(host) > 253 or not re.fullmatch(r"[A-Za-z0-9_.:-]+", host):
            raise PolicyError("invalid_config")
        addresses = target["addresses"]
        if not isinstance(addresses, list) or not 1 <= len(addresses) <= 16:
            raise PolicyError("invalid_config")
        addresses = [str(ipaddress.ip_address(value)) for value in addresses]
        if any(ipaddress.ip_address(value).is_multicast or ipaddress.ip_address(value).is_unspecified for value in addresses):
            raise PolicyError("invalid_config")
        config["targets"].append(dict(host=host.lower(), port=integer(target["port"], 1, 65535), addresses=addresses))
    return config


async def destination(config, host, port):
    """Resuelve solo nombres autorizados y conecta a una IP fijada, evitando rebinding."""
    if not isinstance(host, str):
        raise PolicyError("destination_denied")
    port = integer(port, 1, 65535)
    target = next((item for item in config["targets"] if item["host"] == host.lower() and item["port"] == port), None)
    if target is None:
        raise PolicyError("destination_denied")
    records = await asyncio.wait_for(asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM), config["connect_seconds"])
    resolved = sorted({str(ipaddress.ip_address(item[4][0])) for item in records})
    if not resolved or not set(resolved).issubset(target["addresses"]):
        raise PolicyError("destination_denied")
    return resolved[0], port


async def public_error(ws, code):
    """Envía un código estable; cerrar transporte nunca produce un traceback sensible."""
    if not ws.closed:
        with contextlib.suppress(ConnectionError, RuntimeError):
            await ws.send_json({"type": "error", "code": code})


async def connect_for_socket(ws, host, port, options, timeout):
    """Cancela negociación SSH si se cierra WS; no abre un PTY después de cancelar.

    Las dos tareas pertenecen a esta solicitud y se recogen siempre. Si la conexión
    terminó al mismo tiempo que el cierre, también se cierra antes de devolver.
    """
    async def opening():
        return await asyncssh.connect(host, port, **options)
    connecting = asyncio.create_task(opening())
    closing = asyncio.create_task(ws.receive())
    try:
        done, _ = await asyncio.wait({connecting, closing}, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        if not done:
            raise asyncio.TimeoutError()
        if closing in done:
            if connecting.done() and not connecting.cancelled() and connecting.exception() is None:
                connection = connecting.result()
                connection.close()
                await asyncio.wait_for(connection.wait_closed(), 3)
            return None
        return connecting.result()
    finally:
        for task in (connecting, closing):
            if not task.done(): task.cancel()
        for task in (connecting, closing):
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task


def create_app(config, state_dir=DEFAULT_STATE):
    """Construye el servicio sin iniciarlo: facilita pruebas reales en loopback.

    Estado de confianza queda fuera de JSON del proyecto. Cookie HttpOnly + token
    CSRF en RAM vinculan el WS a una pestaña autorizada del mismo origen.
    """
    state_dir = Path(state_dir)
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    known = state_dir / "known_hosts"
    known.touch(mode=0o600, exist_ok=True)
    # Un solo proceso es dueño de este estado; límites incluyen sesiones conectando.
    sessions, browsers = set(), {}
    origin = f"http://127.0.0.1:{config['http_port']}"

    @web.middleware
    async def boundary(request, handler):
        """Bloquea DNS rebinding, orígenes ajenos y caché; no registra URLs ni cuerpos."""
        if request.host != f"127.0.0.1:{config['http_port']}":
            raise web.HTTPForbidden()
        incoming = request.headers.get("Origin")
        if incoming and incoming != origin:
            raise web.HTTPForbidden()
        response = await handler(request)
        response.headers.update({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
                                 "Cross-Origin-Resource-Policy": "same-origin", "Referrer-Policy": "no-referrer",
                                 "X-Frame-Options": "DENY"})
        return response

    app = web.Application(middlewares=[boundary], client_max_size=65536)
    app["config"], app["sessions"], app["known_hosts"] = config, sessions, known

    async def index(request):
        """Sirve solo la aplicación autorizada, sin directorio de archivos arbitrarios."""
        html = (ROOT / "WAN_v4.html").read_text(encoding="utf-8")
        return web.Response(text=html.replace("</head>", '<meta name="wan-ssh-service" content="1"></head>', 1), content_type="text/html")

    async def asset(request):
        """Lista explícita de recursos vendorizados; no admite traversal ni fuentes remotas."""
        name = request.match_info["name"]
        if name not in {"xterm.js", "xterm.css", "addon-fit.js"}:
            raise web.HTTPNotFound()
        return web.FileResponse(STATIC / name)

    async def bootstrap(request):
        """Autoriza únicamente fetch del mismo origen con cabecera no simple.

        Otra página no puede leer el token mediante SOP ni superar el preflight;
        la cookie es HttpOnly/SameSite Strict y caduca al cerrar/reiniciar el servicio.
        """
        if request.headers.get("X-WAN-Client") != "ssh-ui" or request.headers.get("Sec-Fetch-Site", "same-origin") not in {"same-origin", "none"}:
            raise web.HTTPForbidden()
        now = time.monotonic()
        for sid in list(browsers):
            if browsers[sid][1] < now:
                del browsers[sid]
        sid = request.cookies.get(COOKIE)
        if sid not in browsers:
            if len(browsers) >= 32:
                raise web.HTTPTooManyRequests()
            sid = secrets.token_urlsafe(32)
            browsers[sid] = (secrets.token_urlsafe(32), now + 3600)
        response = web.json_response({"token": browsers[sid][0]})
        response.set_cookie(COOKIE, sid, httponly=True, samesite="Strict", path="/", max_age=3600)
        return response

    async def websocket(request):
        """Una sesión = un WS autenticado + un shell SSH/PTY. Nunca exec de shell local."""
        if request.headers.get("Origin") != origin:
            raise web.HTTPForbidden()
        session = browsers.get(request.cookies.get(COOKIE, ""))
        if not session or session[1] < time.monotonic():
            raise web.HTTPUnauthorized()
        if len(sessions) >= config["max_sessions"]:
            raise web.HTTPTooManyRequests()
        ws = web.WebSocketResponse(max_msg_size=65536, heartbeat=20, receive_timeout=config["idle_seconds"])
        await ws.prepare(request)
        sessions.add(ws)
        connection = process = reader = None
        message, options = {}, {}
        password = key = phrase = None
        try:
            try:
                message = await asyncio.wait_for(ws.receive_json(), 5)
            except asyncio.TimeoutError:
                raise PolicyError("unauthorized") from None
            if not isinstance(message, dict) or message.get("type") != "connect" or not isinstance(message.get("token"), str) or not secrets.compare_digest(message["token"], session[0]):
                raise PolicyError("unauthorized")
            allowed = {"type", "token", "host", "port", "user", "method", "password", "privateKey", "passphrase", "cols", "rows"}
            if set(message) - allowed:
                raise PolicyError("invalid_request")
            host, port = await destination(config, message.get("host"), message.get("port", 22))
            user = message.get("user")
            if not isinstance(user, str) or not re.fullmatch(r"[A-Za-z0-9_.@\\-]{1,64}", user):
                raise PolicyError("invalid_request")
            cols, rows = integer(message.get("cols", 80), 20, 300), integer(message.get("rows", 24), 5, 120)
            options = dict(username=user, known_hosts=str(known), agent_path=None,
                           connect_timeout=config["connect_seconds"], login_timeout=config["connect_seconds"],
                           config=None, client_keys=[], password=None, kbdint_auth=False)
            if message.get("method") == "password":
                password = message.get("password")
                if not isinstance(password, str) or not 1 <= len(password) <= 1024:
                    raise PolicyError("invalid_request")
                options["password"] = password
            elif message.get("method") == "key":
                key = message.get("privateKey")
                phrase = message.get("passphrase", "")
                if not isinstance(key, str) or not 1 <= len(key) <= 32768 or not isinstance(phrase, str) or len(phrase) > 1024:
                    raise PolicyError("invalid_request")
                try:
                    options["client_keys"] = [asyncssh.import_private_key(key, passphrase=phrase or None)]
                except (ValueError, asyncssh.KeyImportError):
                    raise PolicyError("authentication") from None
            else:
                raise PolicyError("invalid_request")
            # Identidad del servidor se verifica ANTES de enviar la contraseña.
            connection = await connect_for_socket(ws, host, port, options, config["connect_seconds"] + 2)
            if connection is None:
                return ws
            options.clear()
            password = key = phrase = None
            message.clear()  # Credenciales no se retienen en el bucle ni en logs/archivos.
            output_ack = asyncio.Event()
            try:
                process = await connection.create_process(term_type="xterm-256color", term_size=(cols, rows), encoding=None, stderr=asyncssh.STDOUT, window=65536, max_pktsize=16384)
            except asyncssh.ChannelOpenError:
                raise PolicyError("terminal_unsupported") from None
            await ws.send_json({"type": "status", "status": "connected"})

            async def output():
                """Backpressure y EOF/error remoto: cerrar WS sin conservar historial."""
                import base64
                try:
                    while True:
                        chunk = await process.stdout.read(4096)
                        if not chunk:
                            if not ws.closed: await ws.send_json({"type": "status", "status": "ended"})
                            break
                        output_ack.clear()
                        await ws.send_json({"type": "output", "data": base64.b64encode(chunk).decode("ascii")})
                        # Un fragmento en vuelo; el navegador confirma tras representarlo.
                        await asyncio.wait_for(output_ack.wait(), 10)
                except (asyncssh.Error, OSError, asyncio.TimeoutError):
                    if not ws.closed:
                        with contextlib.suppress(ConnectionError):
                            await public_error(ws, "network")
                finally:
                    await ws.close()

            reader = asyncio.create_task(output())
            async for packet in ws:
                if packet.type != WSMsgType.TEXT:
                    break
                data = json.loads(packet.data)
                if not isinstance(data, dict):
                    raise PolicyError("invalid_request")
                if data.get("type") == "input":
                    value = data.get("data")
                    if not isinstance(value, str) or len(value.encode("utf-8")) > 16384:
                        raise PolicyError("invalid_request")
                    process.stdin.write(value.encode("utf-8"))
                    await process.stdin.drain()
                elif data.get("type") == "ack":
                    output_ack.set()
                elif data.get("type") == "resize":
                    process.change_terminal_size(integer(data.get("cols"), 20, 300), integer(data.get("rows"), 5, 120))
                elif data.get("type") == "disconnect":
                    break
                else:
                    raise PolicyError("invalid_request")
        except asyncssh.HostKeyNotVerifiable:
            await public_error(ws, "host_key")
        except asyncssh.PermissionDenied:
            await public_error(ws, "authentication")
        except PolicyError as error:
            await public_error(ws, str(error))
        except (asyncio.TimeoutError, OSError, asyncssh.Error):
            if not ws.closed:
                await public_error(ws, "network")
        except (ValueError, TypeError, KeyError):
            if not ws.closed:
                await public_error(ws, "invalid_request")
        finally:
            # Cancelación, EOF, error de autenticación y cierre de pestaña llegan aquí.
            if isinstance(message, dict): message.clear()
            options.clear()
            password = key = phrase = None
            if reader:
                reader.cancel()
                with contextlib.suppress(asyncio.CancelledError, Exception):
                    await reader
            if connection:
                connection.close()
                with contextlib.suppress(Exception):
                    await asyncio.wait_for(connection.wait_closed(), 3)
            sessions.discard(ws)
            await ws.close()
        return ws

    async def shutdown(_app):
        """Cerrar WebSockets provoca el finally de cada sesión antes de apagar HTTP."""
        await asyncio.gather(*(ws.close(code=1001) for ws in list(sessions)), return_exceptions=True)
        browsers.clear()

    app.router.add_get("/", index)
    app.router.add_get("/WAN_v4.html", index)
    async def favicon(request):
        """Evita peticiones de icono sin servir archivos adicionales."""
        return web.Response(status=204)

    async def manual(request):
        """Documento local explícito; no expone un directorio arbitrario."""
        return web.Response(text=(ROOT/"docs/manual-ssh.md").read_text(encoding="utf-8"), content_type="text/plain")

    async def interface_catalog(request):
        """Un único recurso de datos local; no admite rutas ni nombres suministrados por el cliente."""
        return web.FileResponse(ROOT / "data" / "catalogo-interfaces.js")

    app.router.add_get("/data/catalogo-interfaces.js", interface_catalog)
    app.router.add_get("/favicon.ico", favicon)
    app.router.add_get("/docs/manual-ssh.md", manual)
    app.router.add_get("/ssh_service/static/{name}", asset)
    app.router.add_get("/ssh/bootstrap", bootstrap)
    app.router.add_get("/ssh/ws", websocket)
    app.on_shutdown.append(shutdown)
    return app


async def trust_host(config, host, port, fingerprint, state_dir=DEFAULT_STATE):
    """Confianza explícita fuera de banda: nunca aceptar TOFU silencioso ni cambios.

    Sin fingerprint solo muestra SHA256. Con él, exige coincidencia y no permite
    reemplazar una entrada previa; rotaciones requieren revisión manual del archivo.
    """
    address, port = await destination(config, host, port)
    key = await asyncio.wait_for(asyncssh.get_server_host_key(address, port, config=None), config["connect_seconds"])
    if key is None:
        raise PolicyError("host_key")
    actual = key.get_fingerprint("sha256")
    if fingerprint is None:
        return actual
    if not secrets.compare_digest(actual, fingerprint):
        raise PolicyError("fingerprint_mismatch")
    state_dir = Path(state_dir)
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = state_dir / "known_hosts"
    label = address if port == 22 else f"[{address}]:{port}"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    entry = label + " " + key.export_public_key().decode("ascii").strip() + "\n"
    existing = [line for line in old.splitlines() if line.split(" ", 1)[0] == label]
    if existing and entry.strip() not in existing:
        raise PolicyError("host_key_changed")
    if not existing:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(entry)
        path.chmod(0o600)
    return actual


def main():
    """CLI Windows/Linux; validación previa y errores públicos sin tracebacks sensibles."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--http-port", type=int)
    parser.add_argument("--probe-host")
    parser.add_argument("--trust-host")
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--fingerprint")
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        if args.http_port:
            config["http_port"] = integer(args.http_port, 1024, 65535)
        if args.probe_host or args.trust_host:
            if args.trust_host and not args.fingerprint:
                raise PolicyError("fingerprint_required")
            print(asyncio.run(trust_host(config, args.trust_host or args.probe_host, args.port, args.fingerprint)))
        else:
            # Desactivar access logs: no se registran rutas, sesiones, comandos o credenciales.
            web.run_app(create_app(config), host="127.0.0.1", port=config["http_port"], access_log=None)
    except (ValueError, OSError, asyncssh.Error) as error:
        parser.exit(1, "Servicio no iniciado: " + (str(error) if isinstance(error, PolicyError) else "configuración/red no válida") + "\n")


if __name__ == "__main__":
    main()
