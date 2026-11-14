# Documentación del código — revisión integral WAN Architect

## Cómo estudiar esta aplicación

La aplicación sigue siendo un solo archivo autónomo, `WAN_v4.html`. HTML define la estructura; CSS la presentación; JavaScript valida datos, calcula redes, renderiza vistas y genera propuestas de comandos. No hay backend obligatorio. El servicio SSH opcional permite únicamente la administración manual explícita; simulación y módulos tradicionales permanecen autónomos. El botón Generar produce texto para revisión humana: nunca configura equipos.

Base de esta revisión: `1956d1872363c88399f5e8240abb1d7a13bca340`. Lea primero las reglas de [AGENTS.md](../AGENTS.md), el [estado](estado-proyecto.md) y las [pruebas](pruebas.md). Las líneas cambian al documentar: busque el nombre de función, no un número de línea histórico.

```mermaid
flowchart TD
  Proyecto --> Sedes
  Sedes --> Inventario
  Inventario --> VLAN
  VLAN --> Validaciones
  Validaciones --> Pools[Fallback / sede / tránsito]
  Pools --> VLSM
  VLSM --> Confirmacion[Plan confirmado]
  Confirmacion --> Perfiles[Fabricantes por función]
  Perfiles --> Topologia
  Topologia --> Adaptadores[Cisco / Huawei / Fortinet / MikroTik]
  Confirmacion --> IPv6[Plan IPv6 separado]
  Adaptadores --> Propuestas[Texto CLI para revisión]
  Propuestas --> Persistencia[JSON / localStorage]
```

## Catálogo de interfaces: extensión opcional v4 (14 de noviembre de 2026)

El contrato IPv4/IPv6 y sus migraciones no cambian. `nodes[].modelId` opcional identifica una ficha local; ausencia conserva modo genérico. Fuente de datos: `data/catalogo-interfaces.json`; `tools/build_catalogo.py` genera un script de datos estático para HTTP/file://. No se usa internet en tiempo de ejecución. La ruta fija del servidor SSH opcional sirve únicamente ese recurso; no añade directorios ni cambia autenticación/SSH.

- `modelsFor()` filtra fabricante y rol; `validateNodeModel()` rechaza modelos desconocidos/incompatibles y AP.
- `modelOptions()`, `catalogControls()` y `catalogInventory()` muestran selección e inventario escapado, restricciones y fuentes; `previewNodeModel()`/`updateNodeModels()` modifican solo el editor, sin mutar proyecto.
- `catalogPurpose()` deriva prioridad WAN/LAN/uplink/access desde el enlace. `catalogPair()` comprueba medio y velocidad común; el par genérico se considera solo cobre.
- `assignCatalogInterfaces(data)` recibe nodos/enlaces, crea una copia y devuelve enlaces asignados. Reserva asociaciones válidas anteriores, detecta capacidad y modos, ordena por restricciones/ID estable y retrocede por clases equivalentes, con límite de 30.000 pasos. No inventa puertos ni cambia planes.
- `validateCatalogBindings(data)` comprueba nombres incluidos/asignables, modos, duplicados y pareja; importa sin reasignar. `requireCatalogReady()` usa la matriz de capacidades para bloquear funciones activas no respaldadas antes de las plantillas CLI.
- `setNodeModel()` realiza validación/asignación completa antes de adoptar estado e invalidar configuraciones derivadas; mantiene redes, IDs y topología. `saveNode()` integra el mismo contrato con edición normal de fabricante; `buildTopology()` conserva `modelId` y puertos previos válidos al regenerar.
- `saveLink()` asigna antes de guardar. `lockCatalogLinkFields()` deja los nombres nativos del modelo como lectura, sin pedirlos al usuario; las referencias genéricas históricas conservan su edición existente.
- `endpoint()` sigue siendo la entrada común de nombres para los cuatro adaptadores, cuyas plantillas no se duplican. Perfiles archivados no sustituyen los nombres del catálogo cuando hay modelo explícito. Comparación advierte que una sintaxis alternativa usa puertos genéricos, sin atribuir un segundo hardware al mismo nodo.
- `validateImport()` valida `modelId` cerrado y enlaces antes de adoptar proyecto; exportación y localStorage lo conservan automáticamente con el resto de nodos. v2/v3/v4 sin ese campo siguen funcionando. No se almacena inventario duplicado en cada proyecto.

Las funciones nuevas y modificadas incluyen comentarios en español. Roles, variantes, fuentes y límites conservadores: [catálogo de modelos](catalogo-modelos.md). No se certifican equipos físicos ni se ejecutan comandos.

## Estado confirmado y presentación temporal

`state` es el proyecto confirmado. `state.version` sigue siendo 4; los contratos v2/v3 migran a v4 sin reasignar redes. `project.base` es el **fallback**, no un contenedor obligatorio de todas las sedes. `sites[].ipv4Base` es un pool privado independiente. `project.transitBase`, si existe, separa los enlaces /30. Si una sede no define bloque usa el fallback libre; si no hay tránsito explícito usa ese mismo espacio libre excluyendo todas las LAN y reservas.

Los bloques deben ser RFC1918 completos y estar alineados. `192.168.66.0/22` no es una red alineada: su red es `192.168.64.0/22`. Se rechaza la primera expresión; no se corrige silenciosamente. Los nombres/direcciones de las pruebas son datos ficticios del runner, no valores de sedes introducidos en producción.

