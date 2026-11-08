# Manual de usuario — WAN Architect, Corte 3

Versión documental basada en main `f7ed2b907d6edad6f1ed7bd5274c49956a7a77d8`, aplicación `WAN_v4.html`, esquema v4. Las configuraciones son propuestas para revisión manual; **no se ejecutan sobre equipos**. Usar exclusivamente datos ficticios o infraestructura de laboratorio autorizada.

## 1. Instalación y apertura

Descargar/clonar el repositorio completo. Para usar la app basta un navegador actualizado: abrir `WAN_v4.html`, no los nombres antiguos `WAN.html` o `Versión3.html`. No hay backend, cuentas ni paquetes que instalar para su funcionamiento principal.

Para reproducir el entorno de las capturas y disponer de un origen estable:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:8000/WAN_v4.html`. Cerrar con Ctrl+C. No publicar el servidor en Internet. Los enlaces a documentación oficial necesitan conexión; los datos del proyecto se procesan localmente. Cambiar de navegador, puerto o de `file://` a HTTP cambia el origen del almacenamiento: exportar JSON antes de hacerlo.

## 2. Proyecto, sedes e inventario

1. En **Datos del proyecto**, introducir nombre, empresa ficticia, actividad, infraestructura, segmentación y número de sedes. Confirmar datos del proyecto y aplicar el número de sedes.
2. Seleccionar cada sede, registrar pisos, usuarios, áreas, servicios y redundancia; confirmar su ficha. El bloque IPv4 de sede es opcional y debe estar alineado, ser privado, estar dentro del global y no solaparse con otras sedes/tránsito.
3. Revisar **Estimación e infraestructura**. Las cantidades son estimaciones preliminares; no sustituyen estudios RF, inventarios físicos ni dimensionamiento profesional.
4. Preparar las fichas antes de avanzar: `saveSite()` conserva su comportamiento histórico de invalidar VLAN, plan y datos derivados al confirmar. Guardar una copia antes de revisar sedes de un diseño avanzado.

El ejemplo integrado es ficticio. Se puede usar para aprender el flujo sin introducir datos sensibles. No reutilizar su nombre de empresa, DNS o cantidades como si fueran requisitos de una organización real.

## 3. VLAN y direccionamiento IPv4

Proponer VLAN y revisar sede, ID, nombre, servicio, hosts y DHCP de cada fila. Se permite repetir ID entre sedes, pero no dentro de una sede. Mantener una VLAN de Gestión por sede. Los hosts y el crecimiento afectan la capacidad calculada.

En **VLAN y VLSM**, confirmar el bloque global privado, crecimiento y DNS. Vacío en **Subred IPv4 / CIDR (opcional)** mantiene asignación automática; una red manual, por ejemplo `10.20.20.0/24`, no es el gateway ni el pool DHCP. Debe estar alineada, tener capacidad y respetar el bloque de sede o el espacio global libre. LAN /31 y /32 se rechazan. El bloque de tránsito `project.transitBase` se conserva por JSON v4; no tiene control visual propio.

Pulsar **Confirmar VLAN y calcular VLSM**. Primero se reservan manuales/bloques de sede/tránsito; las automáticas buscan huecos CIDR alineados. Si falta capacidad o hay solapamiento, no se sustituye el plan anterior ni se pierden las entradas visibles. No ampliar redes manuales silenciosamente.

El plan muestra redes, prefijos, máscaras, rangos, broadcast IPv4 y gateways. El gateway se edita por separado; debe ser utilizable y no duplicar un endpoint o reservas. Cambiarlo invalida topología/configuraciones para evitar salidas obsoletas. DHCP sigue siendo automático; no hay pools ni reservas manuales editables.

Al eliminar una VLAN se leen antes las ediciones válidas de las otras filas. Cancelar no altera el diseño; una fila inválida bloquea la eliminación sin reconstruir el formulario. Una eliminación confirmada invalida los planes/derivados dependientes; volver a confirmar antes de generar topología.

## 4. Calculadora y planificación IPv6

**Subnetting IPv4 / IPv6** admite IP/CIDR o IPv6/prefijo, por ejemplo `192.168.10.50/26` o `2001:db8:1234:5678::9/64`. Muestra representación canónica, red/prefijo, rango y clasificación. IPv6 no tiene broadcast y su capacidad matemática no descuenta red/broadcast. La clasificación no acredita enrutabilidad ni equivale a una lista de hosts asignables.

