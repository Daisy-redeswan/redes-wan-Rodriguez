# redes-wan-Rodriguez
# Herramienta de Redes WAN — WAN Architect (trabajo individual)

**Materia:** Interconexión de Redes WAN
**Repositorio:** [https://github.com/Daisy-redeswan/redes-wan-Rodriguez.git](https://github.com/Daisy-redeswan/redes-wan-Rodriguez.git)

## Qué hace esta herramienta

WAN Architect permite planificar una red por sedes, calcular subredes IPv4 y representar su topología. Genera configuraciones para equipos Cisco y Huawei a partir de los datos del proyecto.

La aplicación funciona en un único archivo HTML, sin conexión a Internet, servidor ni archivos externos.

## Funciones

- **Subnetting / IP Planning:** cálculo IPv4, clasificación de direcciones públicas y privadas, planificación VLSM y asignación de VLAN. IPv6 está pendiente.
- **Carga y edición de topología:** creación automática y manual de dispositivos y enlaces, incluyendo nodos ISP. Permite cargar una imagen como referencia; su interpretación automática está pendiente.
- **Configuraciones Cisco:** generación de comandos para routers y switches, según las características del proyecto.
- **Configuraciones Huawei:** generación de comandos VRP y comparación con Cisco. Está pendiente corregir el filtro del módulo Huawei para que también muestre los equipos creados automáticamente.
- **Fortinet y MikroTik:** pendientes de implementación para el Corte 3.
- **Ciberdefensa y uso de IA:** validación de entradas, tratamiento seguro del contenido mostrado, políticas visibles y contraseñas representadas mediante marcadores. Falta verificar y publicar su documentación en `docs/politicas-ia.md`.
- **Gestión del proyecto:** guardado local, importación y exportación JSON, exportación de configuraciones y topología SVG.

## Cómo ejecutarla

1. Descargar el repositorio o el archivo de la aplicación.
2. Abrir `WAN.html` directamente en un navegador actualizado. Si se conserva el nombre `Versión3.html`, abrir ese archivo.
3. Registrar los datos del proyecto y revisar el inventario, las VLAN y el direccionamiento.
4. Generar la topología y consultar las configuraciones Cisco y Huawei.
5. Guardar o exportar el proyecto para conservar una copia.

No requiere instalación ni conexión a Internet. Los comandos generados deben revisarse según el modelo y la versión del sistema operativo del equipo antes de aplicarlos.

## Pruebas y % de confianza (Corte 3)

## Documentos

Documentación prevista, pendiente de verificar o publicar en el repositorio:

- `docs/informe-corte2.pdf`
- `docs/manual.md`
- `docs/seguridad.md`
- `docs/politicas-ia.md`
- `docs/pruebas.md`

## Capturas (evidencias)

Carpeta prevista: `docs/capturas/`.

Las capturas deben obtenerse de la aplicación y de las pruebas realizadas. Está pendiente verificar la existencia de las evidencias desde `01-subnetting.png` hasta `10-app-final.png`.

## Autoevaluación

| Criterio                                      | ¿Cumplido?                                                  | Evidencia prevista                             |
| --------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------- |
| Subnetting funciona                           | Sí, para IPv4                                               | `01-subnetting.png`                            |
| Carga de topología                            | Sí                                                          | `02-topologia.png`                             |
| Config Cisco y Huawei                         | No, pendiente completar el funcionamiento del módulo Huawei | `03-config-cisco.png` / `04-config-huawei.png` |
| Config Fortinet y MikroTik (C3)               | No                                                          |                                                |
| Ciberdefensa documentada en `politicas-ia.md` | No                                                          |                                                |
| Pruebas con % de confianza (C3)               | No                                                          |                                                |