`formDrafts`, `inventoryEditing`, `vlanEditing`, `topologyZoom` y la página son presentación temporal. Los borradores sobreviven a navegación y cambio de idioma en la sesión; **no se confunden con datos confirmados guardados en JSON**. Confirmar y luego guardar persiste cantidades reales. La preferencia ES/EN sigue en su clave local independiente, fuera del proyecto.

### Extensiones opcionales de v4

- `sites[].vendorProfile`: `{router, core, distribution, access, firewall, backupRouter}`; cada valor es una cadena de la lista de fabricantes permitidos para su función o vacío.
- `nodes[].autoKey`: asociación estable sede:función:tipo:ordinal para entidades nuevas autogeneradas.
- `nodes[].vendorOverride` / `nameOverride`: booleanos opcionales que conservan la elección individual al regenerar.
- `Genérico`: fabricante sin adaptador para terminales, AP, impresoras, cámaras y servidores; no se permite en router, switch, core o firewall.

El importador acepta proyectos antiguos sin esos campos y no infiere perfiles, autoría automática ni marcas nuevas. Las extensiones pasan por listas/tipos explícitos; no admiten propiedades arbitrarias en perfiles. Un programa antiguo puede rechazar el nuevo valor `Genérico`: la compatibilidad garantizada aquí es **importar los proyectos antiguos en esta versión**, no ejecutar el archivo nuevo en una versión anterior.

## A. Direccionamiento y asignación VLSM

1. `privateIPv4Block()` reutiliza `subnet()` y aritmética IPv4 existente; exige red alineada y contención completa en 10/8, 172.16/12 o 192.168/16.
2. `validateSiteBlocks()` valida fallback, cada pool de sede y tránsito. Solo el pool propio contiene las VLAN de esa sede. Dos sedes nunca se solapan; sede y tránsito tampoco.
3. `allocationPools()` construye un mapa por ID de sede. El fallback puede contener reservas parciales de sedes: estas se excluyen al buscar espacio libre.
4. `manualVlanNetworks()` valida **todas** las subredes manuales antes de reservarlas: pertenencia, capacidad, crecimiento, gateway y solapamientos.
5. `allocate()` reserva manuales, luego redes previas automáticas no afectadas que siguen siendo válidas y /30 reutilizables. Las nuevas solicitudes se ordenan por tamaño y clave estable.
6. `findIPv4Space()` alinea al tamaño del CIDR y salta intervalos reservados; tener IP libres dispersas no garantiza un bloque contiguo.
7. Si no cabe una solicitud, el asignador lanza un error contextual. No amplía ni mueve intenciones manuales ni guarda un plan parcial.
8. `confirmVlans()` adopta el resultado solo tras terminar correctamente. El plan y su orden son estables para la misma entrada y estado previo. Conservar redes previas válidas implica que un proyecto editado puede ocupar huecos diferentes de uno nuevo equivalente; es una decisión explícita de estabilidad, no aleatoriedad.

El cálculo mantiene hosts, crecimiento, reservas (una o tres), gateway automático/manual, máscara, broadcast, `required`, `size` y capacidades. IPv6 conserva su implementación independiente; esta revisión no añade configuración IPv6 por fabricante.

## B. Confirmaciones e invalidación

### Inventario

Sin `counts` se muestra formulario con estimaciones. Confirmar valida todos los campos y usa `counts` como cantidades confirmadas persistidas. Entonces aparece resumen y **Editar inventario**. Editar no destruye el diseño. Restaurar estimación pide confirmación; cancelar no cambia datos. Las fórmulas de `estimated()`, `counts()` y `proposal()` permanecen iguales.

### VLAN

Sin cálculo válido aparece **Pendiente de confirmación**; tras éxito, **VLAN confirmadas** y **Recalcular VLAN**. Escribir valores realmente distintos establece un borrador. No se permite generar dependencias mientras exista ese borrador; sí navegar a calculadora, seguridad u otras vistas independientes y regresar a corregir. Confirmar una entrada idéntica conserva revisión, plan, aprobación, nodos, enlaces y CLI.

### Sedes y dependencias

Guardar una ficha idéntica no invalida. Nombre o ancho de banda no requieren destruir redes; un cambio de nombre retira sus CLI cuando pueden contener comentarios anteriores. Un cambio de bloque invalida las LAN/topología locales; cambios de inventario/estructura requieren reproponer sus VLAN. Las demás VLAN, LAN, /30 válidas y equipos se conservan cuando no dependen del cambio. `proposeVlans()` completa únicamente sedes sin VLAN; «Volver a proponer» permite el reemplazo total explícito. Un bloque nuevo incompatible con un CIDR manual ya guardado se rechaza antes de confirmar la ficha.

`invalidateSite()` y la confirmación diferencial retiran CLI afectadas y las de vecinos cuyo enlace WAN cambió. No se conserva una CLI como válida si ya perdió su interfaz. Las CLI retenidas reciben la revisión vigente. `routerId()` estabiliza los IDs automáticos numéricos `nN` de laboratorio, evitando renumerar otra sede por quitar nodos; IDs personalizados conservan su regla histórica.

Los equipos manuales se conservan al regenerar. Si quedan IP/enlaces incompatibles, deben corregirse con los editores y se bloquean generadores; no se mueven direcciones manuales silenciosamente. La generación de topología valida un candidato completo antes de sustituir entidades.

## C. Topología y fabricantes