En **Planificación IPv6**, habilitar la opción. La app propone un ULA /48 con identificador pseudoaleatorio; confirmar para guardarlo. El proyecto admite ULA local fd00::/8 con prefijo /48–/56; cada sede recibe /56 manual o automático y cada VLAN una /64. No se asigna una dirección pública por generar ULA. La sede sin bloque recibe un /56 del global, excluyendo los bloques manuales reservados. El orden depende de claves estables y no del orden visual de las filas.

Con una sede /56 se pueden planificar hasta 256 VLAN /64. El router se propone como **dirección completa de red + 1**, no como la IP literal `::1`: con redundancia, ::1 virtual y ::2/::3 físicas; sin redundancia, ::1 física. Son reservas, no configuración de protocolos. Confirmar IPv6 no altera el plan IPv4 ni las CLI. Desactivar y confirmar vacía solo la intención y el plan IPv6.

Las VLAN utilizadas son las del estado confirmado; guardar antes sus cambios en la pantalla VLAN/VLSM. Los errores de prefijo, alineación, capacidad, contención o solapamiento conservan formulario, estado y planes anteriores. No hay tránsitos IPv6, DHCPv6, SLAAC avanzado, NAT66 ni políticas IPv6. **Los cuatro generadores siguen siendo IPv4** hasta aclaración docente.

## 5. Topología e interfaces

Tras confirmar IPv4, ir a **Topología → Generar desde el plan**. Revisar roles, sedes, enlaces y puertos. La WAN dibujada es un laboratorio enrutado: no constituye VPN, cifrado ni conexión real con un ISP. Arrastrar nodos solo modifica su posición; generar de nuevo reconstruye el diseño.

Para editar/agregar equipos, usar hostname seguro, tipo y fabricante compatibles. Para cada enlace indicar extremos, tipo, red de tránsito /30 existente y puertos de cada fabricante. Los campos Cisco, Huawei, Fortinet y MikroTik son separados. No repetir un puerto en dos enlaces. Access, trunk y routed tienen validaciones distintas. Una imagen importada se usa como referencia manual; no reconoce automáticamente equipos ni enlaces.

## 6. Generación por fabricante

Las opciones compartidas de OSPF, DHCP/relay y ruta por defecto pueden invalidar propuestas previas al modificarse. No seleccionar simultáneamente DHCP local y relay. Una ruta por defecto exige siguiente salto conectado y justificación; no implica Internet ni NAT. Copiar o descargar texto no lo ejecuta.

### Cisco IOS/IOS XE y Huawei VRP

La topología automática sirve para el flujo de routers/switches y cores. Elegir fabricante, equipo y opciones; generar un equipo o todos. Huawei ofrece equivalencias si no existen nodos Huawei: revisar interfaces y capacidades del modelo real. **Comparación** no convierte hardware ni certifica interoperabilidad. Las propuestas incluyen VLAN, SVI/Vlanif, IP, OSPF, DHCP o relay y funciones según rol/opciones. HSRP y VRRP no forman un mismo grupo interoperable; no mezclar cores de distinta marca para suponer redundancia común.

### Fortinet FortiOS

Supuesto autorizado: FortiGate genérico de laboratorio, FortiOS 7.4, sin multi-VDOM. Crear un nodo **Firewall / Fortinet**, con IP/red del nodo vacíos: los enlaces y el plan aportan las direcciones. Mapear puertos propios `af`/`bf`, por ejemplo `port1` y `port2`. Usar /30 existentes para routed. Un trunk a switch puede hacer que el firewall asuma los gateways LAN, por lo que no debe competir con cores u otros gateways; no hay HA/LACP modelados.

En **Configuración Fortinet**, generar la propuesta y revisar interfaces/VLAN, IP, objetos, administración restringida, DHCP/relay y rutas/OSPF. `root` es el contexto interno de VLAN, no la habilitación de multi-VDOM. No se inventan NAT ni permisos de tránsito; revisar políticas, objetos e IDs antes de una futura aplicación autorizada. La [captura 06](capturas/06-config-fortinet.png) corresponde a este escenario perimetral independiente, sin cores en su sede.

