# Estado de WAN Architect

## Actualización: confirmaciones y consola SSH

Código sobre el HEAD de referencia PR #10 `194a43e`; véanse [manual SSH](manual-ssh.md), [servicio opcional](../ssh_service/README.md) y [pruebas actuales](pruebas-ssh.md). **58/58 UI + 26/26 SSH local = 84/84 ejecutadas**; una comprobación exploratoria file:// bloqueada por política se declara aparte. Windows y fabricantes físicos no ejecutados.

Sedes: confirmed opcional v4 validado, resumen verde/Editar y protección contra cambios accidentales; ausencia en proyectos antiguos no se interpreta como confirmación. Se conserva invalidación selectiva. VLAN: previsualización pendiente/efectiva por sede, mensajes de capacidad y aprobación efectiva; errores preservan estado y formulario.

Consola SSH: módulo 14 con simulación autónoma de comandos cerrados y conexión real opcional HTTP/WS→AsyncSSH con PTY/xterm local. La conexión manual es independiente de VLSM. Origen/Host, autorización local, allowlist, claves de host, timeouts, cuotas, buffers/ACK y limpieza de sesiones verificados. Credenciales/historial real nunca entran en JSON o localStorage. No se envían configuraciones automáticamente.

**El contenido restante conserva el registro de la revisión anterior de 50 casos; no es el resultado actual ni se suma dos veces.**

## Versión y alcance de la revisión anterior

