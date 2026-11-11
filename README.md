# Herramienta de Redes WAN — WAN Architect (trabajo individual)

**Estudiante:** Daisy Jurleny Rodriguez

**Institución:** Fundación Universitaria Compensar

**Materia:** Interconexión de Redes WAN · Ingeniería de Telecomunicaciones

**Repositorio público:** https://github.com/Daisy-redeswan/redes-wan-Rodriguez

## Qué hace esta herramienta

WAN Architect permite diseñar una WAN por sedes, calcular y planificar IPv4/IPv6 y representar dispositivos, enlaces e interfaces. Genera **propuestas IPv4** separadas para Cisco IOS/IOS XE, Huawei VRP, Fortinet FortiOS y MikroTik RouterOS. Funciona localmente en [WAN_v4.html](WAN_v4.html); no aplica comandos sobre equipos.

## Funciones

- **Subnetting / IP Planning:** calculadora IPv4 pública/privada e IPv6; VLSM con fallback y bloques privados independientes por sede/tránsito y subred CIDR manual por VLAN. IPv6 se planifica separadamente con ULA /48, /56 por sede y /64 por VLAN; no tiene broadcast.
- **Topología:** generación desde el plan, edición de dispositivos/enlaces e interfaces y exportación SVG. Una imagen importada es referencia manual, no reconocimiento automático.
- **Cuatro fabricantes:** Cisco, Huawei, Fortinet y MikroTik consumen el mismo modelo validado. FortiOS 7.4 y RouterOS 7.x son supuestos genéricos de laboratorio; ninguna marca está certificada físicamente.
- **Ciberdefensa y uso de IA:** validación de entradas, importación atómica, contenido escapado, administración restringida y marcadores de secretos; [políticas](docs/politicas-ia.md) y [límites](docs/seguridad.md). `.env` y sus variantes quedan excluidos por [.gitignore](.gitignore).
- **Español/English:** español inicial, selector de idioma y preferencia independiente. Traduce la interfaz; conserva nombres introducidos, claves internas, JSON y CLI.
- **Consola SSH:** simulación educativa autónoma y [conexión real opcional](ssh_service/README.md) por servicio Python local, sin aplicar configuraciones automáticamente. [Manual SSH](docs/manual-ssh.md).
- **Persistencia:** JSON v4, migración v2→v3→v4 sin reasignar y localStorage v4 con fallback no destructivo v3/v2.

## Cómo ejecutarla

1. Descargar/clonar el repositorio completo y abrir `WAN_v4.html` en un navegador actualizado. No requiere backend, cuentas ni paquetes para usar la aplicación.
2. Para reproducir pruebas y capturas, desde la raíz ejecutar `python -m http.server 8000 --bind 127.0.0.1` y abrir `http://127.0.0.1:8000/WAN_v4.html`. Detener con Ctrl+C; no exponer ese servidor a Internet.
3. Seguir proyecto → sede → estimación → VLAN/IPv4 → IPv6 opcional → topología → fabricante → revisión y exportación. Confirmar fichas e inventario: guardar valores idénticos conserva el diseño; los cambios reales invalidan únicamente dependencias afectadas. Elegir fabricantes por sede/función antes de generar topología.
4. Cambiar **Idioma / Language** entre Español y English. La preferencia no modifica el proyecto ni sus configuraciones. Guardar/exportar un respaldo JSON; localStorage depende del origen y no cifra los datos.

El [manual](docs/manual.md) explica controles, idiomas, escenarios y limitaciones. Los cuatro generadores siguen siendo IPv4; las configuraciones IPv6 requieren aclaración del alcance docente.

## Pruebas y % de confianza (Corte 3)