El usuario selecciona fabricantes por sede y función **antes de generar**. Router, core, acceso y distribución (si existe) requieren selección explícita. Firewall y router secundario son opcionales; si cambian, se recalculan VLAN para crear sus /30. No se presupone Internet, NAT, VPN ni políticas permisivas.

| Función | Fabricantes admitidos en este adaptador |
| --- | --- |
| Router principal/secundario | Cisco, Huawei, MikroTik |
| Core capa 3 | Cisco, Huawei |
| Distribución/acceso | Cisco, Huawei |
| Firewall opcional | Fortinet |
| Terminales y AP | Genérico; sin CLI propia |

Dos cores redundantes deben usar un mismo fabricante: HSRP y VRRP no forman un grupo interoperable. La mezcla sí se permite entre funciones y sedes. No se certifica interoperabilidad física ni firmware.

`buildTopology()` consume VLAN, /30 e inventario reales, crea claves estables y puertos independientes por marca. IDs se reutilizan al regenerar; equipos manuales permanecen. Los proyectos anteriores carecen de `autoKey`, así que no se presume que un equipo antiguo fuera automático ni se elimina como tal.

`siteCode()` deriva iniciales/números del nombre real, elimina acentos y resuelve colisiones con ID. Los hostnames usan prefijos de función y ordinales; los cambios individuales explícitos se preservan con overrides. No hay nombres de las sedes del enunciado codificados como datos productivos.

`arrangeTopology()` cambia solo coordenadas por sede, nivel, fila y columna. `svgTopology()` dibuja iconos originales inline; enlaces WAN, routed, trunk y access tienen estilos distintos y canales fuera de las cajas. En diagramas densos se omiten etiquetas permanentes de enlace y se consultan con hover/tablas para evitar amontonamientos. La separación automática se comprueba para cajas; el arrastre manual permite que el usuario vuelva a superponer equipos. No se promete resolver todo cruce de enlaces posible.

Zoom limita escala; el contenedor desplaza el dibujo, sin comprimir etiquetas. Se conservan arrastre, editor por clic/Enter, creación de enlaces, carga de imagen local y descarga SVG autónoma. La imagen sigue siendo referencia manual; no OCR.

### Generadores reales y Comparación

`configNodes()` filtra equipos realmente asignados a la marca. El generador Huawei ya no ofrece equipos Cisco como si fueran Huawei. **Comparación** conserva equivalencias explícitas de IOS/VRP, sin cambiar fabricantes del modelo.

Los cuatro adaptadores conservan sus familias de comandos, validadores y políticas anteriores. Cambia la selección real y la precondición de aprobación. `endpoint()` obtiene puerto e IP de los mismos enlaces del modelo. Cambiar una marca individual exige puertos válidos para destino y confirmación; no convierte roles incompatibles. Las configuraciones son IPv4 y revisión textual: no se ejecutan, no demuestran conectividad ni compatibilidad física.

## D. Interfaz retirada sin eliminar cálculos ni entregables

Se retiraron exclusivamente el desplegable explicativo VLSM/CIDR/gateway, el desplegable Interpretación de Subnetting y el módulo Evidencias Corte 2. El diseño anterior tenía 13 módulos; la consola añade el módulo 14, índice 13, sin reintroducir Evidencias Corte 2; Fortinet 10, MikroTik 11 e IPv6 12. La barra de progreso y navegación usan el mismo arreglo `steps`. Calculadora, resultados, algoritmos, comparación y todos los documentos/capturas académicos permanecen.

## E. Contratos de funciones nuevas o modificadas

Los encabezados de código explican entrada, salida y efectos. Se usan comentarios por bloque para plantillas HTML/SVG: insertar comentarios dentro de atributos, cadenas CLI o expresiones rompería el programa y no se hace. Los cálculos estables no se reescriben para aumentar artificialmente el número de comentarios.