Repositorio: [Daisy-redeswan/redes-wan-Rodriguez](https://github.com/Daisy-redeswan/redes-wan-Rodriguez). Base main `1956d1872363c88399f5e8240abb1d7a13bca340`. Rama `fix/revision-integral-wan-architect`; código probado `8a27f672e03b6e777b077a8910915d13adeb7127`. Fecha de ejecución: 2026-11-09T23:32:21-05:00 (America/Bogota).

Implementación autónoma en `WAN_v4.html`: HTML/CSS/JavaScript/SVG, sin backend, servicios obligatorios ni ejecución de comandos. Flujo: proyecto → sedes → inventario → VLAN/IPv4 y planificación IPv6 separada → fabricantes por función → topología → cuatro adaptadores IPv4 → persistencia y exportación. Español predeterminado y English conservados.

## Nueve correcciones implementadas e inspeccionadas

| Corrección | Implementación | Evidencia actual |
| --- | --- | --- |
| 01 · IPv4 independiente por sede | Fallback del proyecto, bloques privados propios y tránsito independiente, sin exigir contención de sede en global; validación RFC1918/alineación/solapamientos | N01/N02/N03/N14/N18 |
| 02 · Inventario confirmado | Formulario inicial, resumen confirmado, editar/restaurar con cancelación, borradores y guardado sin invalidar por igualdad | N04/N05/N06/N17 |
| 03 · VLAN/VLSM por sede | Automáticas y manuales en pool efectivo, reservas/capacidad/huecos, conservación de redes y repropuestas no afectadas | C07/C08; N01/N03/N15/N19 |
| 04 · Retirar explicación VLSM | Componente y traducciones exclusivas retirados; algoritmos y gateway permanecen | N08; C01/C07/C12–C16 |
| 05 · Retirar Interpretación | Solo explicación de calculadora retirada; resultados IPv4/IPv6 completos | N08; C01/C02 |
| 06 · Confirmación efectiva | Pendiente/confirmadas/recalcular, bloqueo de dependencias con borradores, igualdad conserva derivados y errores atómicos | N07; C08/C10 |
| 07 · Topología | Jerarquías, iconos originales, nombres por sede, zoom/scroll, reorganización sin borrar, IDs estables, editores, imagen y SVG | N11/N12/N16; C11/C29/C30 |
| 08 · Retirar Evidencias Corte 2 | Menú/pantalla exclusivos retirados; 13 módulos e índices corregidos; archivos académicos conservados | N08/C22/C27 |
| 09 · Fabricantes mixtos | Perfiles por sede/función y editor individual; elección explícita, roles/puertos validados y selección real por marca, Comparación separada | N09/N10/N11/N13; C12–C16/C26 |

## Modelo, compatibilidad e invalidación

Se mantiene v4 y migración no destructiva v2→v3→v4. Los pools independientes se validan también al importar; no se llama a asignadores durante la carga. `vendorProfile`, `autoKey` y overrides de nombre/fabricante son extensiones opcionales validadas; `Genérico` identifica terminales sin adaptador. Proyectos antiguos sin esos campos no se reclasifican. No se garantiza que un lector antiguo acepte estas extensiones/enum nuevos.

Guardar una ficha o inventario idénticos mantiene datos. Cambios reales invalidan dependencias locales y vecinos WAN afectados; CLI realmente válidas de otras sedes conservan texto y revisión. La repropuesta parcial completa sedes sin VLAN; el reemplazo total sigue siendo explícito. Una sede no puede guardar un nuevo pool incompatible con un CIDR manual ya confirmado.

Los borradores viven en memoria de presentación y sobreviven a navegación/idioma; no se serializan como datos confirmados. Reemplazar el proyecto los limpia. Los equipos manuales se conservan; si una edición deja una IP/enlace incompatible, el generador se bloquea para revisión. No se renumeran intenciones manuales silenciosamente.

## Confirmado mediante pruebas ejecutadas

[Pruebas actuales](pruebas.md) y [reporte real](../tests/reporte-revision-integral.html): **50/50 = 100%**, 0 fallidas, bloqueadas o no ejecutadas. Se conservaron los 31 casos anteriores y se añadieron 19; no se suman repeticiones de desarrollo. Python/Playwright/Chromium, HTTP local, contextos limpios y datos ficticios. C26 mantiene los hashes previos y ocho salidas CLI exactas para un proyecto histórico conservado; no se exige que una topología rediseñada tenga los nombres/posiciones anteriores.

Se revisaron visualmente inventario y topología mixta, English a 390 px; pruebas a 1440/390 px y 140 cajas sin superposición automática. HTML5 estático y 26 vistas dinámicas sin errores de parseo, SVG XML, sintaxis y consola revisados. Estos resultados no certifican accesibilidad completa ni hardware.

## Documentación, pendientes y límites

[Documentación del código](documentacion-codigo.md) explica entradas, salidas, validaciones, efectos, funciones y dependencias. Los comentarios en español se agregan donde son seguros; no se insertan dentro de cadenas CLI ni se reescribe aritmética estable para comentar cada línea.

- Los cuatro fabricantes son propuestas IPv4 verificadas como texto. Continúa pendiente validación física de modelos/firmware, conectividad, convergencia y compatibilidad real.
- Dos cores redundantes con fabricantes diferentes siguen bloqueados; no se equiparan HSRP/VRRP. Fortinet solo Firewall; MikroTik solo Router en los adaptadores actuales.
- IPv6 continúa como cálculo/planificación ULA, sin configuración de fabricantes, DHCPv6 avanzado, NAT66 ni políticas automáticas. Pools DHCP/reservas editables siguen fuera de alcance.
- Los canales e iconos mejoran legibilidad, pero no resuelven todos los cruces posibles; el arrastre manual puede crear superposiciones. Los detalles completos están en tablas/títulos, no en etiquetas masivas.
- Equipos antiguos sin `autoKey` se conservan como entidades no clasificadas al regenerar; no se infiere que puedan borrarse.
- Capturas 01–10 e informes académicos se preservan intactos como entrega histórica de main 1956d18; no se presentan como capturas de esta revisión. La sustentación y validación física no se simulan.

Fuentes: [AGENTS.md](../AGENTS.md), [guía docente](<requisitos/Guía Docente.html>), [trazabilidad](trazabilidad-corte3.md), [matriz](matriz-fabricantes.md), fuentes oficiales ya documentadas en cada adaptador y el código confirmado. Ninguna configuración se aplicó sobre infraestructura.
