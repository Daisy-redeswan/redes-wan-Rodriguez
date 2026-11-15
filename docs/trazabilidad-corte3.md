# Trazabilidad del Corte 3

Edición 2026-11-15, main `1b46af32c8217a1f9bcea686151b1f070ac38352`. Fuente principal: [Guía Docente.html](<requisitos/Guía Docente.html>) v4.0. [Auditoría completa de ambos cortes](auditoria-entrega-final.md): requisitos literales, hallazgos, 19 rutas, diez capturas y pendientes.

## Rúbrica oficial de Corte 3

| Criterio exacto | Peso | Implementación / prueba registrada | Evidencia y documento | Estado / pendiente |
| --- | --- | --- | --- | --- |
| Config Fortinet + 4.ª marca | 25% | C14–C16/K/F/L; 06/07 actuales | README.md; WAN_v4.html; docs/capturas/ | Cumple: Cumplimiento documental/local verificado; plataformas físicas no certificadas. |
| Ciberdefensa integrada | 15% | validadores, warnings(), política y rechazo real 08 | README.md; WAN_v4.html; docs/capturas/ | Cumple: Cumplimiento documental/local verificado; plataformas físicas no certificadas. |
| Pruebas y % de confianza | 20% | reportes 114+26 por hashes; 09 síntesis, docspruebas | docs/pruebas.md; docs/capturas/ | Parcial: Falta ejecutar ante el docente. |
| Documento + manual | 15% | PDF reconstruido completo, manual actual y diez figuras | docs/informe-corte3.pdf; docs/manual.md | Cumple: Cumplimiento documental/local verificado; plataformas físicas no certificadas. |
| Sustentación | 15% | No hay registro de defensa en vivo | README.md; WAN_v4.html; docs/capturas/ | No verificable: La defensa y comprensión personal no se pueden certificar documentalmente. |
| Repositorio y versiones | 10% | main 1b46af3, PR11 merged, rama preservada, 10 actual | README.md; WAN_v4.html; docs/capturas/ | Cumple: Cumplimiento documental/local verificado; plataformas físicas no certificadas. |

Los pesos suman 100% y no son nota otorgada ni cobertura de tests. **140/140 = 100% del conjunto ejecutado** procede de 114 UI + 26 SSH, dos reportes reales previos al squash verificados por hashes; no se repitieron en esta tarea. 09 identifica la síntesis documental; ejecutar suites en vivo permanece pendiente.

## Transversales y límites

- V4, migración v2/v3 sin reasignación; almacenamiento v4 con fallback no destructivo. IPv4 privado por sede/tránsito y CIDR manual/automático; gateway independiente. Calculadora pública/privada; planificación pública automática no demostrada.
- IPv6 ULA /48–/56–/64 separado; sin CLI IPv6 de fabricantes, pendiente aclaración docente.
- Cisco/Huawei/Fortinet/MikroTik consumen plan/interfaces reales; catálogo doce fichas, AP conservados sin CLI. Ver [matriz](matriz-fabricantes.md). Compatibilidad física no validada.
- Manual, siete políticas y seguridad actualizados con SSH opcional y datos efímeros; informes de ambos cortes y capturas correctas.
- 2FA y comprensión/defensa en vivo no verificables; fechas académicas no inventadas.

## Antecedentes conservados

La [trazabilidad anterior](https://github.com/Daisy-redeswan/redes-wan-Rodriguez/blob/1b46af32c8217a1f9bcea686151b1f070ac38352/docs/trazabilidad-corte3.md) conserva 31/50/99 y referencias de sus versiones. Ya no se presentan como resultados actuales ni se suman al 140. Esta edición corrige evidencia 09 histórica, capturas pendientes y descripción de fabricantes/SSH sin modificar código.