| Función | Entrada | Proceso, salida y efectos |
| --- | --- | --- |
| `invalidateSite()` | ID estable de sede y decisión de conservar sus VLAN. | Filtra dependencias locales y CLI de vecinos WAN; conserva otras sedes y actualiza revisión. |
| `captureDraft()` | Página y controles visibles de sede, inventario o VLAN. | Copia valores/checks en memoria de presentación; no guarda datos sin confirmar en JSON. |
| `restoreDraft()` | Página activa y borradores asociados a su sede. | Restaura solo controles existentes; no cambia el estado confirmado ni dispara eventos. |
| `selectSite()` | Índice elegido en el selector. | Captura primero el formulario anterior, cambia la ficha y vuelve a renderizar. |
| `editCounts()` | Índice de sede con cantidades confirmadas. | Abre el formulario; no invalida hasta confirmar cantidades realmente diferentes. |
| `vlanFormChanged()` | Valores visibles y última intención confirmada. | Devuelve un booleano comparando campos; no parsea, asigna ni guarda entradas. |
| `requireConfirmedPlan()` | Aprobación, plan efectivo y bandera de borrador. | Lanza un error si falta cálculo confirmado; las vistas independientes siguen navegables. |
| `go()` | Índice de módulo solicitado. | Conserva borradores, limita el índice al menú vigente y desplaza al encabezado. |
| `render()` | Estado confirmado, idioma, página y preferencias visuales. | Reconstruye únicamente la vista; restaura borradores y enlaza eventos de esa página. |
| `projectView()` | Proyecto y sede seleccionada. | Devuelve HTML escapado para datos y bloque propio; no escribe estado. |
| `saveSite()` | Ficha visible con nombre, bloque, usuarios y opciones. | Valida una candidata completa; igualdad conserva diseño y cambio real invalida solo dependencias locales. Rechaza nuevos pools incompatibles con intenciones manuales confirmadas. |
| `estimateView()` | Cantidades reales o fórmulas estimadas por sede. | Devuelve formulario o resumen confirmado junto con infraestructura y ancho de banda, sin cambiar fórmulas. |
| `saveCounts()` | Cantidades visibles, dentro de límites numéricos. | Valida todo antes de confirmar; diferencias reales invalidan su sede, cantidades iguales no destruyen diseño. |
| `resetCounts()` | Índice de sede y confirmación nativa del usuario. | Cancelar conserva todo; aceptar retira la personalización y aplica estimación vigente. |
| `vlanView()` | Intenciones, aprobación y último plan efectivo. | Muestra fallback, tránsito, CIDR manual, estado pendiente/confirmado y redes calculadas; no asigna. |
| `addVlan()` | Filas actuales del formulario. | Incorpora primero ediciones válidas y añade una clave nueva; falla sin renderizar si otra fila es inválida. |
| `deleteVlan()` | Índice elegido y confirmación del usuario. | Lee todas las filas antes de eliminar una; conserva texto ante validación fallida e invalida el plan dependiente. |
| `readVlans()` | Controles de cada VLAN y opciones de direccionamiento visibles. | Devuelve candidatas validadas; comprueba IDs, gestión e intenciones manuales sin sustituir estado. |
| `initialTransits()` | Sedes, redundancia, interconexión y perfiles opcionales. | Devuelve solicitudes /30 por clave estable, incluidos firewall y router secundario; no inventa Internet. |
| `allocationPools()` | Fallback candidato, proyecto y lista de sedes. | Devuelve pools numéricos independientes y reservas; valida RFC1918, alineación y separación. |
| `allocate()` | VLAN candidatas, fallback, crecimiento, solicitudes de tránsito y proyecto candidato. | Reserva manuales y redes no afectadas válidas; busca huecos CIDR en cada pool y devuelve un plan completo o lanza error. |
| `confirmVlans()` | Formulario visible y último diseño confirmado. | Calcula antes de guardar; error conserva todo, igualdad mantiene aprobación y cambios invalidan dependencias diferenciales. |
| `planTable()` | Filas efectivas del plan. | Devuelve tabla de redes/gateways/capacidad y origen manual o automático; no confunde intención con resultado. |
| `subnetView()` | Último cálculo y plan IPv4/IPv6. | Devuelve resultados completos sin el desplegable retirado; las funciones matemáticas permanecen separadas. |
| `vendorProfile()` | Sede, con o sin perfil heredado. | Devuelve las seis funciones con cadenas explícitas; vacío significa que debe elegir, no Cisco implícito. |
| `validateVendorProfile()` | Objeto opcional recibido del formulario o JSON. | Rechaza claves y combinaciones ajenas a la lista permitida; devuelve una copia conocida. |
| `vendorProfilesView()` | Perfiles de todas las sedes. | Devuelve selectores por función, incluyendo opcionales; no convierte firewalls en switches. |
| `saveVendorProfiles()` | Todos los selectores de fabricantes. | Valida en conjunto, pide confirmación ante equipos existentes y exige recalcular si cambian tránsitos. |
| `validateNodeVendor()` | Tipo y fabricante de un equipo candidato. | Bloquea roles no implementados: Fortinet solo firewall, MikroTik solo router y Genérico solo terminal. |
| `buildTopology()` | Plan confirmado, inventario, perfiles y entidades existentes. | Valida perfiles/capacidad; genera por clave, conserva IDs y manuales, prueba el candidato completo y solo después lo adopta. |
| `siteCode()` | Nombre real de sede e ID estable. | Normaliza caracteres, deriva iniciales/números y agrega ID solo cuando hay colisión entre sedes. |
| `arrangeTopology()` | Equipos existentes y opción de renderizar. | Ordena por sede, jerarquía e ID; cambia únicamente coordenadas y nunca borra entidades. |
| `zoomTopology()` | Factor solicitado por botones. | Limita escala entre 0,25 y 3; modifica solo ancho visual del SVG, sin cambiar coordenadas del modelo. |
| `deviceIcon()` | Tipo de equipo de la lista permitida. | Devuelve trazados SVG originales embebidos; no utiliza fuentes, Internet ni recursos protegidos. |
| `svgTopology()` | Nodos, enlaces, posiciones y plan actual. | Devuelve SVG autónomo con iconos, carriles, títulos y detalles escapados; sirve para pantalla y descarga. |
| `editNode()` | ID existente o cadena vacía para alta manual. | Abre un editor; altas requieren elegir fabricante y no asignan Cisco de forma implícita. |
| `saveNode()` | Campos del editor y enlaces del equipo. | Valida rol, IP y puertos antes de guardar; conserva overrides explícitos y solicita aprobación al cambiar fabricante. |
| `routerId()` | ID del equipo y orden legado. | Conserva router-ID de IDs automáticos nN al editar otras sedes; IDs personalizados mantienen regla histórica. |
| `configNodes()` | Nombre oficial del fabricante. | Filtra exclusivamente nodos asignados y soportados; las equivalencias viven solo en Comparación. |
| `configView()` | Fabricante Cisco o Huawei. | Muestra nodos reales, opciones y CLI guardadas; no ofrece un Cisco como equipo Huawei. |
| `assertReady()` | Nodo IOS/VRP, opciones y topología. | Exige plan confirmado sin borradores y dependencias técnicas válidas antes de producir CLI. |
| `generateFortinet()` | Firewall Fortinet con interfaces explícitas del plan. | Exige aprobación efectiva y controles existentes; conserva gramática FortiOS, políticas seguras y límites de laboratorio. |
| `generateMikroTik()` | Router MikroTik con interfaces explícitas del plan. | Exige aprobación efectiva y validaciones existentes; conserva gramática RouterOS y endurecimiento sin ejecutar comandos. |
| `validateSiteBlocks()` | Proyecto y candidatas de todas las sedes. | Valida privacidad y alineación de cada dominio; rechaza solapamientos sede/sede y sede/tránsito sin exigir contención global. |
| `validateImport()` | Objeto JSON v2, v3 o v4 no confiable. | Reconstruye contrato, perfiles y overrides opcionales; valida pools/plan, relaciones y CLI sin asignar nuevas redes y restaura estado temporal. |
| `applyImport()` | Resultado ya validado por validateImport. | Reemplaza proyecto de forma atómica y limpia borradores/banderas anteriores; no llama al asignador. |
| `newProject()` | Confirmación de crear un proyecto nuevo. | Reinicia estado y borradores solo si acepta; conserva claves de almacenamiento y preferencia de idioma. |
| `topologyView()` | Estado gráfico, imagen y perfiles. | Devuelve lienzo desplazable, zoom, editores y tablas de detalles técnicos sin sustituir datos. |
| `setLanguage()` | Código es/en y presentación visible. | Traduce avisos simples y controles sin mutar proyecto, CLI ni JSON; conserva preferencia independiente. |
| `demo()` | Confirmación de reemplazo por laboratorio ficticio. | Reinicia datos y borradores; conserva almacenamiento previo y preferencia independiente de idioma. |
| `proposeVlans()` | Inventario y opción explícita de reemplazo total. | Completa solo sedes sin VLAN, conservando claves y CIDR de otras; el reemplazo total exige confirmación. |

