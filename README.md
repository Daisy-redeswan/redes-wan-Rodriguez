# WAN Architect — Corte 3

Herramienta académica local para diseñar redes WAN por sedes, planificar IPv4/IPv6 y generar **propuestas IPv4** separadas para Cisco IOS/IOS XE, Huawei VRP, Fortinet FortiOS y MikroTik RouterOS. No aplica configuraciones a equipos.

- **Autora:** Daisy Jurleny Rodriguez Rodriguez, según el informe del Corte 2.
- **Materia:** Interconexión de Redes WAN · Ingeniería de Telecomunicaciones.
- **Repositorio:** [Daisy-redeswan/redes-wan-Rodriguez](https://github.com/Daisy-redeswan/redes-wan-Rodriguez).
- **Institución, docente y grupo:** pendientes de confirmar; no se inventan datos académicos.
- **Base técnica de esta entrega:** `f7ed2b907d6edad6f1ed7bd5274c49956a7a77d8`; esquema de proyecto **v4**.

## Abrir la aplicación

El archivo real de entrada es [WAN_v4.html](WAN_v4.html). Puede abrirse directamente en un navegador actualizado; no requiere backend, cuenta ni dependencias de ejecución. Para reproducir las pruebas y capturas se recomienda HTTP local:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:8000/WAN_v4.html`. Detener el servidor con Ctrl+C. No exponer la carpeta a una red pública. Las referencias técnicas enlazadas requieren Internet, pero el funcionamiento principal de la app es local. El almacenamiento del navegador depende del origen; conservar además una exportación JSON.

## Funciones y alcance confirmado

- Proyecto, fichas por sede, estimación de inventario y VLAN con claves estables.
- IPv4: bloque global, bloques opcionales por sede/tránsito, VLSM automático y CIDR manual opcional por VLAN; gateway independiente y validación de capacidad/solapamientos.
- IPv6: calculadora y planificación ULA separada; /48 propuesto, /56 por sede y /64 por VLAN, reservas según redundancia. Sin broadcast, tránsitos ni comandos IPv6.
- Topología automática/manual y mapeo de interfaces; una imagen importada es **referencia manual**, no OCR ni reconocimiento automático.
- Cuatro generadores separados desde el mismo plan/topología. Huawei ofrece equivalencias cuando no hay nodos Huawei; esto no certifica hardware equivalente.
- Fortinet: supuesto FortiGate genérico/FortiOS 7.4 sin multi-VDOM; MikroTik: RouterOS 7.x genérico sin VRF/CAPsMAN. Ambos requieren puertos propios y roles compatibles.
- JSON v4, migración v2→v3→v4 sin reasignar, localStorage v4 con fallback no destructivo v3/v2 y exportaciones de texto/SVG.
- Validación, escape de contenido, marcadores de secretos y advertencias de ciberdefensa. No equivale a auditoría completa ni validación física.

## Flujo de uso

Proyecto → fichas de sede → estimación → propuesta/confirmación de VLAN → IPv4/VLSM → cálculo/planificación IPv6 opcional → topología → fabricante → revisión de propuestas → guardado/exportación. El [manual](docs/manual.md) explica los pasos y los escenarios compatibles para cada marca.

**Importante:** confirmar una sede mantiene la invalidación histórica de VLAN y derivados. Revisar las fichas antes de avanzar. Las ediciones visibles de un formulario todavía no son datos confirmados; una validación fallida conserva el texto. Los cuatro generadores siguen siendo IPv4 hasta aclaración docente sobre configuraciones IPv6.

## Pruebas reproducibles

Python 3.10+, Playwright 1.62.0 y Chromium; dependencias solo para pruebas:

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/test_corte3.py
```

El runner inicia/cierra HTTP local, usa un contexto limpio por caso, imprime resultados y devuelve un código no cero ante fallos. La ejecución normal guarda el reporte fuera del repositorio. [Instalación, casos, resultados y sustentación](docs/pruebas.md).

**Resultado registrado:** 20/20 superadas = **100% del conjunto ejecutado**, 0 fallidas, bloqueadas o no ejecutadas; ratificado sobre el main indicado durante esta entrega. Validación de navegador y texto, sin ejecutar CLI ni certificar conectividad, modelos o firmware.

## Entregables y evidencias del Corte 3

| Evidencia | Qué demuestra | Archivo |
| --- | --- | --- |
| 06 | Propuesta Fortinet realmente generada en la aplicación | [06-config-fortinet.png](docs/capturas/06-config-fortinet.png) |
| 07 | Propuesta MikroTik realmente generada en la aplicación | [07-config-mikrotik.png](docs/capturas/07-config-mikrotik.png) |
| 08 | Rechazo real de una IPv4 inválida, conservando el resultado anterior | [08-ciberdefensa.png](docs/capturas/08-ciberdefensa.png) |
| 09 | Suite ejecutada, 20 casos y 20/20 = 100%; evidencia conservada íntegra | [09-pruebas.png](docs/capturas/09-pruebas.png) |
| 10 | Pantalla principal del laboratorio funcionando | [10-app-final.png](docs/capturas/10-app-final.png) |

- [Informe académico Corte 3](docs/informe-corte3.pdf).
- [Manual de usuario](docs/manual.md).
- [Medidas y límites de seguridad](docs/seguridad.md).
- [Políticas de ciberdefensa y uso de IA](docs/politicas-ia.md).
- [Pruebas, entorno y evidencia real](docs/pruebas.md) y [reporte HTML](tests/reporte-corte3.html).
- Orientación técnica: [estado](docs/estado-proyecto.md), [trazabilidad](docs/trazabilidad-corte3.md) y [matriz de fabricantes](docs/matriz-fabricantes.md). Sus registros históricos deben leerse junto con esta entrega documental.
- Se conservan sin cambios el [informe Corte 2](docs/informe-corte2.pdf) y las capturas anteriores. No se inventó la captura 05 ausente.

## Límites y pendientes

No hay certificación de compatibilidad física, aplicación automática de CLI, pruebas de conectividad, convergencia ni auditoría integral de seguridad. Las políticas entre servicios requieren intención explícita: MikroTik bloquea forward por defecto; Fortinet no inventa permisos ni NAT. No se asume Internet, VPN ni interoperabilidad HSRP/VRRP.

Pendientes: aclaración docente de configuraciones IPv6, pools DHCP/reservas editables, corrección de `saveSite()`, desbordamientos históricos ajenos a los flujos verificados, validación de plataforma, datos académicos faltantes y sustentación en vivo. La entrega documental no adjudica una nota ni declara completado todo requisito del curso.
