# Pruebas del PR #10: interfaces automáticas, AP y menú

## Resultado, entorno y procedencia

- Rama `fix/revision-integral-wan-architect`; base `9675ce7f1c553e1225609772cbb6a500822fa2f0`; main intacto `1956d1872363c88399f5e8240abb1d7a13bca340`.
- Ejecución **2026-11-11T13:02:18-05:00**, Linux, Python 3.12.14, Playwright 1.62.0 y Chromium 154.0.8037.57, HTTP loopback y contexto limpio por caso.
- **73/73 aplicación**, aproximadamente 80 s: C01–C31, N01–N19, P01–P08 y Q01–Q15. **26/26 SSH local**, 10.754 s, AsyncSSH 2.24.1/aiohttp 3.14.5, con servicio y runner SSH sin cambios.
- **99 superadas / 99 ejecutadas × 100 = 100%**. Fallidas, bloqueadas y no ejecutadas dentro de ambas matrices: 0. No es porcentaje de certificación ni cobertura absoluta.
- HTML SHA-256: `a5b13cfbeae69b8588ce18a7735925aa919b2a5d1dfc5c199941416fff04bbaf`.
- Runner UI SHA-256: `a70494d3575af149b058465b2c17c2fba259146aab73b3f79a8112de8c716301`.
- [Reporte real de 73 casos](../tests/reporte-interfaces.html), con esperado/obtenido/estado y tiempo. El Commit del reporte es el HEAD anterior a los commits de este ajuste; sus hashes identifican el código y suite ejecutados, no el blob base sin modificar.
- La repetición SSH de esta tarea imprimió `Ran 26 tests`, `OK` y `26/26 = 100.00%`. [Matriz SSH y procedimiento](pruebas-ssh.md); el reporte enlazado allí sigue siendo histórico y no se atribuye a esta nueva ejecución.

## Reproducir

```bash
python tests/test_corte3.py
python tests/test_corte3.py --report tests/reporte-interfaces.html
```

Para SSH, en el entorno opcional descrito en el [manual SSH](manual-ssh.md):

```bash
python tests/test_ssh_service.py
```

No se añadieron dependencias. Ambos runners finalizan sus servidores/contextos y devuelven código no cero si falla un caso. Los comandos de fabricantes se inspeccionan como texto; no se ejecutan.

## Casos afectados y evidencia observable

Todos están **superados** en el reporte actual:

| Casos | Esperado | Obtenido |
| --- | --- | --- |
| Q01/Q02/Q14 | Mantener aprobación efectiva y navegación protegida | Borradores/planes incoherentes bloquean Topología/fabricantes/Comparación; revertir reconoce aprobación; calculadora, seguridad, IPv6 y SSH manual siguen accesibles |
| Q03 | Conservar AP sin CLI genérica | Seis AP mantienen VLAN, IP, máscara, gateway, enlaces y JSON; listas y llamadas directas de cuatro adaptadores los excluyen |
| Q04 | No exigir confirmación física | Generación Cisco por botón y API sin perfil; modal/funciones del formulario ausentes; archivo v2 con cuatro textos conservado |
| Q05–Q08 | Cuatro generadores automáticos | Cisco/Huawei usan tres puertos y Fortinet/MikroTik dos en sus laboratorios; nombres coinciden exactamente con los enlaces; sin perfiles ni requisitos nuevos |
| Q09 | Mantener seguridad de nombres | Cuatro entradas maliciosas en puertos Cisco/Huawei/Fortinet/MikroTik rechazadas atómicamente por el editor de enlaces |
| Q10 | JSON y persistencia compatibles | v4 previo con perfiles y CLI histórica conservado; regeneración automática e ida/vuelta exacta; localStorage exacto; v2/v3 sin nuevas asignaciones |
| Q11 | Editar/eliminar enlaces sin reconfirmación física | Nuevo puerto usado directamente; eliminación mantiene JSON coherente y permite regenerar; sin modal adicional |
| Q12 | Comparación sin perfiles | IOS/VRP automáticos con sintaxis y nombres separados; marca real intacta |
| Q13 | Avisos visuales ES/EN y responsive | Dieciséis combinaciones de cuatro vistas/idiomas/anchos 1440 y 390; sin formulario ni desbordamiento nuevo; advertencia y Cancelar por teclado |
| Q15 | Nuevo orden de módulos | Cisco/Huawei/Fortinet/MikroTik/Comparación/Ciberdefensa en ES/EN; Enter, flechas, numeración y catorce indicadores correctos; sin cambiar estado |

## Regresiones y cambios deliberados de pruebas

Se conservan todos los identificadores C/N/P y los 26 casos SSH. Los ocho hashes CLI históricos (cuatro fabricantes × ES/EN) siguen idénticos, sin modificar referencias para ocultar regresiones. Migraciones, localStorage, IPv4 independiente/mixto, IPv6, topología mixta, controles, descargas, portapapeles, idioma, seguridad y SSH pasan.

Se elimina el helper que añadía perfiles antes de generar: los laboratorios normales prueban ahora el flujo automático sin preparar confirmaciones. Un helper de metadatos archivados se usa solo en Q10 para reproducir un v4 anterior válido; no habilita la CLI normal. Q04–Q13 reemplazan expectativas del formulario eliminado por los requisitos vigentes; no se omiten como casos fallidos. Q15 es nuevo. Los índices de Comparación, Ciberdefensa, Fortinet y MikroTik se actualizan también en las pruebas antiguas, sin alterar direcciones, algoritmos ni valores de referencia. La materialización histórica de `subnetOK=false` al importar sigue contemplada, sin modificar producción.

## Límites

Las propuestas usan los puertos del enlace de cada marca y muestran advertencias de revisar hardware antes de aplicarlas. No se certifican modelo, firmware, puerto físico, conectividad WAN/RF ni AP específico; no se realizaron pruebas físicas ni en Windows. Las fuentes oficiales previas siguen en la [matriz](matriz-fabricantes.md); no se amplió soporte ni se inventaron comandos. Los perfiles antiguos se validan por seguridad como datos archivados y no dirigen la generación nueva.

La comprobación histórica `file://` permanece bloqueada por política del Chromium administrado y no se contabiliza como éxito. El frontend/simulación por HTTP estático sigue probado. SSH real se prueba exclusivamente en loopback con credenciales efímeras, sin aplicar CLI. Los PDF/capturas académicos, AGENTS.md, backend y fixtures quedan intactos.
