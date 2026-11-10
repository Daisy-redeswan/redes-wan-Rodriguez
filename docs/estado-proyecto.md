# Estado de WAN Architect

## Estado vigente de esta entrega

Repositorio: [Daisy-redeswan/redes-wan-Rodriguez](https://github.com/Daisy-redeswan/redes-wan-Rodriguez). Base main: `6ac46f9257143f88ec8cb7b47c020bb3739adbfa`. Rama: `feature/i18n-evidencias-finales`; código bilingüe: `71d56cb469a1f9049d24fc0bf2804adefdd256db`. Auditoría: 9 de noviembre de 2026, America/Bogota. Estudiante: Daisy Jurleny Rodriguez · Fundación Universitaria Compensar.

Objetivo: apoyar el diseño WAN académico por sedes mediante requisitos, inventario, VLAN, direccionamiento, topología, propuestas por fabricante y evidencia reproducible. Genera texto; no ejecuta configuraciones.

## Arquitectura y contrato actuales

`WAN_v4.html` contiene HTML/CSS/JavaScript, estado central y renderizado de vistas, sin backend ni credenciales. Flujo: proyecto → sedes → estimación → VLAN → plan IPv4 / plan IPv6 separado → topología → generadores IPv4 → exportación/persistencia y evidencias.

- **V4:** `project.base`/`transitBase`/`ipv6Base`; `sites[].ipv4Base`/`ipv6Base`; `vlans[].ipv4Cidr`; `plan` IPv4 e `ipv6Plan` por claves VLAN; nodos, enlaces, opciones y configuraciones derivadas.
- **Migración:** v2→v3→v4 sin asignar redes durante la carga. Importador reconstruye/valida el contrato y conserva CLI coherentes con su regeneración.
- **Persistencia:** `WAN-Architect-v4`, fallback no destructivo v3/v2; JSON v4. Cadenas para IPv6, BigInt solo en memoria.
- **I18N:** catálogo `I18N`, `t()` y `setLanguage()` en la misma aplicación. Español inicial; clave independiente `WAN-Architect-language`. No cambia el esquema ni traduce datos/CLI.
- **Adaptadores:** Cisco IOS/IOS XE, Huawei VRP, Fortinet FortiOS y MikroTik RouterOS separados, con el mismo plan/topología/interfaces como entrada.

## Implementado e inspeccionado

IPv4: cálculo público/privado, VLSM global y por bloques de sede, tránsito /30, CIDR manual opcional por VLAN, asignación mixta, capacidad/crecimiento/reservas, contención, alineación y solapamientos. Gateway independiente de la subred y del DHCP. Las redes manuales se reservan y no se mueven silenciosamente.

IPv6: calculadora comprimida/expandida/canónica y clasificación; planificación ULA /48 de proyecto → /56 de sede → /64 de VLAN, router completo +1; redundancia virtual +1 y físicas +2/+3. Sin broadcast, tránsitos IPv6 ni comandos IPv6 por fabricante.

Topología: generación, edición de equipos/enlaces, roles y puertos por fabricante, access/trunk/routed y controles de coherencia; imagen como referencia manual, sin OCR. CLI separadas con administración restringida, DHCP/relay y enrutamiento según rol/opciones. FortiOS 7.4 genérico sin multi-VDOM; RouterOS 7.x genérico sin VRF/CAPsMAN. No se asumen NAT/Internet/permisos de tránsito.

Interfaz bilingüe: vistas, ayudas, botones, atributos accesibles, validaciones, confirmaciones y descargas de interfaz. Nombres del usuario, JSON, claves, hostnames, interfaces y CLI permanecen iguales. Se conservaron 58 plantillas de botón, dos importadores y un selector: todos tenían función real; 0 eliminados. La disponibilidad de Vista automática y los mensajes de copia/descarga sin configuración se ajustaron; importadores y controles tienen acceso por teclado.

## Confirmado mediante pruebas ejecutadas

[Suite y resultados](pruebas.md): **C01–C31, 31/31 = 100% del conjunto ejecutado**, 0 fallidas, bloqueadas o no ejecutadas. Se ejecutó en HTTP local, contextos limpios y datos ficticios con Python/Playwright/Chromium. Los 20 casos originales siguen incluidos; no se sumaron matrices históricas.

C26 compara referencias calculadas desde el main base: plan IPv4, topología y plan IPv6 exactos, y ocho comparaciones CLI (cuatro fabricantes × ES/EN). C28 activó 54 familias/objetivos con Enter; C29 comprueba portapapeles real, descarga, fallback e importadores por teclado. C30 cubre 52 combinaciones de vistas/idioma/ancho a 1440/390 px; no certifica todo ancho. El manifiesto de 58 plantillas está en [manual.md](manual.md).

Las diez capturas se revisaron; 01–04 corrigen la calculadora/diagrama completo y VLAN/IP de cores, 05 muestra GitHub real y 06–10 corresponden a generación, rechazo, pruebas y app actual. GitHub devolvió HTTPS 200; sus estilos/avatares externos quedaron bloqueados, por lo que 05 conserva render nativo sin reconstrucción. PDF, README y entregables actualizados; detalles de maquetación, páginas y hashes en [pruebas.md](pruebas.md).

## Dependencias e invalidación

Confirmar fichas de sede mantiene la invalidación histórica de VLAN y derivados de `saveSite()`. VLAN/plan condicionan gateways, topología y configuraciones; modificar gateway obliga a regenerar derivados. Una eliminación conserva ediciones válidas de otras VLAN antes de invalidar lo previsto. Confirmar IPv6 no sustituye IPv4 ni sus CLI. Cambiar idioma solo reconstruye presentación y restaura los campos pendientes; no confirma ni invalida el proyecto.

La importación no asigna nuevas redes; normaliza el contrato existente. El indicador transitorio `subnetOK` no pertenece al contrato reconstruido por el importador heredado; el roundtrip de teclado compara un proyecto ya canonicalizado. No se amplió ese comportamiento en esta tarea.

## Límites, riesgos y pendientes

- Ninguna propuesta se ejecutó: no hay validación física, conectividad, convergencia, compatibilidad de firmware/modelos ni auditoría exhaustiva de seguridad.
- Los cuatro generadores permanecen IPv4; el alcance de configuraciones IPv6 requiere aclaración académica. IPv6 es cálculo/planificación ULA.
- Pools DHCP y reservas editables, revisión de `saveSite()` y cobertura completa de accesibilidad/navegadores/datos masivos quedan para trabajos separados.
- La auditoría 1440/390 px y los controles deshabilitados no certifican cada combinación de datos ni eliminan todos los riesgos históricos de interfaz.
- La sustentación en vivo no se ha realizado en esta entrega. La autoevaluación de README usa evidencia local y no asigna una calificación.

## Fuentes y antecedentes

Prevalece [Guía Docente.html](<requisitos/Guía Docente.html>). [Trazabilidad](trazabilidad-corte3.md) conserva los pesos oficiales; [matriz de fabricantes](matriz-fabricantes.md) documenta objetivos y límites. Los resultados históricos M/S/A/C/V y etapas previas se conservan en el [historial de este documento en la base](https://github.com/Daisy-redeswan/redes-wan-Rodriguez/blob/6ac46f9257143f88ec8cb7b47c020bb3739adbfa/docs/estado-proyecto.md); no se vuelven a presentar como ejecuciones actuales.

Siguiente etapa recomendada: revisar el PR, contrastar la entrega con la rúbrica y sustentar el funcionamiento y sus límites. Una prueba textual no autoriza aplicar CLI a equipos.
