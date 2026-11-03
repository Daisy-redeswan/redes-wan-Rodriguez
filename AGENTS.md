Actúa como WAN Architect Engineering Lead y trabaja sobre el repositorio
Daisy-redeswan/redes-wan-Rodriguez.

Esta es una tarea de documentación local. No modifiques GitHub, no abras
pull requests y no realices commit ni push.

Objetivo:

Crear en una rama local de documentación los archivos aprobados para
orientar el trabajo futuro de Codex sobre WAN Architect.

Procedimiento obligatorio:

1. Confirma la URL del remoto, la rama actual, el último commit local y
   remoto y el estado del árbol de trabajo.
2. Ejecuta una actualización no destructiva de las referencias remotas.
3. No descartes, sobrescribas ni ocultes cambios existentes.
4. Si existen cambios locales que puedan entrar en conflicto, detente y
   repórtalos antes de crear la rama.
5. Parte de la versión más reciente confirmada de `main`.
6. Crea o cambia a la rama local:
   `docs/instrucciones-codex`
7. No publiques la rama.
8. Crea únicamente los archivos aprobados:
   - `AGENTS.md`
   - `docs/estado-proyecto.md`
   - `docs/trazabilidad-corte3.md`
   - `docs/matriz-fabricantes.md`
9. Usa exactamente el contenido aprobado para `AGENTS.md`.
10. En los otros tres documentos crea la estructura mínima aprobada.
    Distingue siempre:
    - requisito oficial;
    - confirmado por inspección de código;
    - confirmado por prueba ejecutada;
    - supuesto;
    - pendiente;
    - bloqueado.
11. Consulta como fuentes:
    - `docs/requisitos/Guía Docente.html`
    - `WAN_v4.html`
    - `docs/requisitos/Arquitectura_Agente_WAN_Architect.docx`
    - `docs/requisitos/Correcciones Pendientes.txt`
    - `docs/requisitos/Instrucciones de Código.txt`
12. No copies íntegramente esos documentos en los nuevos archivos.
    Referéncialos por su ruta exacta.
13. No inventes pruebas, resultados, capturas, versiones de fabricante,
    evidencias, fechas de ejecución ni porcentajes.
14. No modifiques bajo ninguna circunstancia:
    - `WAN_v4.html`
    - los cuatro archivos de `docs/requisitos/`
    - documentos o capturas existentes
15. No cambies el esquema JSON ni ningún archivo de la aplicación.
16. No ejecutes configuraciones de red.
17. Revisa el diff final y confirma que contiene solamente los cuatro
    archivos de documentación autorizados.
18. No uses `git add`, no hagas commit y no hagas push.

Al terminar, entrega:

- Rama local utilizada.
- Commit base de `main`.
- Archivos creados.
- Resumen de su contenido.
- Resultado de `git status --short --branch`.
- Resultado resumido de `git diff --check`.
- Confirmación de que `WAN_v4.html` no cambió.
- Confirmación de que no realizaste commit, push ni publicación.
- Cualquier contradicción o información que no haya podido verificarse.

Detente después del informe y espera autorización expresa antes de
preparar o crear un commit.