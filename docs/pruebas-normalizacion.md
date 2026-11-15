# Pruebas de normalización final

Fecha de verificación: `2026-11-15T13:47:40-05:00`. Base main `3e3ed118544be32e32aa7cd6f74ca61b3eb74665`; rama `refactor/normalizacion-final-wan-architect`. Los reportes registran este HEAD base del árbol antes de los commits; sus hashes identifican exactamente el código normalizado probado, no una ejecución del código anterior de main.

## Resultado real

**114/114 aplicación + 26/26 SSH local = 140/140 ejecutadas = 100%.** Cero fallidas, bloqueadas o no ejecutadas dentro de esos conjuntos. Esta vez **sí se ejecutaron ambas suites**, porque cambia el texto fuente. No se suman resultados históricos ni comprobaciones visuales al denominador.

- [Reporte completo UI: caso, esperado, obtenido y estado](../tests/reporte-normalizacion.html).
- [Reporte SSH real exclusivamente loopback](../tests/reporte-normalizacion-ssh.json).
- [Equivalencia estática, laboratorio y 56 imágenes por hash RGB](../tests/reporte-normalizacion-equivalencia.json).
- UI: `2026-11-15T13:43:03-05:00`, Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57, 192.6 s.
- SSH: `2026-11-15T18:50:02.719616+00:00`, aiohttp 3.14.5, AsyncSSH 2.24.1; 26 casos, aproximadamente 10 s. Sin equipos externos ni CLI enviada a fabricantes.

## Comandos y entorno

En una instalación normal se recomienda entorno virtual y dependencias ya declaradas:

```bash
python -m pip install -r tests/requirements.txt -r ssh_service/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py --report tests/reporte-normalizacion.html
# Guardar reporte real sin cambiar el runner:
WAN_SSH_REPORT=tests/reporte-normalizacion-ssh.json python tests/test_ssh_service.py
```

En este entorno `asyncssh` no estaba instalado: el primer intento de arrancar el runner SSH se detuvo en importación y **no ejecutó casos**. Se instalaron los requirements existentes en `/tmp/wan-ssh-deps` y se ejecutó el segundo comando con `PYTHONPATH=/tmp/wan-ssh-deps`. Resultado posterior 26/26; no se modificó el runner ni una expectativa. El formateador temporal también quedó fuera del repositorio; no hay dependencias nuevas de la aplicación.

## Comparación antes/después

| Comprobación | Esperado | Obtenido | Estado |
| --- | --- | --- | --- |
| JavaScript | Mismos nodos, literales, operadores, llamadas y flujo AST al ignorar posiciones/formato | AST Acorn idéntico; se conservan claves entrecomilladas y valores de plantillas | Superada |
| CSS | Mismas reglas, valores, selectores y orden/cascada | Forma canónica idéntica al retirar únicamente comentarios/espacio editorial | Superada |
| HTML estático | Mismos elementos, atributos, IDs, eventos y texto | Estructura canónica idéntica; scripts/CSS comparados aparte | Superada |
| Catálogo | Mismo bloque generado y doce fichas | Bloque exacto; `python tools/build_catalogo.py --check` satisfactorio | Superada |
| Python SSH | Mismas instrucciones y política | AST ejecutable idéntico al ignorar docstrings; 19 funciones documentadas | Superada |
| Laboratorio + IPv6 | Conservar intenciones, planes, nodos, enlaces, opciones y 16 CLI | JSON completo idéntico: 21 redes IPv4, 42 nodos, 48 enlaces; IPv6 confirmado | Superada |
| Presentación | Ningún cambio de colores, medidas o disposición | 56/56 imágenes RGB idénticas: 14 vistas × ES/EN × 1440/390 | Superada |
| Aplicación | Conservar 114 casos C/N/P/Q/K/F/L | 114 superados, sin errores de página/consola en los casos registrados | Superada |
| Servicio SSH | Conservar 26 casos, PTY y controles de sesión | 26 superados contra servidor de laboratorio loopback | Superada |

Los recorridos visuales cargaron el botón público, confirmaron IPv6 con un prefijo ULA fijo y calcularon el /26. Se capturó cada vista con scroll inicial y navegador idéntico. Los hashes de píxeles y del JSON anterior/posterior están en el reporte de equivalencia. Las imágenes intermedias quedan fuera del repositorio. Esta comparación de viewport no equivale a probar todos los estados posibles; la suite aporta las interacciones, persistencia y validaciones adicionales.

## Integridad de entradas y referencias

SHA-256 HTML probado: `ecce98974207874cd2fc27a30bde834adda50b6e8475cbf7d843a81911a705cf`.
SHA-256 servidor: `bbbce468c0ddaef0f437e449ed50cf859d0c9d8f8485da10c1865a7e6e030a01`.
No se modificaron scripts de pruebas, fixtures ni referencias CLI. C26 conserva ocho comparaciones exactas de cuatro fabricantes × ES/EN; L01 verifica el laboratorio público completo y L02–L05 inventario, JSON, rollback y determinismo. Compatibilidad v2/v3/v4, IPv4/IPv6, AP sin CLI, simulación/SSH real, descargas y offline permanecen dentro de las suites.


