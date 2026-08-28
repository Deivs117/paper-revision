# Auditoría de redundancia final — antes de compilar/enviar (2026-08-31) — PENDIENTE

**Estado: 🔲 Programada, NO ejecutar todavía.** Este es explícitamente el ÚLTIMO paso antes de la
compilación/envío final — correrlo demasiado pronto significa tener que repetirlo cuando lleguen
R2-02/R3-01/R3-02/R3-04/R3-05 (el equipo confirmó datos listos el domingo, integración el lunes) y el resto de
`R02-01-05`/`R3-06`. Ejecutar solo cuando **todas** las filas de `PROGRESS.md` relevantes a esta ronda estén en
`drafted` o mejor.

**Origen:** pregunta directa del autor — "hay forma de seguir auditando estas correcciones para que no sean
contraproducentes en nuestra labor de sintetizar el paper", citando el comentario original del Revisor 2 que
`R2-01` ya resolvió una vez.

## 0. Comentario textual del Revisor 2 (ancla, igual que R2-01 lo usó)

> "However the paper is overly verbose with repeated content, and several minor supplements are needed: Stream
> the whole manuscript heavily: Cut repetitive descriptions, duplicated neural raster plots and identical
> stability curves between simulation and physical tests; merge unified metric definitions to avoid restating
> multiple times, and shorten the symbolic warehouse simulation section."

`R2-01` (Sebas) ya lo resolvió una vez de forma completa y documentada (`PROGRESS.md`, 4 rondas de pasada
completa sobre las 6 secciones, `results.tex` 9668→8524 palabras). **Este documento no repite ese trabajo** —
audita específicamente si algo de lo añadido *después* de que `R2-01` cerró (commit `51c07b4`) reintrodujo el
mismo problema.

## 1. Por qué esto es un riesgo real, no solo precaución

Desde que `R2-01` cerró, se añadió contenido nuevo en cada una de estas filas — cada una individualmente
justificada, pero el efecto acumulado es exactamente el tipo de crecimiento que hay que vigilar:

| Fila | Qué añadió |
|---|---|
| `N-01` | Caption + prosa nueva para la rejilla fusionada de simulación, con disclosure de vectorización del panel Obstacle |
| `N-04` | Reescritura de 5 párrafos (M-01–M-04) |
| `N-05` | Párrafo + tabla nueva de energía de transición + consumo por modo (R2-04) |
| `N-06`/`N-07`/`N-08` | Correcciones de imagen (sin prosa nueva significativa, pero confirmar) |
| `C-07` | Limpieza editorial — en teoría reduce, confirmar que no añadió neto |
| `R3-06` (en curso) | **Tabla comparativa nueva + reformulación de prosa en `introduction.tex`** — el más grande de los pendientes, alto riesgo si no se coordina bien con el párrafo ya existente de la línea 9 |
| `R2-02`/`R3-01`/`R3-02`/`R3-04`/`R3-05` (por integrar, datos llegan el domingo) | Contenido completamente nuevo — no existía antes, no hay redundancia previa que auditar, pero sí hay que revisar que la integración no *cree* redundancia con lo ya existente |

`scripts/check_word_growth.sh` (nuevo, wired en `scripts/push_to_overleaf.sh`) da visibilidad continua del
conteo de palabras por sección en cada push — **no reemplaza esta auditoría**, solo la hace más fácil de
priorizar (si una sección creció mucho más de lo esperado para el contenido que se supone que se le añadió, es
la primera candidata a releer aquí).

## 2. Hallazgo ya identificado que esta auditoría debe re-visitar explícitamente

**Grupo B del informe `figure-redundancy-audit.pdf`** (ver `intake/processed/figure-redundancy-audit-triage.md`)
ya señaló esto y se dejó como backlog explícito: los pares de rasters `NEU_IMU`/`NEU_IMU2` (simulación) vs. sus
versiones `_real` (físico) tienen layout casi idéntico. **Esto ahora es más relevante que cuando se escribió el
backlog** — desde entonces, `R02-01-05` vectorizó y pulió las versiones de simulación (`N-06`/`N-08`), así que
hoy ambos lados del par están más pulidos y visualmente más parecidos entre sí de lo que estaban antes. El
Revisor 2 nombra literalmente "duplicated neural raster plots... between simulation and physical tests" — esta
auditoría debe decidir con criterio fresco si, ahora que ambos lados están terminados, siguen siendo pares
legítimos de validación sim→real (la lectura original) o si conviene fusionar/condensar alguno, en vez de asumir
la conclusión de hace varios días sin revisarla.

## 3. Método (mismo rigor que R2-01, no un vistazo rápido)

1. Releer las 6 secciones completas (`introduction.tex`, `methodology.tex`, `results.tex`, `conclusions.tex`,
   `preamble.tex`, `closing.tex`) — no solo los diffs desde `R2-01`, porque una restatement puede ocurrir entre
   texto viejo y texto nuevo, no solo dentro de lo nuevo.
2. Para cada afirmación/definición de métrica que aparece en más de un lugar, aplicar el mismo criterio que
   `R2-01` ya estableció (ver su fila en `PROGRESS.md` para el patrón: mención de establecimiento + referencia
   cruzada de las repeticiones, no restatement completo).
3. Revisar específicamente el §2 de este documento (rasters sim/físico) con ojos frescos.
4. Revisar que la tabla nueva de `R3-06` (`tab:action_selection_comparison`) no reintroduzca en tabla lo que el
   párrafo de la línea 9 de `introduction.tex` ya dice en prosa — deben complementarse, no decir lo mismo dos
   veces (el plan de `R3-06` ya lo advierte explícitamente, confirmar que se ejecutó así).
5. Revisar la sección de simulación del "warehouse" (Referee 2 la nombra explícitamente, ya acortada por
   `R2-01`) — confirmar que ninguna fila nueva le añadió prosa de vuelta.
6. Correr `scripts/check_word_growth.sh` como punto de partida para priorizar qué secciones releer primero, no
   como sustituto de la relectura.

## 4. Al ejecutar

- Cualquier condensación encontrada sigue el mismo patrón que `R2-01`: un patch por hallazgo, wrapped en
  `\revblue{}` solo si cambia contenido (una fusión de párrafos sí cuenta, un ajuste de una palabra no).
- Registrar como fila(s) `C-xx` en `PROGRESS.md` (`scripts/next_id.sh C`), `Category: Escritura`, referenciando
  este documento.
- `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.
- Mover este documento a `intake/processed/` solo cuando esas filas `C-xx` lleguen a `applied` — no antes.