## F. Funciones principales conservadas y sus relaciones

| Función / familia | Papel en el sistema |
| --- | --- |
| `fresh`, `siteDefault` | Construyen proyecto v4 y sedes vacías; no inventan datos reales. |
| `projectValid`, `text`, `num`, `enumVal`, `idVal`, `hostname` | Validación de requisitos, límites y contenido antes de mutar. |
| `estimated`, `counts`, `proposal` | Fórmulas de demanda e infraestructura, sin cambios en esta revisión. |
| `subnet`, `ipNum`, `ipStr`, `isHost` | Aritmética IPv4, red, máscara, broadcast y capacidad. |
| `privateIPv4Block`, `findIPv4Space`, `manualVlanNetworks` | Privacidad, búsqueda alineada y reservas manuales. |
| `ipv6Subnet`, `allocateIPv6`, `confirmIPv6`, `validateIPv6Plan` | IPv6 separado con cadenas persistidas y BigInt solo en memoria. |
| `availableIPs`, `coreIP`, `endpoint` | Reservas físicas/virtuales, gateway y extremos reales de interfaces. |
| `validateLink`, `topologyIssues`, `bindDrag` | Integridad de enlaces, bloqueos técnicos y edición del diagrama. |
| `configurable`, `routed`, `switching` | Capacidades por tipo, nunca equivalencia indiscriminada. |
| `generate`, `generateFortinet`, `generateMikroTik` | Adaptadores independientes; producen texto con datos del plan. |
| `generateCompare` | Equivalencia IOS/VRP solicitada expresamente. |
| `securityWarnings`, `securityView` | Advertencias contextualizadas, sin afirmar auditoría exhaustiva. |
| `exportJSON`, `saveLocal`, `loadLocal`, `importJSON` | Descarga/importación y persistencia v4 con fallback no destructivo v3/v2. |
| `migrateV2`, `migrateV3`, `applyImport` | Migración sin asignadores y adopción posterior a validación atómica. |
| `I18N`, `t`, `setLanguage` | Traducción de presentación sin traducir datos, JSON, nombres ni CLI. |
| `download`, `copyConfig`, `downloadConfig`, `downloadReport` | Exportación/copia local con acciones reales y validación previa. |

### Índice exhaustivo de declaraciones de función del archivo

La lista sirve para localizar código y distinguir el mapa general de los contratos detallados anteriores. Las funciones internas auxiliares anidadas siguen documentadas en su bloque contenedor.

