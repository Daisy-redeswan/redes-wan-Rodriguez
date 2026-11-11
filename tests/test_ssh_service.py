#!/usr/bin/env python3
"""Laboratorio SSH real en loopback, con claves/credenciales efímeras en RAM.

python -m unittest tests/test_ssh_service.py -v no requiere equipos físicos.
También: python tests/test_ssh_service.py (imprime porcentaje y devuelve fallo).
"""
import asyncio
import base64
import contextlib
import io
import json
import hashlib
import os
import platform
import subprocess
import datetime
from pathlib import Path
import secrets
import socket
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asyncssh
from aiohttp import ClientSession, CookieJar, WSServerHandshakeError, web
from ssh_service.server import create_app, load_config, trust_host, PolicyError


class SSHLabTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Genera un servidor SSH auténtico que solo devuelve eco; no ejecuta shell OS."""
        self.hostkey = asyncssh.generate_private_key("ssh-ed25519")
        self.userkey = asyncssh.generate_private_key("ssh-ed25519")
        self.password = secrets.token_urlsafe(24)
        self.clients = set()
        self.sizes = []
        self.pty_allowed = True
        self.received = []
        self.auth_calls = 0
        owner = self

        class Server(asyncssh.SSHServer):
            def begin_auth(self, username): return True
            def password_auth_supported(self): return True
            def public_key_auth_supported(self): return True
            def validate_password(self, username, password):
                owner.auth_calls += 1
                return username == "lab" and secrets.compare_digest(password, owner.password)
            def validate_public_key(self, username, key): return username == "lab" and key == owner.userkey.convert_to_public()
            def session_requested(self): return Session()

        class Session(asyncssh.SSHServerSession):
            def connection_made(self, channel):
                self.channel = channel
                owner.clients.add(self)
            def pty_requested(self, term_type, term_size, term_modes):
                owner.sizes.append(term_size)
                return owner.pty_allowed
            def shell_requested(self): return True
            def session_started(self): self.channel.write("\x1b[32mLAB SSH READY\x1b[0m\r\n")
            def data_received(self, data, datatype):
                owner.received.append(data)
                if data.startswith("stderr"): self.channel.write("LAB STDERR\r\n",asyncssh.EXTENDED_DATA_STDERR)
                elif "\x03" in data: self.channel.write("CTRL-C\r\n")
                elif "exit" in data: self.channel.write("BYE\r\n"); self.channel.exit(0)
                else: self.channel.write("ECHO:" + data.replace("\r", "\r\n"))
            def terminal_size_changed(self, width, height, pixwidth, pixheight): owner.sizes.append((width, height, pixwidth, pixheight))
            def connection_lost(self, exc): owner.clients.discard(self)

        self.ssh = await asyncssh.create_server(Server, "127.0.0.1", 0, server_host_keys=[self.hostkey], line_editor=False)
        self.sshport = self.ssh.get_port()
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0)); self.httpport = sock.getsockname()[1]
        self.config = load_config()
        self.config.update(http_port=self.httpport, max_sessions=2, connect_seconds=2,
                           targets=[dict(host="127.0.0.1",port=self.sshport,addresses=["127.0.0.1"])])
        self.tmp = tempfile.TemporaryDirectory(prefix="wan-ssh-lab-")
        self.app = create_app(self.config, self.tmp.name)
        self.runner = web.AppRunner(self.app, access_log=None)
        await self.runner.setup()
        await web.TCPSite(self.runner,"127.0.0.1",self.httpport).start()
        self.origin = f"http://127.0.0.1:{self.httpport}"
        self.http = ClientSession(cookie_jar=CookieJar(unsafe=True))
        self.token = await self.authorize(self.http)
        await trust_host(self.config,"127.0.0.1",self.sshport,self.hostkey.get_fingerprint("sha256"),self.tmp.name)

    async def asyncTearDown(self):
        await self.http.close()
        await self.runner.cleanup()
        self.ssh.close(); await self.ssh.wait_closed()
        self.tmp.cleanup()

    async def authorize(self, client):
        async with client.get(self.origin+"/ssh/bootstrap",headers={"X-WAN-Client":"ssh-ui"}) as response:
            self.assertEqual(response.status,200)
            self.assertNotIn("Access-Control-Allow-Origin",response.headers)
            return (await response.json())["token"]

    async def connect(self, **changes):
        ws = await self.http.ws_connect(self.origin+"/ssh/ws",origin=self.origin)
        payload=dict(type="connect",token=self.token,host="127.0.0.1",port=self.sshport,user="lab",method="password",password=self.password,cols=80,rows=24)
        payload.update(changes)
        await ws.send_json(payload)
        response = await asyncio.wait_for(ws.receive_json(),5)
        return ws,response

    async def text(self, ws, target):
        combined=""
        for _ in range(20):
            message=await asyncio.wait_for(ws.receive_json(),3)
            if message.get("type")=="output":
                combined+=base64.b64decode(message["data"]).decode("utf-8")
                await ws.send_json({"type":"ack"})
            if target in combined:return combined
        self.fail("No se recibió salida esperada")

    async def test_password_interactive_and_unicode(self):
        ws,reply=await self.connect();self.assertEqual(reply,{"type":"status","status":"connected"})
        await self.text(ws,"LAB SSH READY")
        await ws.send_json({"type":"input","data":"hola áé\r"});self.assertIn("hola áé",await self.text(ws,"hola áé"))
        await ws.send_json({"type":"input","data":"\x03"});await self.text(ws,"CTRL-C");await ws.close()

    async def test_stderr_and_remote_eof(self):
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        await ws.send_json({"type":"input","data":"stderr\r"});await self.text(ws,"LAB STDERR")
        await ws.send_json({"type":"input","data":"exit\r"});await self.text(ws,"BYE")
        reply=await ws.receive_json();self.assertEqual(reply.get("status"),"ended");await ws.close()

    async def test_output_backpressure(self):
        ws,reply=await self.connect();message=await ws.receive_json();self.assertEqual(message['type'],'output')
        await ws.send_json({'type':'input','data':'x'*12000})
        with self.assertRaises(asyncio.TimeoutError):await asyncio.wait_for(ws.receive(),.1)
        await ws.send_json({'type':'ack'});message=await ws.receive_json();self.assertEqual(message['type'],'output');self.assertLessEqual(len(base64.b64decode(message['data'])),4096);await ws.close()

    async def test_pty_refusal_never_marks_connected(self):
        self.pty_allowed=False
        ws,reply=await self.connect();self.assertEqual(reply['code'],'terminal_unsupported');await ws.close()

    async def test_invalid_password(self):
        ws,reply=await self.connect(password=secrets.token_urlsafe(12));self.assertEqual(reply["code"],"authentication");await ws.close()

    async def test_private_key_authentication(self):
        ws,reply=await self.connect(method="key",password="",privateKey=self.userkey.export_private_key().decode())
        self.assertEqual(reply.get("status"),"connected");await self.text(ws,"LAB SSH READY");await ws.close()

    async def test_unknown_host_key(self):
        self.app["known_hosts"].write_text("")
        ws,reply=await self.connect();self.assertEqual(reply["code"],"host_key");self.assertEqual(self.auth_calls,0);await ws.close()

    async def test_changed_host_key(self):
        other=asyncssh.generate_private_key("ssh-ed25519")
        self.app["known_hosts"].write_text(f"[127.0.0.1]:{self.sshport} "+other.export_public_key().decode())
        ws,reply=await self.connect();self.assertEqual(reply["code"],"host_key");self.assertEqual(self.auth_calls,0);await ws.close()

    async def test_register_key_requires_exact_fingerprint(self):
        self.app["known_hosts"].write_text("")
        with self.assertRaises(PolicyError):await trust_host(self.config,"127.0.0.1",self.sshport,"SHA256:incorrect",self.tmp.name)
        self.assertEqual(self.app["known_hosts"].read_text(),"")
        await trust_host(self.config,"127.0.0.1",self.sshport,self.hostkey.get_fingerprint("sha256"),self.tmp.name)
        ws,reply=await self.connect();self.assertEqual(reply.get("status"),"connected");await ws.close()

    async def test_key_registration_never_replaces_changed_key(self):
        other=asyncssh.generate_private_key("ssh-ed25519")
        self.app["known_hosts"].write_text(f"[127.0.0.1]:{self.sshport} "+other.export_public_key().decode())
        with self.assertRaises(PolicyError):await trust_host(self.config,"127.0.0.1",self.sshport,self.hostkey.get_fingerprint("sha256"),self.tmp.name)

    async def test_destination_and_dns_pinning(self):
        ws,reply=await self.connect(host="localhost");self.assertEqual(reply["code"],"destination_denied");await ws.close()
        self.config["targets"][0]["addresses"]=["192.0.2.1"]
        ws,reply=await self.connect();self.assertEqual(reply["code"],"destination_denied");await ws.close()

    async def test_closed_port_network_error(self):
        with socket.socket() as sock:sock.bind(("127.0.0.1",0));closed=sock.getsockname()[1]
        self.config["targets"][0]["port"]=closed
        ws,reply=await self.connect(port=closed);self.assertEqual(reply["code"],"network");await ws.close()

    async def test_network_timeout(self):
        async def silent(reader,writer):
            try:await reader.read()
            finally:writer.close();await writer.wait_closed()
        server=await asyncio.start_server(silent,"127.0.0.1",0)
        port=server.sockets[0].getsockname()[1];self.config["targets"][0]["port"]=port
        try:
            ws,reply=await self.connect(port=port);self.assertEqual(reply["code"],"network");await ws.close()
        finally:server.close();await server.wait_closed()

    async def test_pty_resize_disconnect_reconnect(self):
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        await ws.send_json({"type":"resize","cols":100,"rows":40});await asyncio.sleep(.05)
        self.assertTrue(any(size[:2]==(100,40) for size in self.sizes))
        await ws.send_json({"type":"disconnect"});await ws.close();await asyncio.sleep(.05)
        self.assertFalse(self.clients)
        ws,reply=await self.connect();self.assertEqual(reply.get("status"),"connected");await ws.close()

    async def test_simultaneous_session_isolation_and_limit(self):
        a,_=await self.connect();b,_=await self.connect();await self.text(a,"LAB SSH READY");await self.text(b,"LAB SSH READY")
        with self.assertRaises(WSServerHandshakeError) as error:await self.http.ws_connect(self.origin+"/ssh/ws",origin=self.origin)
        self.assertEqual(error.exception.status,429)
        await a.send_json({"type":"input","data":"ONLY-A\r"});self.assertIn("ONLY-A",await self.text(a,"ONLY-A"))
        with self.assertRaises(asyncio.TimeoutError):await asyncio.wait_for(b.receive(),.1)
        await a.close();await b.close()

    async def test_ws_requires_origin_cookie_and_csrf(self):
        for origin in ["http://evil.example","null","http://127.0.0.1:9999"]:
            with self.assertRaises(WSServerHandshakeError):await self.http.ws_connect(self.origin+"/ssh/ws",origin=origin)
        async with ClientSession() as anonymous:
            with self.assertRaises(WSServerHandshakeError):await anonymous.ws_connect(self.origin+"/ssh/ws",origin=self.origin)
        ws,reply=await self.connect(token="wrong");self.assertEqual(reply["code"],"unauthorized");await ws.close()

    async def test_bootstrap_and_host_boundary(self):
        async with self.http.get(self.origin+"/ssh/bootstrap") as response:self.assertEqual(response.status,403)
        async with self.http.get(self.origin+"/ssh/bootstrap",headers={"X-WAN-Client":"ssh-ui","Origin":"http://evil.example"}) as response:self.assertEqual(response.status,403)
        async with self.http.get(self.origin,headers={"Host":"evil.example"}) as response:self.assertEqual(response.status,403)
        async with self.http.get(self.origin+"/ssh_service/static/../../AGENTS.md") as response:self.assertEqual(response.status,404)
        async with self.http.get(self.origin+"/ssh_service/static/LICENSE-xterm") as response:self.assertEqual(response.status,404)

    async def test_malformed_and_input_limits(self):
        ws,reply=await self.connect(user="lab\ncommand");self.assertEqual(reply["code"],"invalid_request");await ws.close()
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        await ws.send_json({"type":"exec","command":"anything"});reply=await ws.receive_json();self.assertEqual(reply["code"],"invalid_request");await ws.close()
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        await ws.send_json({"type":"input","data":"x"*17000});reply=await ws.receive_json();self.assertEqual(reply["code"],"invalid_request");await ws.close()

    async def test_scalar_and_oversized_frames(self):
        ws=await self.http.ws_connect(self.origin+'/ssh/ws',origin=self.origin)
        await ws.send_json(7);reply=await ws.receive_json();self.assertEqual(reply['code'],'unauthorized');await ws.close()
        ws=await self.http.ws_connect(self.origin+'/ssh/ws',origin=self.origin)
        await ws.send_str('x'*70000);packet=await ws.receive();self.assertEqual(packet.data,1009);await ws.close()
        await asyncio.sleep(.05);self.assertFalse(self.app['sessions'])

    async def test_authorization_deadline(self):
        ws=await self.http.ws_connect(self.origin+'/ssh/ws',origin=self.origin)
        reply=await asyncio.wait_for(ws.receive_json(),6);self.assertEqual(reply['code'],'unauthorized');await ws.close()
        await asyncio.sleep(.05);self.assertFalse(self.app['sessions'])

    async def test_session_token_isolation(self):
        async with ClientSession(cookie_jar=CookieJar(unsafe=True)) as other:
            other_token=await self.authorize(other);self.assertNotEqual(other_token,self.token)
            ws=await other.ws_connect(self.origin+"/ssh/ws",origin=self.origin)
            await ws.send_json({"type":"connect","token":self.token});reply=await ws.receive_json();self.assertEqual(reply["code"],"unauthorized");await ws.close()

    async def test_cancel_during_negotiation(self):
        closed=asyncio.Event()
        async def silent(reader,writer):
            try:await reader.read()
            finally:writer.close();await writer.wait_closed();closed.set()
        server=await asyncio.start_server(silent,'127.0.0.1',0)
        port=server.sockets[0].getsockname()[1];self.config['targets'][0]['port']=port
        try:
            ws=await self.http.ws_connect(self.origin+'/ssh/ws',origin=self.origin)
            await ws.send_json(dict(type='connect',token=self.token,host='127.0.0.1',port=port,user='lab',method='password',password=self.password))
            await asyncio.sleep(.05);await ws.close();await asyncio.wait_for(closed.wait(),1)
            await asyncio.sleep(.05);self.assertFalse(self.app['sessions'])
        finally:server.close();await server.wait_closed()

    async def test_peer_drop_and_cleanup(self):
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        for session in list(self.clients):session.channel.abort()
        packet=await asyncio.wait_for(ws.receive_json(),3)
        self.assertIn(packet.get("type"),["status","error"])
        await ws.close();await asyncio.sleep(.05);self.assertFalse(self.app["sessions"])

    async def test_service_shutdown_closes_ssh(self):
        ws,reply=await self.connect();await self.text(ws,"LAB SSH READY")
        await self.app.shutdown();await asyncio.sleep(.05);self.assertFalse(self.clients);await ws.close()

    async def test_credentials_never_persist_or_log(self):
        import logging
        stream=io.StringIO();handler=logging.StreamHandler(stream);logging.getLogger().addHandler(handler)
        try:
            ws,reply=await self.connect();await self.text(ws,"LAB SSH READY");await ws.send_json({"type":"input","data":"SENSITIVE-LAB\r"});await self.text(ws,"SENSITIVE-LAB");await ws.close()
            self.assertNotIn(self.password,stream.getvalue());self.assertNotIn("SENSITIVE-LAB",stream.getvalue())
            for file in Path(self.tmp.name).iterdir():self.assertNotIn(self.password,file.read_text())
        finally:logging.getLogger().removeHandler(handler)

    async def test_browser_xterm_real(self):
        """Navegador -> HTTP/WS -> SSH real local, sin infraestructura de fabricante."""
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            bundled=Path(p.chromium.executable_path)
            executable=os.environ.get('CHROMIUM_EXECUTABLE') or (str(bundled) if bundled.is_file() else shutil.which('chromium') or shutil.which('chromium-browser'))
            if not executable:raise RuntimeError('Instale Chromium con python -m playwright install chromium')
            browser=await p.chromium.launch(executable_path=executable,headless=True)
            try:
                context=await browser.new_context(viewport={"width":1440,"height":1000});page=await context.new_page();errors=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                await page.goto(self.origin+"/WAN_v4.html");await page.evaluate("go(13);sshTab('real')")
                await page.locator('#sshHost').fill('127.0.0.1');await page.locator('#sshPort').fill(str(self.sshport));await page.locator('#sshUser').fill('lab');await page.locator('#sshPassword').fill(self.password);await page.locator('#sshAuthorization').check()
                before=await page.evaluate('JSON.stringify(state)');await page.locator('#sshConnect').click();await page.wait_for_function("sshStatusCode==='connected'")
                await page.wait_for_function("sshTerminal.buffer.active.getLine(0)?.translateToString().includes('LAB SSH READY')")
                await page.locator('.xterm-helper-textarea').focus();await page.keyboard.type('hola');await page.keyboard.press('Enter')
                await page.wait_for_function("Array.from({length:sshTerminal.buffer.active.length},(_,i)=>sshTerminal.buffer.active.getLine(i)?.translateToString()).join(String.fromCharCode(10)).includes('ECHO:a')")
                self.assertIn('hola', ''.join(self.received))
                self.assertEqual(await page.locator('#sshPassword').input_value(),'');self.assertEqual(await page.evaluate('JSON.stringify(state)'),before)
                self.assertNotIn(self.password,await page.evaluate('JSON.stringify(localStorage)'))
                if os.environ.get('WAN_SSH_EVIDENCE'):
                    await page.screenshot(path=os.environ['WAN_SSH_EVIDENCE'],full_page=True)
                await page.set_viewport_size({"width":390,"height":844});await asyncio.sleep(.15);self.assertGreater(len(self.sizes),1)
                self.assertTrue(await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                await page.locator('#sshDisconnect').click();await asyncio.sleep(.1);self.assertFalse(self.clients);self.assertFalse(errors,errors)
                await context.close()
            finally:await browser.close()


if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(SSHLabTests)
    class Records(unittest.TextTestResult):
        def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
        def addSuccess(self,test):super().addSuccess(test);self.records.append({'case':test._testMethodName,'status':'passed'})
        def addFailure(self,test,error):super().addFailure(test,error);self.records.append({'case':test._testMethodName,'status':'failed'})
        def addError(self,test,error):super().addError(test,error);self.records.append({'case':test._testMethodName,'status':'error'})
    result=unittest.TextTestRunner(verbosity=2,resultclass=Records).run(suite)
    executed=result.testsRun-len(result.skipped);passed=executed-len(result.failures)-len(result.errors)
    print(f"SSH real local: {passed}/{executed} = {100*passed/executed if executed else 0:.2f}%; bloqueadas/no ejecutadas={len(result.skipped)}")
    if os.environ.get('WAN_SSH_REPORT'):
        report={'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'python':platform.python_version(),'aiohttp':__import__('aiohttp').__version__,'asyncssh':asyncssh.__version__,'server_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'ssh_service/server.py').read_bytes()).hexdigest(),'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'records':result.records,'passed':passed,'executed':executed,'skipped':len(result.skipped)}
        Path(os.environ['WAN_SSH_REPORT']).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
