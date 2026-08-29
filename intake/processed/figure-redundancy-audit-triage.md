# Triage de `figure-redundancy-audit.pdf`

**Estado: ✅ CERRADO (2026-08-27).** Informe de 11 páginas leído completo y decidido por grupo. Sin fila de
`PROGRESS.md` propia — cada grupo se resolvió por su cuenta (ver abajo).

**Origen del archivo:** commit `a5e88d3` de un teammate, colocado originalmente en una carpeta `reports/` en la
raíz del repo (fuera del pipeline de `intake/`) — reubicado a `intake/pending/` el 2026-08-27 (ver
`CLAUDE.md`/`README.md` §8.1, regla añadida ese mismo día para que esto no se repita).

## Grupo A — "Los mismos 3 paneles, dibujados 5 veces" (máxima prioridad según el informe)

**❌ Descartado.** Proponía cortar por completo las figuras físicas de Appetitive y Obstacle por redundantes,
dejando solo Aversive y Complex como representativas. Esto conflictúa con una decisión ya ejecutada y publicada:
N-02/N-03 resolvieron la misma redundancia fusionando el panel del ganglio basal dentro del panel RMS en los 4
escenarios, sin cortar ninguno (ver `intake/processed/R02-01-02_fisico_regeneracion_N02-N05.md`). Reabrir esto
significaría deshacer trabajo ya sincronizado a Overleaf por una alternativa que el autor nunca pidió — no se
persigue.

## Grupo B — pares simulación/físico (rasters de terreno rugoso/inclinado)

**🔲 Backlog explícito para la próxima ronda de revisión, no esta.** El informe marca 2 pares (`NEU_IMU`/
`NEU_IMU2`, sim y físico) como "vale la pena mirar dos veces" — layout casi idéntico entre terreno rugoso e
inclinado, posible candidato a fusionar en una figura multi-panel. Es la misma familia de figuras que
`intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md` ya va a tocar (F-01/F-04, vectorización pendiente)
— **no se adopta ahora** porque cambiar cuántas figuras hay ahí mismo agrega alcance nuevo a 4 días del
deadline (2026-08-31). Si se retoma en una ronda futura, empezar por releer ese documento antes de tocar nada.

## Grupo C — "3 montajes de 6 fotos" (format repetition)

**✅ Convertido en tarea ejecutable.** El autor pidió acotar la revisión a este grupo específicamente y
verificar con criterio, no solo por sospecha. Resultado tras inspeccionar cada una de las 18 fotos y cruzarlas
contra qué frames tienen referencia individual en la prosa: **2 de los 3 montajes sí tenían relleno real**
(`D1-D6` y `E1-E6`, cada uno con solo 0-1 de 6 frames citados individualmente), el tercero (`Prueba_Terreno_
Parte_1-6`) está completamente justificado (los 6 frames mapean 1:1 a una tabla dedicada) y no se toca. Plan de
ejecución completo, con selección de frames verificada visualmente y captions redactadas, en
`intake/pending/R02-01-07_recorte_montajes_fotograficos.md`.

## "Revisado, sin acción" + inventario completo (resto del informe)

Confirma 6 pares de figuras que ya se sabía que eran contenido distinto (nada nuevo que decidir), más una tabla
de referencia de las 91 imágenes del paper — quedó como contexto de esta triage, no genera ninguna acción
adicional.