`t()`, `localizeMessage()`, `setLanguage()`, `fresh()`, `siteDefault()`, `fail()`, `num()`, `text()`, `hostname()`, `commandName()`, `ipNum()`, `ipStr()`, `ipType()`, `subnet()`, `isHost()`, `safe()`, `toast()`, `invalidateSite()`, `captureDraft()`, `restoreDraft()`, `selectSite()`, `editCounts()`, `vlanFormChanged()`, `requireConfirmedPlan()`, `invalidate()`, `optsHTML()`, `field()`, `badge()`, `go()`, `title()`, `render()`, `estimated()`, `counts()`, `proposal()`, `projectValid()`, `projectView()`, `saveProject()`, `resizeSites()`, `removeSite()`, `saveSite()`, `estimateView()`, `saveCounts()`, `resetCounts()`, `proposeVlans()`, `siteName()`, `vlanView()`, `addVlan()`, `deleteVlan()`, `readVlans()`, `initialTransits()`, `allocationPools()`, `findIPv4Space()`, `vlanGatewayIntent()`, `manualVlanNetworks()`, `allocate()`, `confirmVlans()`, `planTable()`, `editGateway()`, `inspectSubnet()`, `subnetView()`, `subnetResult()`, `calculate()`, `ipv6Number()`, `ipv6String()`, `ipv6In()`, `ipv6Type()`, `ipv6Subnet()`, `addressCalculation()`, `addressResult()`, `ipv6Intent()`, `ipv6Block()`, `ipv6Blocks()`, `ipv6Row()`, `allocateIPv6()`, `validateIPv6Plan()`, `newULAPrefix()`, `toggleIPv6()`, `confirmIPv6()`, `ipv6View()`, `row()`, `node()`, `routed()`, `switching()`, `configurable()`, `availableIPs()`, `coreAddress()`, `vendorProfile()`, `validateVendorProfile()`, `vendorProfilesView()`, `saveVendorProfiles()`, `validateNodeVendor()`, `buildTopology()`, `topologyView()`, `siteCode()`, `arrangeTopology()`, `zoomTopology()`, `deviceIcon()`, `svgTopology()`, `bindDrag()`, `modal()`, `closeModal()`, `editNode()`, `saveNode()`, `deleteNode()`, `editLink()`, `interfaceName()`, `saveLink()`, `validateLink()`, `deleteLink()`, `loadImage()`, `downloadSVG()`, `connected()`, `endpoint()`, `routerId()`, `configNodes()`, `configView()`, `configControls()`, `changeOpts()`, `assertReady()`, `generate()`, `fortinetNode()`, `fortinetInterfaceName()`, `fortinetInterfaces()`, `fortinetPath()`, `fortinetRoute()`, `generateFortinet()`, `fortinetControls()`, `changeFortinetOpts()`, `generateFortinetFromForm()`, `fortinetView()`, `mikrotikNode()`, `mikrotikInterfaceName()`, `mikrotikInterfaces()`, `mikrotikRoute()`, `mikrotikDhcpRanges()`, `generateMikroTik()`, `mikrotikControls()`, `generateMikroTikFromForm()`, `mikrotikView()`, `trunkCommands()`, `wildcard()`, `generateSelected()`, `generateAll()`, `configBlock()`, `compareView()`, `generateCompare()`, `copyConfig()`, `downloadConfig()`, `downloadAll()`, `topologyIssues()`, `securityWarnings()`, `securityView()`, `dashboard()`, `download()`, `exportJSON()`, `saveLocal()`, `loadLocal()`, `importJSON()`, `privateIPv4Block()`, `validateSiteBlocks()`, `migrateV2()`, `migrateV3()`, `optionalAddressIntent()`, `validateImport()`, `enumVal()`, `bool()`, `idVal()`, `unique()`, `applyImport()`, `newProject()`, `demo()`, `downloadPlan()`, `downloadReport()`.

## G. Verificación y límites

Ejecute `python tests/test_corte3.py`. Conserva C01–C31 y añade N01–N19; consulte [resultados actuales](pruebas.md). Las expectativas de navegación/fabricantes se actualizan porque son cambios autorizados. **No se cambiaron hashes de referencia**: C26 usa un proyecto previo real preservado en `tests/fixtures/pre-revision-v4.json` y las referencias anteriores para ocho comparaciones CLI ES/EN. Una nueva topología sí cambia nombres, posiciones, categorías representativas y fabricante elegido; no se oculta esa diferencia como igualdad bit a bit.

El runner abre/cierra HTTP y contextos limpios, informa esperado/obtenido/estado y falla con código no cero. Los resultados no prueban infraestructura real ni todas las combinaciones de tamaños, navegadores, accesibilidad o topologías. Los diagramas de revisión están fuera del repositorio; las capturas académicas y el PDF anteriores se conservan como evidencia histórica del commit al que corresponden, no como capturas de esta nueva interfaz.

## H. Confirmaciones y consola SSH opcional

Esta ampliación conserva el modelo v4 y los pools independientes anteriores. `sites[].confirmed` es un booleano opcional validado; solo guardar una ficha válida lo publica como true. `siteEditing`, `sitePending` y `siteSnapshots` son presentación temporal: distinguen editar de cambios reales sin borrar el último estado confirmado. Los importadores no infieren confirmación de archivos antiguos y excluyen banderas temporales durante su validación interna, restaurándolas si rechazan el archivo.

`updateVlanStatus()` actualiza estado y placeholders sin renderizar; vacío significa intención automática, no un ejemplo numérico fijo. Tras confirmar se muestra la red efectiva del pool real. `confirmVlans()` conserva transacción e invalidación diferencial y marca pendiente/foco tras error; `allocate()` expone demanda completa y solo estima un prefijo mínimo cuando es matemáticamente justificable. `requireConfirmedPlan()` incluye borradores de sede y VLAN; no bloquea calculadora ni SSH manual.

### Funciones JavaScript de presentación y sesión

