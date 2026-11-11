# Pruebas adicionales del PR #10: navegación, AP e interfaces

## Fuentes, versión y resultado real

- Rama: `fix/revision-integral-wan-architect`; base de trabajo `ce1873ccf41691474dead928c7b55c561ce7ad58`; main `1956d1872363c88399f5e8240abb1d7a13bca340`.
- Ejecución UI: **2026-11-11T12:25:40-05:00**, Python 3.12.14, Playwright 1.62.0, Chromium 154.0.8037.57, Linux; HTTP loopback y contexto limpio por caso. Aproximadamente 85 s.
- **72/72 UI superadas**: C01–C31, N01–N19, P01–P08 y Q01–Q14. **26/26 SSH local superadas**, aproximadamente 11 s, con el servicio y runner SSH sin cambios, AsyncSSH 2.24.1/aiohttp 3.14.5. Incluye el navegador con el HTML actual.
- **98 superadas / 98 ejecutadas × 100 = 100%**. Fallidas: 0; bloqueadas/no ejecutadas dentro de ambas matrices: 0. No equivale a cobertura total ni porcentaje de compatibilidad física.
- SHA-256 del HTML probado: `b89a27a766f86fd3928ed444641957544dee5cc7f9e7b2653c07e5f94ddf2fab`.
- SHA-256 del runner UI probado: `10037ed0b0d2fa9c1554f40ba31e15e84f67f8b3c9f78e903778e03443f7649c`.
- [Reporte real de 72 casos](../tests/reporte-interfaces.html), con esperado/obtenido/estado/tiempo y hashes. El campo Commit identifica el HEAD antes de los commits de esta tarea; los hashes identifican exactamente los archivos modificados ejecutados. El reporte no atribuye los cambios al blob base.

El servicio SSH conserva sus [26 casos documentados](pruebas-ssh.md) y [reporte histórico](../tests/reporte-ssh-servicio.json); su repetición de esta tarea terminó con `Ran 26 tests`, `OK`, `26/26 = 100.00%`, en 10.587 s. No se suman las ejecuciones históricas. No se ejecutó ninguna configuración ni se conectaron equipos reales de fabricante.

## Reproducción

```bash
python tests/test_corte3.py
```

Opcional para conservar evidencia nueva:

```bash
python tests/test_corte3.py --report tests/reporte-interfaces.html
```

Para el servicio SSH, activar el entorno virtual y las dependencias separadas según el [manual SSH](manual-ssh.md); después:

```bash
python tests/test_ssh_service.py
```

Ambos runners devuelven código distinto de cero ante fallos. La suite UI inicia/cierra HTTP y usa contexto nuevo por caso. Los perfiles de pruebas se declaran explícitamente como **LAB-FICTICIO / LAB-no-fisica** o **LABORATORIO-DECLARADO**, con puertos deterministas y fuentes oficiales; no son inventarios físicos certificados. No se añadieron dependencias.

## Casos nuevos: esperado y evidencia obtenida

Todos los casos siguientes están **superados** en el reporte; cada uno corre en un contexto limpio.

