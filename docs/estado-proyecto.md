# Estado de WAN Architect

## Laboratorio e inventario físico vigentes

Base `09279698084fa166b937ae7d5450fedf4827017e`; rama del PR #11. El botón público construye un laboratorio completo mediante validaciones reales, con LAN `192.168.32.0/21` y `172.16.64.0/21`, tránsito `10.250.0.0/24` y DNS privado obtenido del servidor del plan. Selecciona modelos compatibles del catálogo existente: C9200L-24T-4G, S5700-28P-LI-AC, FortiGate 60F y RB750Gr3. Resultado: 21 redes, 42 nodos, 48 enlaces, 16 CLI nativas y AP conservados sin CLI genérica.

Los cuatro módulos muestran tabla de interfaces agrupada por dispositivo, con marca/modelo, puerto, función y vecino reales; las configuraciones permanecen debajo. Proyectos sin modelo se identifican como Modo genérico. Datos detallados/capacidad: [manual](manual.md); funciones: [documentación del código](documentacion-codigo.md); evidencia real y límites: [pruebas](pruebas.md). **Prueba vigente:** 114/114 aplicación + 26/26 SSH = 140/140, 100% del conjunto ejecutado; L01 recorre quince pasos y L02–L05 cubren tabla ES/EN, rollback, compatibilidad y determinismo. Verificación estática/local, sin certificar equipos físicos. Los apartados siguientes son antecedentes, no sustituyen la ejecución actual.

## Correcciones funcionales vigentes del PR #11

Base `89a5a2a948c965129ca28f40cb57f5f303f587b2`. Datos del proyecto y fabricantes muestran confirmación persistida/Editar; confirmar igualdad no destruye diseños. Cambiar solo una marca conserva VLAN/VLSM/IPv6 y retira CLI dependientes; nuevas funciones agregan únicamente /30 necesarias sin mover redes previas. El catálogo de doce fichas está embebido en el HTML y se selecciona exclusivamente en Topología. Las cuatro vistas CLI muestran datos guardados, sin selectores repetidos.

Comparación incorpora cinco funciones × cuatro marcas reales, con extractos y límites; conserva adicionalmente IOS/VRP cuando corresponde. La simulación normaliza comandos de lectura de cada marca, muestra propuestas/plan y abre un manual integrado sin Python. SSH real, exclusión CLI de AP y JSON v2/v3/v4 se conservan. Detalle operativo: [manual](manual.md); contrato: [documentación del código](documentacion-codigo.md); resultados reales y limitación file://: [pruebas](pruebas.md). **Prueba vigente:** 109/109 aplicación + 26/26 SSH = 135/135 ejecutadas, 100%; FILE01 adicional bloqueada por política del navegador, sin certificar apertura file://. Doce modelos y 19 comandos de lectura comprobados mediante HTTP; revisión visual 1440/390 px. Los registros siguientes son históricos.

## Registro anterior: primera versión del catálogo local

Base `6466c9494cefdb5423d95e1bc04175304a4e248d`, rama `feature/catalogo-interfaces-fabricantes`. Verificación documental y pruebas: **14 de noviembre de 2026**. Se incorporan doce fichas, tres por fabricante, contrastadas con fuentes oficiales y límites explícitos en [catálogo de modelos](catalogo-modelos.md). No es certificación física.

**Implementado:** selección fabricante/modelo filtrada por tipo en el editor normal y selección de modelo en Topología/configuración; inventario local, asignación determinista de puertos por enlace/medio/velocidad, conservación de nombres válidos, bloqueo de capacidad/roles/funciones incompatibles y validación de importaciones. No se pide escribir interfaces, versión ni URL. Los cuatro adaptadores leen nombres reales de los enlaces para el modelo elegido. Huawei LI incluye solo banco RJ45 verificado; Fortinet reserva switch interno y FortiLink. No hay consultas de red durante uso normal.

**Confirmado por pruebas:** 73 casos anteriores + 23 casos K01–K23 = **96/96 aplicación**; **26/26 SSH local**, total **122/122 = 100%** del conjunto ejecutado, 0 fallidas/bloqueadas/no ejecutadas dentro de las matrices. Reportes reales: [aplicación](../tests/reporte-catalogo.html) y [SSH](../tests/reporte-catalogo-ssh.json). Se conservan las ocho comparaciones exactas de CLI (cuatro marcas × ES/EN) para proyectos sin modelo, los 99 casos previos, IPv4/IPv6, JSON v2/v3/v4 y exclusión CLI de AP. Datos ficticios, contextos limpios, HTTP local y SSH real exclusivamente loopback; no se aplica CLI.

**Persistencia:** `nodes[].modelId` es una extensión opcional de v4; ausencia conserva comportamiento genérico y aviso de modelo no especificado. Las interfaces permanecen en campos de enlaces existentes. La carga valida sin reasignar; no cambia versión, migración, claves locales, planes, IP ni configuración SSH. La ruta fija del servicio SSH opcional sirve solo el script local del catálogo.

**Pendiente/límites:** comprobar equipos reales, firmware/licencias, transceptores, puertos renombrados y configuración previa. SFP Huawei excluidos hasta completar nomenclatura por variante. No se amplían los adaptadores a roles/funciones no respaldados, IPv6 CLI ni pools/reservas editables. Revisión visual 1440/390 px satisfactoria; `file://` fue bloqueado por política del navegador del entorno y se declara como una exploración bloqueada aparte, no como caso superado. El modo sin internet se verificó mediante HTTP local con la red del contexto desactivada. Los apartados siguientes conservan evidencia histórica, no sustituyen este resultado.

## Registro anterior del PR #10: interfaces automáticas y orden del menú

Base de trabajo `9675ce7f1c553e1225609772cbb6a500822fa2f0`; main conservado en `1956d1872363c88399f5e8240abb1d7a13bca340`. Ejecución 2026-11-11T13:02:18-05:00: **73/73 aplicación + 26/26 SSH local = 99/99 (100%)**, 0 fallidas/bloqueadas/no ejecutadas dentro de las matrices. Se mantienen los 58 casos C/N/P y los 26 SSH; Q04–Q13 cambian sus expectativas porque se retiró expresamente el formulario físico, y Q15 verifica el nuevo menú. No se alteraron fixtures ni hashes CLI de referencia. [Resultados y límites](pruebas-interfaces.md), [reporte real](../tests/reporte-interfaces.html).

Se elimina la confirmación manual de interfaces: los cuatro adaptadores vuelven a tomar puertos automáticamente de los enlaces, sin pedir modelo/versión/URL/perfil. El aviso de revisar hardware es visual. AP conserva inventario, topología y administración, excluido de CLI genérica. El menú agrupa Cisco → Huawei → Fortinet → MikroTik → Comparación → Ciberdefensa; permanecen las demás vistas, ES/EN, flechas y progreso. La confirmación del plan VLAN/VLSM, fabricantes mixtos, IPv4/IPv6, JSON v2/v3/v4 y SSH se conservan. Los perfiles v4 antiguos permanecen como metadatos/CLI archivada, sin controlar propuestas nuevas ni exigir confirmaciones.

## Registro anterior: confirmaciones y consola SSH (84 casos)

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