| Función / variables | Entrada, salida y efectos |
| --- | --- |
| `editSite`, `siteFormSnapshot` | Recuperan formulario sin borrar valores, capturan referencia para comparar cambios; no invalidan por entrar a editar. |
| `saveSite`, `projectView` | Candidata validada, confirmed opcional, resumen/bloqueo y acción Editar; guardar idéntico preserva redes/CLI. |
| `sshConsoleView`, `sshTab`, `sshChooseDevice`, `sshSelected` | HTML escapado y selección por ID; pestañas independientes, sin cambiar fabricante/plan. Cambiar vista cierra una sesión real. |
| `sshManagementAddress` | Solo toma IP explícita de Gestión; no infiere desde gateway, SVI o WAN. |
| `sshCommands`, `sshRunSimulation` | Lista cerrada por marca; consultas al modelo/CLI vigente. Nunca red, eval ni emulación de NOS completo. |
| `sshHistory`, `sshClearSimulation`, `sshResetSimulation` | Buffer educativo limitado a 40.000 caracteres, sin persistencia. Nuevo proyecto/importación limpia selección e historial. |
| `sshAuthMethod` | Muestra método y vacía credenciales que dejan de usarse. |
| `sshLoadTerminal` | Carga solo recursos locales de xterm/fit al conectar realmente; la simulación no los requiere. |
| `sshSetStatus` | Estado visual y bloqueo de campos durante conexión. connected solo procede del backend autenticado con PTY abierto. |
| `sshConnect` | Valida autorización y formulario, obtiene cookie/token local, envía credenciales una vez por WS y las borra del DOM. No envía state ni configuraciones. |
| `sshSocket`, `sshTerminal`, `sshObserver` | Sesión efímera fuera del proyecto; Uint8Array conserva bytes/ANSI; onData envía teclas, ResizeObserver envía dimensiones. |
| `sshGeneration`, `sshConnecting` | Evitan doble conexión y la continuación de una operación asíncrona cancelada. |
| `sshDispose`, `sshDisconnect` | Cierre idempotente de WS, observador, terminal y secretos al salir/cancelar; nunca deja sesiones ocultas intencionalmente. |
| `sshClearReal` | Solo limpia pantalla local; no envía comandos al equipo. |
| `setLanguage`, `render`, `applyImport`, `newProject`, `demo` | No restauran contraseñas/claves al traducir; cierran sesiones al reconstruir y limpian borradores al sustituir proyectos. |

### Servicio Python: funciones y dependencias

`ssh_service/server.py` es opcional y no se importa desde la aplicación. AsyncSSH 2.24.1 aporta transporte/host keys/PTY, aiohttp 3.14.5 HTTP/WS. El mismo proceso atiende un puerto loopback configurable; no abre un listener SSH ni sirve un directorio arbitrario.

| Función | Contrato y seguridad |
| --- | --- |
| `integer`, `load_config` | Tipos/límites estrictos, lista permitida de claves y destinos exactos; targets vacío prohíbe toda conexión. |
| `destination` | Resuelve solo un host/puerto autorizado y exige que todas las IP estén fijadas; devuelve IP literal a conectar. |
| `create_app` | Factory sin iniciar servidor; crea confianza local, cuotas y autorizaciones efímeras. Facilita pruebas reales aisladas. |
| `boundary` | Host/origen exactos, no caché/CORS; bloquea rebinding y páginas ajenas. |
| `index`, `asset`, `manual`, `favicon` | Solo HTML conocido, tres recursos concretos y manual; no endpoints para archivos/OS arbitrarios. |
| `bootstrap` | Cookie HttpOnly/SameSite Strict y CSRF en RAM para el mismo origen; no usa URL/localStorage ni tokens impresos. |
| `websocket` | Primer mensaje autorizado en 5 s, allowlist, host key estricta, autenticación, shell/PTY y bucle input/resize/ack. finally recoge recursos y secretos. |
| `connect_for_socket` | Carrera controlada entre negociación y cierre de WS; cancela ambas tareas y no abre PTY después de cancelar. |
| `output` | Lee ≤4096 bytes y espera ACK del navegador tras representar; limita memoria y cierra por EOF/error/timeout. stderr se combina con stdout. |
| `public_error` | Códigos estables sin datos sensibles; tolera que el transporte ya haya cerrado. |
| `shutdown` | Cierra WS/SSH al apagar y elimina autorizaciones efímeras. |
| `trust_host` | Solo destinos aprobados, prueba de huella pública y registro tras coincidencia externa; rechaza cambios de clave existentes. |
| `main` | CLI Windows/Linux, binding 127.0.0.1, puerto configurable y sin access logs; no subprocess/exec del OS. |

El protocolo WS usa connect (credenciales solo en memoria), status/error, output (bytes base64), input, resize, ack y disconnect. No hay mensaje exec ni aplicación del generador. Usuario y dispositivo determinan los comandos manuales; la biblioteca no simula haber conectado. Un servidor sin shell/PTY se rechaza con un error explícito en lugar de fingir interacción.

Detalles, tamaños, modelo de confianza, instalación Windows, rotación de claves y solución de problemas están en [manual SSH](manual-ssh.md) y [README del servicio](../ssh_service/README.md). Código de terceros en static se conserva sin reescribir, con licencias y hashes; los comentarios nuevos propios están en español. No se insertan comentarios dentro de cadenas CLI/atributos donde romperían el programa.

