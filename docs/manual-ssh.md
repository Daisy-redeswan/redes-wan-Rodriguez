# Manual de consola SSH

## Manual integrado y consultas vigentes del PR #11

El botón **Manual de consola SSH** abre un diálogo dentro de WAN Architect, disponible en ES/EN y sin iniciar Python, abrir Markdown ni consultar internet. Esta página conserva el detalle de instalación y seguridad de la conexión real.

La simulación exige seleccionar un equipo; `help` funciona también sin selección y lista únicamente comandos de la marca. Se aceptan espacios repetidos y mayúsculas en comandos de lectura, sin cambiar las reglas del SSH real. Las consultas de configuración muestran el texto vigente guardado o una propuesta actual calculada sin guardarla; no solicitan generación previa en otro módulo. El rótulo SIMULACIÓN identifica siempre que no es una sesión ni un running-config real. Los cores muestran además interfaces Vlan/Vlanif del plan. Comandos ajenos o de escritura no se interpretan ni ejecutan.

## Dos modalidades sin confusión

**Simulación** funciona en WAN_v4.html sin Python, internet o acceso a dispositivos. **Conexión real** requiere iniciar el [servicio opcional](../ssh_service/README.md) y abrir la aplicación por su HTTP local. Ninguna selección de equipo, simulación, generación, copia o limpieza aplica configuraciones.

El menú tiene 14 módulos: Consola SSH se añade al final; los índices anteriores de IPv6 y fabricantes se conservan. Español es predeterminado, con English disponible. Cambiar idioma, pestaña o módulo cierra una sesión real para evitar terminales ocultas; las credenciales no se restauran.

## Confirmar sedes y VLAN

Confirmar una ficha válida muestra **Sede confirmada**, resumen y **Editar sede**, con campos bloqueados contra cambios accidentales. Editar recupera los valores; confirmar sin cambios conserva inventario, redes, aprobación y dependencias. El indicador opcional `sites[].confirmed` se guarda en v4; un proyecto antiguo sin él permanece editable, sin inferir confirmación.

VLAN automática vacía muestra **Asignación automática pendiente** antes de calcular y la subred efectiva después. El pool propio de la sede tiene prioridad sobre el predeterminado; un CIDR manual debe pertenecer a ese pool. No se cambia una red manual ni se amplía un bloque automáticamente. Ante insuficiencia se muestran sede, VLAN, bloque, hosts, crecimiento, reservas y demanda. Solo se sugiere un prefijo mínimo de capacidad cuando se puede calcular para un pool automático dedicado; no sustituye autorización ni garantiza una ubicación concreta.

Un error conserva el último estado/plan y lo escrito, muestra pendiente y enfoca un campo de corrección. No se generan topología/CLI dependientes mientras haya datos pendientes. Calculadora y conexión SSH manual siguen accesibles; la simulación avisa cuando falta un plan confirmado.

## Simulación paso a paso

1. Seleccionar un equipo de la topología y revisar nombre, marca, rol e interfaces.
2. Escribir `help` y Enter para conocer **la lista cerrada soportada**.
3. Consultar la propuesta de configuración actual del proyecto. Se usa la CLI vigente guardada o el adaptador real en modo de solo lectura; si el proyecto/rol no es compatible se explica el bloqueo. No representa el running-config de un equipo físico.
4. Consultar interfaces/VLAN del proyecto o inventario de redes. Este último no representa rutas aprendidas, ping, conectividad ni estado operativo real.
5. **Limpiar consola** borra el buffer; **Reiniciar simulación** limpia entrada/buffer y confirma la acción. Reemplazar el proyecto limpia la selección y el historial educativo anterior.

| Fabricante | Comandos admitidos, además de help/? |
| --- | --- |
| Cisco | `show running-config`, `show ip interface brief`, `show vlan brief`, `show ip route` |
| Huawei | `display current-configuration`, `display ip interface brief`, `display vlan`, `display ip routing-table` |
| Fortinet | `show`, `show system interface`, `get router info routing-table all` |
| MikroTik | `/export`, `/ip address print`, `/interface print`, `/ip route print` |

Otro comando muestra **Comando no disponible en el simulador**. No se emulan configuración de protocolos, conectividad, cambios de NOS ni una sesión física. Los comandos y el texto CLI permanecen sin traducción; la interfaz/avisos son bilingües.

## Conexión real paso a paso

1. Seguir la instalación Windows/Linux del [README del servicio](../ssh_service/README.md). Configurar destinos autorizados y verificar su host key fuera de banda.
2. Abrir `http://127.0.0.1:8765/WAN_v4.html` o el puerto configurado. Con file:// o un servidor estático distinto se indica servicio no disponible; no se escanean puertos ni se eluden restricciones de origen.
3. Seleccionar **Conexión real**. Se puede elegir nodo o conexión manual; esta última no requiere VLSM.
4. Introducir IP/hostname autorizado, puerto (22 predeterminado) y usuario. Solo se completa automáticamente una IP explícita asociada a Gestión; gateway, SVI, WAN o endpoint no se presumen administración. Verificarla con el responsable del equipo.
5. Elegir contraseña o clave privada y frase opcional. Son entradas de sesión, no campos del proyecto. Confirmar autorización y pulsar **Conectar**.
6. **Conectando** no significa autenticado; **Conectado** aparece solo tras autenticación y apertura de PTY. Errores distinguen autenticación, red, confianza de host, destino o autorización local.
7. Escribir manualmente en xterm; entrada/salida, Unicode, secuencias de terminal, Ctrl+C y resize se transportan por SSH. La paginación y comandos disponibles los determina el equipo real. La aplicación no los ejecuta sola.
8. **Limpiar consola** limpia solo la pantalla web, sin enviar clear. **Desconectar** cierra la sesión. Reconectar requiere nueva autenticación; las credenciales se vacían y no se guardan en JSON, localStorage ni logs.

No pegar configuraciones completas sin autorización explícita del administrador. El shell remoto tiene los permisos del usuario autenticado: esta herramienta no decide si un comando manual es adecuado.

## Solución de problemas

| Mensaje | Comprobación segura |
| --- | --- |
| Servicio no disponible | Iniciar Python con dependencias opcionales y usar su URL/puerto, no file:// |
| Destino no autorizado | Añadir host, puerto y todas sus IP autorizadas al config local; reiniciar |
| Clave de host desconocida/modificada | Comparar huella por canal independiente y seguir registro explícito; no desactivar validación |
| Error de autenticación | Verificar cuenta y método con el administrador; no publicar credenciales |
| Error de red | Revisar ruta, puerto, firewall y servicio SSH; no asumir que la app creó conectividad/VPN |
| Sesión local no autorizada | Recargar la página del servicio propio; no usar un iframe u otro origen |
| Demasiadas sesiones | Cerrar sesiones propias; el límite incluye intentos conectando |
| Sesión finalizada | Puede ser cierre remoto, cambio de vista, inactividad, ACK ausente o desconexión; reconectar expresamente |

## Límites declarados

Las pruebas usan SSH real en loopback y una terminal de eco controlada, sin equipos físicos. No certifican Cisco/Huawei/Fortinet/MikroTik, algoritmos antiguos, Windows ejecutado, conectividad de una WAN ni auditoría completa. No se habilitan algoritmos inseguros, NAT, proxy abierto o acceso desde la LAN. La instalación de paquetes necesita acceso a sus fuentes o un repositorio local; una vez instalados, los recursos de ejecución son locales.
