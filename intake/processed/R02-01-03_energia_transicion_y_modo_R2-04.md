# R02-01-03 — Energía de transición morfológica + tabla de consumo por modo (R2-04)

**Estado: ✅ CERRADO (2026-08-27, N-05, commit `b104186`).** Ambas figuras/tabla ejecutadas, promovidas y en
`results.tex`. Único seguimiento abierto: la fila Omnidireccional de la tabla es un placeholder N=1 — ver §5.

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` §9.7/§9.9 (ambos eliminados tras atomizarse, ver
`intake/R02-01_INDEX.md`).

## 1. Contexto — dos métricas distintas, no confundir

- **Energía de *transición*** (este documento §2): cuánto cuesta, en Joules, el evento breve de cambiar de modo.
- **Consumo *en estado estable*** (este documento §3, R2-04 del revisor): cuánta potencia media consume el robot
  mientras *opera* en cada uno de los 3 modos, excluyendo las ventanas de transición.

## 2. Energía de transición morfológica (`FigReal_Morphological_Transition_Energy.png`)

**Qué cambió respecto a la versión rechazada:** el método pasó de "un pico de potencia inferido, sin verificar
contra ningún evento real" a "35 transiciones de modo reales, detectadas por comando estructural (`robot_cmd` ∈
{`c`,`z`,`x`}, filtrando las teclas direccionales), integradas en la ventana mecánica ya precalibrada y publicada
(2.92s para `z`=Diferencial, 1.56s para `c`=Cuadrúpedo — mismos valores publicados en el caption de
`FigReal_Terrain_Latencies_4Panels`)". **Causa raíz del descarte de la Opción A original:** la columna `mode` de
`Test_current_integrated_*/neural_metrics.csv` nunca cambia (siempre `'C'`) en los 5 registros — no ubica
transiciones reales; el autor aportó la lógica original de detección.

**Derivación de potencia:** `|current_A| × 7.2V` (paquete NiMH 3300mAh fijo, confirmado fiable por el equipo de
hardware) — **no** las columnas `power_W`/`voltage_V` originales (rotas, magnitud implausible ~1e-4 W).

**Resultados finales (N reales, no inferidos):**

| Dirección | N | Energía (media ± SD) |
|---|---|---|
| Quadrupedal → Differential Mobile (ventana 2.92s) | 16 | 5.06 ± 2.93 J |
| Differential Mobile → Quadrupedal (ventana 1.56s) | 19 | 4.13 ± 1.19 J |

Diferencia entre direcciones **no estadísticamente significativa** (Welch t≈1.18). La SD es mayor en
Quad→Diff, lo opuesto de lo que la prosa antigua (narrativa causal "river-pebble terrain") afirmaba — se
reemplazó por una observación sin atribución causal no verificada.

**Código:** `experiments/_plotting/builders/energy_transition.py` (reescrito por completo, no un ajuste menor).

## 3. Tabla de consumo por modo — R2-04 (`tab:mode_steady_state_energy`)

**Decisión del autor (2026-08-27):** tabla, no figura — un bar chart de 3 categorías (una N=1 y temporal) no es
muy diciente, y una tabla es mucho más barata de actualizar cuando lleguen los datos reales de Omnidireccional
(una fila, no una regeneración de figura).

**Método:** mismo `robot_cmd` estructural. Para cada segmento donde el modo activo se mantiene constante, se
excluye la ventana de acoplamiento electromecánico precalibrada desde el inicio del segmento (2.92s/1.56s; sin
ventana calibrada para `x`, usa el segmento completo) y se promedia potencia = `|current_A| × 7.2V` sobre el
resto.

**Resultado (2026-08-27):**

| Modo | N segmentos | Potencia media ± SD |
|---|---|---|
| Quadrupedal (C) | 20 | 1.94 ± 1.77 W |
| Differential Mobile (H) | 20 | 1.36 ± 0.98 W |
| Omnidireccional (X) | **1** (preliminar, sin réplica) | 5.71 W |

C vs. H no es estadísticamente significativo (Welch t≈1.26). Los 20 segmentos C/H mezclan condiciones físicas
distintas (piso plano, rampa, ensayo estático) — parte de la varianza intra-modo refleja esa heterogeneidad, no
solo ruido de medición.

**Código:** `experiments/R2-04-mode-energy/scripts/build_mode_energy.py`.

## 4. `sections/results.tex` — cambios aplicados

- Figura promovida (`--force`, mismo nombre) con caption reescrita: N reales por dirección, método de derivación
  de potencia, no-significancia estadística.
- Párrafo de energía (antes `results.tex:934`) reescrito con los valores reales y sin la narrativa causal no
  verificada.
- Tabla `tab:mode_steady_state_energy` insertada tras el párrafo de energía, mismo estilo `tabularx` que
  `tab:consolidated_physical_metrics`, con nota destacada de que Omnidireccional es preliminar (N=1).
- Todo envuelto en `\revblue{}`.

## 5. Seguimiento abierto (no bloquea el cierre de este bloque)

**La fila Omnidireccional de `tab:mode_steady_state_energy` es un placeholder N=1.** El equipo de hardware
confirmó (2026-08-27, verbalmente) que viene una campaña de pruebas dedicada para este modo. **Cuando lleguen
los datos:** re-correr `experiments/R2-04-mode-energy/scripts/build_mode_energy.py` contra la(s) carpeta(s)
nueva(s) de `experiments/real/` — la fila de X se actualiza (media±SD/N), nada más del pipeline cambia (edición
de una fila, no una tarea nueva). **Este seguimiento se rastrea únicamente en `PROGRESS.md` (fila `R2-04`,
estado `drafted`, no `applied` a propósito) y en `experiments/R2-04-mode-energy/README.md`** — no se crea un
documento `intake/pending/` aparte para esto porque no es una tarea ejecutable hoy (bloqueada por datos externos
aún no recolectados), y esos dos archivos ya son la fuente de verdad única para cuándo/cómo actuar.

## 6. Trazabilidad

- Patch: `patches/n-05-transition-energy-redaction.tex`
- `PROGRESS.md`: fila `N-05` → `applied`; fila `R2-04` → `drafted` (por diseño, ver §5)
- Commit: `b104186` (patch: N-05 transition-energy redaction + R2-04 steady-state power table)