Pruebas actuales: [pruebas-ssh.md](pruebas-ssh.md). El mecanismo SSH se probó realmente en loopback, no físicamente en marcas. Windows no ejecutado y file:// bloqueado por política son límites declarados, no éxitos inferidos.


## Navegación y aprobación efectiva — ajustes adicionales del PR #10

La causa de acceso indebido era que `go(i)` no verificaba dependencias: el control existía solo al generar. Otra causa de rechazo falso era usar `vlanEditing` como verdad persistente después de un intento fallido o una edición revertida, en lugar de comparar datos.

`confirmedPlan()` exige `approved === true`, VLAN y plan no vacíos, claves únicas, redes/máscaras/números coherentes, tránsitos requeridos y correspondencia de sede, ID, nombre, servicio, DHCP, hosts, pool, capacidad y CIDR manual. No ejecuta `allocate()`, no reasigna ni cambia datos. `pendingVlans()` consulta controles visibles o el borrador conservado, aun al intentar un salto programático de página. Revertir valores recupera una aprobación realmente válida; una bandera sola no confirma ni invalida redes.

`requireConfirmedPlan()` es el guardián compartido de navegación, topología y adaptadores. `dependentPage()` identifica seis vistas dependientes. `go()` comprueba antes de capturar/reconstruir el formulario; un rechazo conserva DOM y estado. `render()` protege además una asignación directa de página. `updateVlanStatus()` actualiza badge, previsualización y botón Continuar con el mismo resultado, sin renderizar filas. Las comprobaciones de aprobación de la simulación SSH también usan esta fuente. Los módulos independientes no quedan bloqueados por VLSM.

## Perfiles físicos opcionales y compatibilidad

**Decisión vigente:** se retiraron `editPhysicalProfile()`, `savePhysicalProfile()`, `requirePhysicalProfile()` y sus accesos/traducciones exclusivos. No existe formulario ni confirmación física adicional para generar CLI. La advertencia de revisar los puertos antes de aplicar es informativa. Se restauró `configBlock()` sin botones/estados de confirmación física; los cuatro adaptadores mantienen sus plantillas, datos reales de plan/enlaces y validaciones de seguridad.

`endpoint()` vuelve a obtener la interfaz de `links[].ac/bc` para Cisco, `ah/bh` para Huawei, `af/bf` para Fortinet y `am/bm` para MikroTik. `buildTopology()` sigue proponiendo nombres deterministas por fabricante, y `editLink()` permite ajustarlos sin formulario nuevo. Los generadores y la simulación comparten esa resolución. No se descubren puertos ni se certifica un modelo; el usuario revisa la propuesta antes de cualquier aplicación física.

La extensión opcional `nodes[].interfaceProfiles` de algunos proyectos v4 previos **se conserva solo como archivo**: no se cambian versión, migradores ni claves locales; los proyectos sin esa propiedad no la necesitan. Se mantienen sus campos conocidos `model/version/source/confirmed/ports`, con las restricciones de tipo/seguridad del lector. `physicalName()`, `physicalBinding()` y `validatePhysicalProfile()` atienden exclusivamente esos metadatos importados; no son requisitos del flujo de generación automática ni una fuente activa de nombres.

`refreshPhysicalProfiles()` conserva coherencia de los metadatos legados al editar/eliminar enlaces, sin pedir reconfirmación ni impedir regeneración. Se mantienen equipos manuales, perfiles de fabricantes mixtos, IDs, redes y CLI no afectadas.

`validateImport()` valida el esquema conocido y comprueba CLI por igualdad con una salida canónica. Primero prueba la generación automática; si no coincide y existe un perfil antiguo válido, prueba la reconstrucción histórica mediante `archivedPhysicalNames` en `try/finally`. Solo una coincidencia exacta conserva el texto; no se acepta CLI arbitraria. Así una exportación del HEAD `9675ce7` con nombres declarados y otra posterior con puertos automáticos pueden restaurar sus textos sin perder metadatos. Ambos caminos son internos a la importación; el indicador vuelve a `false` también ante error. `checkingArchive` sigue evitando consultar borradores de la pantalla al verificar un archivo. La carga nunca ejecuta asignadores.

## Orden de módulos y dependencias

`steps` y la lista de vistas de `render()` tienen el mismo orden: 06 Cisco, 07 Huawei, 08 Fortinet, 09 MikroTik, 10 Comparación, 11 Ciberdefensa, 12 IPv6 y 13 SSH. Los módulos 00–05 permanecen. `dependentPage()` protege 05–10 con `requireConfirmedPlan()`; Ciberdefensa queda independiente en 11. La inserción del aviso IPv4 se aplica ahora a 06–09. Menú, flechas, traducciones y progreso se derivan de estos índices; ningún índice se guarda dentro del proyecto JSON.

## Access Points: administración sin CLI genérica

`accessPoint()` clasifica por tipo, independientemente de la marca. `configurable()` y las listas por rol excluyen AP; la defensa de los adaptadores impide invocaciones directas. No se eliminan AP ni sus VLAN/IP/enlaces. `editNode()` presenta IP, máscara y gateway de gestión; la topología, el inventario, JSON y el puerto del switch vecino permanecen. Un adaptador AP específico requeriría modelo, firmware y modo autónomo/controlador; no se implementó ni se simuló.

Fuentes oficiales y límites léxicos: [matriz de fabricantes](matriz-fabricantes.md). Reproducción, evidencia y relación Q01–Q15: [pruebas de interfaces y navegación](pruebas-interfaces.md).