### MikroTik RouterOS

Supuesto: router genérico RouterOS 7.x, sin VRF/CAPsMAN. Crear **Router / MikroTik**, IP/red del nodo vacíos, puertos propios `am`/`bm`, por ejemplo `ether1`/`ether2`. No usar roles o redundancia no modelados. Para LAN, el adaptador genera bridge y filtrado VLAN a partir de enlaces reales; routed usa las /30 del plan. No asignar los mismos gateways a MikroTik y cores/firewalls.

En **Configuración MikroTik**, revisar identidad, puertos, bridge/VLAN, IPv4, rutas, OSPF v7 y DHCP/relay. SSH se restringe a Gestión; servicios innecesarios y acceso MAC se deshabilitan. **Forward queda bloqueado por defecto** hasta definir permisos explícitos. No se supone NAT/Internet ni se entrega una configuración de producción lista sin revisión. La [captura 07](capturas/07-config-mikrotik.png) no demuestra compatibilidad física.

No combinar el laboratorio automático con cores y el escenario perimetral que reclama sus gateways. Son alternativas de laboratorio compatibles con el mismo modelo, no un único diseño de gateways duplicados.

## 7. Guardar, importar y exportar

- **Guardar proyecto:** escribe `WAN-Architect-v4` en localStorage del origen actual; no es almacenamiento cifrado ni respaldo remoto.
- **Cargar guardado:** prioriza v4; si no existe, busca v3 y luego v2. Un v4 corrupto se rechaza, no se oculta cargando silenciosamente otra copia.
- **Exportar JSON:** guarda `{ state, imageData }` en esquema v4. Conservarlo además del guardado local. Los proyectos v4 no son compatibles con apps anteriores.
- **Importar JSON:** admite v2/v3 mediante migración v2→v3→v4. Conserva datos válidos de IPv4, plan, gateways, nodos, enlaces y opciones; no llama a asignadores y deja IPv6 vacío al migrar. V4 valida intenciones y coherencia del plan IPv6 recibido, sin recalcularlo.
- La importación es atómica: archivo inválido no reemplaza el estado. Los textos CLI importados solo se conservan si coinciden con su regeneración validada. No se evalúan instrucciones del JSON.
- Descargar configuraciones, SVG o CSV produce archivos; nunca conecta con routers. El CSV del plan actual sigue siendo IPv4; IPv6 está incluido en JSON v4.

## 8. Pruebas, seguridad y evidencia

Seguir [docs/pruebas.md](pruebas.md) para instalar Playwright/Chromium y ejecutar:

```bash
python tests/test_corte3.py
```

El runner abre/cierra HTTP local y contextos limpios, imprime C01–C20 y el porcentaje real. Detener la publicación si devuelve no cero. El 20/20 registrado es del conjunto ejecutado, no certificación de toda la app ni hardware. No volver a generar la captura 09 sin una tarea autorizada para actualizar su procedencia.

Antes de compartir: usar datos ficticios, revisar nombres/IP/configuraciones, no introducir secretos y conservar `<CAMBIAR_EN_PRODUCCION>` como marcador externo. Consultar [seguridad](seguridad.md) y [políticas IA](politicas-ia.md). La [captura 08](capturas/08-ciberdefensa.png) muestra una IPv4 rechazada conservando el último resultado válido.

| Evidencia | Lectura correcta |
| --- | --- |
| [06 Fortinet](capturas/06-config-fortinet.png) | Propuesta real de un nodo Firewall; no prueba de forwarding |
| [07 MikroTik](capturas/07-config-mikrotik.png) | Propuesta RouterOS real; no configuración ejecutada |
| [08 Ciberdefensa](capturas/08-ciberdefensa.png) | Rechazo de entrada inválida; no auditoría integral |
| [09 Pruebas](capturas/09-pruebas.png) | 20/20 de la ejecución identificada; ratificado en main actual |
| [10 Aplicación](capturas/10-app-final.png) | Resumen funcional con datos de laboratorio y estimaciones |

Pendientes: validación física/modelos/firmware, aclaración docente de comandos IPv6, pools DHCP y reservas editables, invalidación histórica de sedes y desbordamientos ajenos a las pantallas verificadas. No se aplicaron configuraciones sobre infraestructura real en esta entrega.