| Caso | Esperado | Obtenido observable |
| --- | --- | --- |
| Q01 | Bloquear módulos dependientes por todas las rutas | Seis destinos bloqueados por menú y `go`; Siguiente y `render` protegidos; cuatro módulos independientes accesibles; estado intacto |
| Q02 | Reconocer aprobación válida y bloquear borradores | Bandera antigua no bloquea; cambio pendiente conserva el mismo DOM; salto directo tampoco lo reconstruye; revertir/cargar reconoce la aprobación |
| Q03 | Conservar AP sin CLI genérica | Seis AP con VLAN/IP/máscara/gateway/enlaces; ninguna lista/adaptador ni llamada directa genera CLI; JSON conserva datos |
| Q04 | No certificar propuestas antiguas | Botón y llamada directa bloqueados sin perfil; v2 carga cuatro textos archivados sin inventar perfiles |
| Q05 | Cisco usa interfaces declaradas | Tres nombres TenGigabitEthernet introducidos por formulario coinciden exactamente con CLI y `endpoint` |
| Q06 | Huawei usa interfaces declaradas | Tres nombres XGigabitEthernet coinciden con CLI y `endpoint` |
| Q07 | Fortinet usa interfaces declaradas | Dos nombres físicos declarados `lanLab...` coinciden con CLI y enlaces |
| Q08 | MikroTik usa interfaces declaradas | Dos nombres físicos declarados `sfp-sfpplus...` coinciden con CLI y enlaces |
| Q09 | Rechazar errores físicos atómicamente | Duplicado, inyección, modelo vacío, función incoherente y dominio engañoso rechazados; DOM/estado/CLI/localStorage intactos |
| Q10 | Persistir perfiles y validar importación | JSON/localStorage exactos, salvo materialización previa de `subnetOK=false`; siete perfiles malformados rechazados; v2/v3 sin llamadas al asignador ni certificación implícita |
| Q11 | Reconfirmar cambios de enlaces | Editar/eliminar retira confirmación afectada, conserva perfiles editables y elimina referencias huérfanas; JSON válido |
| Q12 | Comparar con perfiles separados | Sin perfil Huawei no genera ambas salidas; al declararlo produce IOS/VRP sin cambiar marca real ni mezclar interfaces |
| Q13 | Editor bilingüe, teclado y responsive | 1440/390 px sin desbordamiento nuevo; guardar inválido/cancelar con Enter; modelo/versión/controles EN, estado intacto; capturas temporales inspeccionadas |
| Q14 | Rechazar aprobación incoherente | Red ausente, hosts desactualizados, números de red incoherentes y pool incompatible bloquean Topología sin mutar datos |

## Conservación de las 84 pruebas anteriores

No se eliminó ni se omitió ningún caso C/N/P o SSH. Los laboratorios de generación ahora declaran perfiles ficticios antes de pedir CLI. C26 conserva **los mismos ocho hashes de referencia** (cuatro fabricantes × ES/EN), sin modificar fixtures ni actualizar referencias para ocultar regresiones. C03–C05 conservan planes/topología/CLI de importaciones antiguas sin reasignación. Direccionamiento IPv4 independiente/mixto, IPv6, idioma, descargas, portapapeles, topología y SSH siguen en regresión.

C27, N07, P03 y P08 esperan ahora rechazo **al navegar**, además de las defensas al generar: no esperan poder abrir una vista dependiente inválida. N15 compara todos los atributos de equipos/redes no afectados y sus CLI; el vecino WAN afectado debe retirar confirmación física si perdió un enlace, mientras otros perfiles siguen idénticos. Se conserva la normalización histórica que materializa `subnetOK=false` al importar un proyecto sin esa propiedad; no se cambió producción para ocultarla.

## Inspección y límites

`node --check`, compilación JavaScript en Chromium y consola/página en los 72 casos, sintaxis Python, revisión HTML, `git diff --check`, enlaces locales y patrones de secretos/temporales se revisaron. Se inspeccionaron capturas reales temporales del editor a 1440/390; no se sustituyeron evidencias académicas. El código nuevo contiene comentarios en español; fuentes oficiales y límites por marca en la [matriz](matriz-fabricantes.md).

**No ejecutado físicamente:** modelos, firmware, inventario de puertos, conectividad WAN/RF, Windows y configuración de AP específicos. Las restricciones léxicas evitan comandos inseguros, pero no demuestran que exista un puerto. La URL debe ser oficial; la app no inspecciona su contenido ni consulta hardware. Fortinet devolvió HTTP 403 al abrir el artículo completo: se consultó su índice oficial, sin atribuirle una lectura completa. Nomenclaturas fuera del adaptador se rechazan en lugar de inventarlas.

La comprobación exploratoria histórica `file://` permanece bloqueada por política del navegador administrado; no se repitió ni se contabilizó como éxito. El uso autónomo por HTTP estático/simulación conserva sus pruebas. La consola SSH opcional solo se conectó al servidor de laboratorio loopback, sin ejecutar CLI de fabricantes. IPv6 sigue siendo planificación separada; no se ampliaron sus generadores.