**Pruebas actuales: 58/58 UI y regresión + 26/26 SSH local = 84/84 ejecutadas (100%).** En las matrices automatizadas: 0 fallidas/bloqueadas/no ejecutadas. Conserva C01–C31/N01–N19 y añade P01–P08 de confirmaciones/consola y 26 casos SSH reales en loopback. Una comprobación exploratoria file:// fue bloqueada por política; Windows y hardware no ejecutados. Los hashes históricos de cuatro CLI no se sustituyen.

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
```

El runner inicia/cierra HTTP local, crea contextos limpios y devuelve un código no cero ante fallos. El reporte normal es temporal y su ruta se imprime; [casos, resultados, hashes y entorno](docs/pruebas.md), [reporte UI actual](tests/reporte-ssh-ui.html) y [pruebas SSH](docs/pruebas-ssh.md). El porcentaje no certifica toda la aplicación ni hardware, conectividad o seguridad integral.

## Documentos

- [Informe Corte 2](docs/informe-corte2.pdf) · [Informe Corte 3](docs/informe-corte3.pdf).
- [Manual](docs/manual.md) · [Seguridad](docs/seguridad.md) · [Políticas IA](docs/politicas-ia.md) · [Pruebas](docs/pruebas.md).
- [Documentación del código](docs/documentacion-codigo.md).
- [Estado del proyecto](docs/estado-proyecto.md) · [Trazabilidad Corte 3](docs/trazabilidad-corte3.md) · [Matriz de fabricantes](docs/matriz-fabricantes.md).
- La matriz conserva antecedentes de soporte por plataforma; el inventario vigente de pruebas y capturas es el de esta entrega.
- Fuente de requisitos: [Guía Docente.html](<docs/requisitos/Guía Docente.html>).

## Capturas (evidencias)

Las capturas 01–10 y los PDF se conservan intactos como evidencia histórica de main 1956d18 (31 casos); no muestran el rediseño actual. El resultado actual 50/50 está en el reporte enlazado arriba. Se retiró la pantalla de evidencias de la app, no estos archivos.

Las capturas de la aplicación se obtuvieron por HTTP local con Playwright, contexto limpio y datos ficticios. Las propuestas nunca se ejecutaron en infraestructura real.

| Evidencia | Qué se verificó | Archivo exacto |
| --- | --- | --- |
| 01 | IP, prefijo /26, red, broadcast y 62 hosts visibles | [01-subnetting.png](docs/capturas/01-subnetting.png) |
| 02 | Diagrama completo de dos sedes; dispositivos y enlaces sin recorte | [02-topologia.png](docs/capturas/02-topologia.png) |
| 03 | Core Cisco: hostname, VLAN e IP visibles | [03-config-cisco.png](docs/capturas/03-config-cisco.png) |
| 04 | Core Huawei: sysname, VLAN e IP visibles | [04-config-huawei.png](docs/capturas/04-config-huawei.png) |
| 05 | Página real de commits de main, con al menos cinco mensajes claros | [05-github-commits.png](docs/capturas/05-github-commits.png) |
| 06 | Propuesta Fortinet generada por la aplicación | [06-config-fortinet.png](docs/capturas/06-config-fortinet.png) |
| 07 | Propuesta MikroTik generada por la aplicación | [07-config-mikrotik.png](docs/capturas/07-config-mikrotik.png) |
| 08 | IPv4 inválida rechazada; último cálculo válido conservado | [08-ciberdefensa.png](docs/capturas/08-ciberdefensa.png) |
| 09 | Ejecución histórica: 31/31 y 100% visibles | [09-pruebas.png](docs/capturas/09-pruebas.png) |
| 10 | Aplicación funcionando con selector de idioma visible | [10-app-final.png](docs/capturas/10-app-final.png) |

La 05 procede de [Commits en GitHub](https://github.com/Daisy-redeswan/redes-wan-Rodriguez/commits/main/), respuesta HTTPS real 200. Los recursos externos de estilo/avatar quedaron bloqueados en el entorno: se conserva el render nativo sin estilos, legible y sin reconstruir ni alterar sus mensajes. Las otras capturas muestran laboratorios identificados en el manual; no representan un único despliegue de gateways duplicados.

## Autoevaluación (Sí/No con evidencia)

“Sí” indica implementación y evidencia local comprobadas, **no una nota otorgada ni certificación física**. Los pesos de la rúbrica no son el porcentaje de pruebas.

| Criterio de la plantilla docente | ¿Cumplido? | Evidencia concreta |
| --- | --- | --- |
| Subnetting funciona | Sí | Captura 01; C01/C02/C07/C09: IPv4 e IPv6 |
| Carga de topología | Sí | Captura 02; C11 y editores auditados en C28 |
| Config Cisco y Huawei | Sí | Capturas 03/04; C12/C13/C26: generación y texto exacto |
| Config Fortinet y MikroTik (C3) | Sí | Capturas 06/07; C14/C15/C26; validación textual |
| Ciberdefensa (`politicas-ia.md`) | Sí | Captura 08; C08/C10/C17; `.gitignore` y políticas documentadas |
| Pruebas con % de confianza (C3) | Sí | Captura 09 histórica (31/31); suite/reporte actual y `docs/pruebas-ssh.md`: 84/84 ejecutadas |
| Documento y manual finales | Sí | Informe PDF revisado, capturas insertadas y manual de controles/idioma |
| Repositorio y versiones | Sí | Repositorio público, ramas e historial; capturas 05 y 10 |
| Sustentación en vivo realizada | No | Debe demostrarse ante evaluación; esta entrega no la simula |

Límites: propuestas IPv4 revisadas como texto; IPv6 de cálculo/planificación, sin DHCPv6/SLAAC avanzado/NAT66 ni políticas IPv6. Pools DHCP y reservas editables, y validación física quedan fuera de esta entrega. La revisión a 1440/390 px no certifica todos los dispositivos o anchos.
