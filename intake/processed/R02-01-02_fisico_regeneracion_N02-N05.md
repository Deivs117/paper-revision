# R02-01-02 — Regeneración de figuras físicas (N-02–N-05): traducción, fusiones, promoción

**Estado: ✅ CERRADO (2026-08-27).** Las 12 figuras físicas aprobadas + la fusión del clasificador están
promovidas a `assets/` y `sections/results.tex` está actualizado. Sin acción pendiente.

**Origen:** `intake/pending/R02-01_metric_and_figure_audit.md` (§3 F-01/F-03/F-05/F-06, §8, §9.1–9.6) +
`intake/pending/R02-01_data_traceability_and_plotting_plan.md` (§1.2, §2 Grupos B/D de vectorización) — ambos
eliminados tras atomizarse (ver `intake/R02-01_INDEX.md`).

## 1. Alcance de este bloque

Todo lo que tocó `experiments/N-02-physical-figure-regeneration/` y llegó a `assets/`:

- **F-01 (instancias físicas)** — traducción "March Decision Module"→"Gait Decision Module" y
  "Auxiliar"→"Auxiliary" en `NEU_EST_UNIG_real.png`, `NEU_EST_MUL_real.png`, `NEU_IMU_real.png`,
  `NEU_IMU2_real.png`. Vectorizadas por intensidad de píxel (método generalizado a layouts multi-columna de
  4/8/12 paneles).
- **F-03** — fusión `fig5_classifier_comparison.png` + `fig6_computational_cost.png` → panel único
  `fig_classifier_tradeoff_fused.png` (1×3: métricas / latencia / tamaño de modelo). Sin notebook de
  entrenamiento original → vectorizado con extracción directa de color de píxel en Python (no WebPlotDigitizer
  por navegador — refinamiento de D-11 encontrado en la práctica). El clasificador es único (no hay variante
  "física" separada de "simulación" — mismo modelo offline), así que este bloque cierra F-03 para **ambos**
  contextos, no solo el físico.
- **F-05** — notación $N_0/N_1/N_2$ añadida a `GRAPH_IMU_real.png`/`GRAPH_IMU2_real.png` (resultaron ser heatmaps
  categóricos, no series continuas — caso distinto de F-04, que sigue pendiente solo para la versión de
  simulación, ver `R02-01-05`).
- **F-06** — reescalado del eje Y de `fig4_architecture_ablation.png` a 0.65–0.80 (sin vectorizar — los 4 valores
  de F1 ya estaban en prosa, `results.tex:598`).
- **`fig1_confusion_matrix.png`** — regenerado con estilo serif consistente (M-05 ya confirmaba sus 4 valores
  correctos, sin cambio de contenido).
- **`FigReal_Terrain_Latencies_4Panels.png`** — vectorizada (Grupo D de calibración compartida, Informe 2 §2).
- **Eliminación de `*_Real_Plot_2_Basal_Ganglia_Dynamics.png`** (12 figuras: 4 escenarios × esta figura) por
  decisión del autor, respondiendo al comentario del revisor "cut repetitive descriptions, duplicated neural
  raster plots and identical stability curves". Su contenido (firing variance) se fusionó como panel superior
  dentro de `*_Real_Plot_3` (ahora compuesto de 2 paneles: neuronal arriba + cinemático abajo, con sombreado
  rojo/azul de presencia de estímulo para Appetitive/Aversive/Complex, sin sombreado para Obstacle por ser
  estímulo no cromático). **Análisis detallado de por qué esto no debilita el argumento científico (la narrativa
  textual ya era independiente de la figura desde antes) vive en un bloque aparte, ya cerrado:**
  `intake/processed/R02-01_basal_ganglia_text_adaptation_plan.md`.
- **Tipografía:** se importaron los skills de Claude Code `matplotlib`/`scientific-visualization` a
  `.claude/skills/` (fuente serif 10/11/12pt, paleta Okabe-Ito colorblind-safe, sin grilla por defecto, 300dpi) —
  ahora es el estilo por defecto del proyecto (`experiments/_plotting/style.py`), aplica automáticamente a
  cualquier figura futura.

## 2. Vectorización — método (Grupos B y D, ya cerrados)

Herramienta: extracción directa de color de píxel en Python (no WebPlotDigitizer por navegador, D-11 refinado en
la práctica). Documentación completa por CSV en `experiments/_plotting/vectorized/README.md`.

- **Grupo B** (clasificador): `fig5`/`fig6` — cerrado.
- **Grupo D** (IMU terreno físico): `GRAPH_IMU_real`, `GRAPH_IMU2_real`, `NEU_IMU_real`, `NEU_IMU2_real`,
  `FigReal_Terrain_Latencies_4Panels` — cerrado, las 5 promovidas.

(Los Grupos A y C de calibración compartida — `fig_stability_phases.png` y las 6 figuras IMU de **simulación** —
siguen pendientes, ver `intake/pending/R02-01-05_simulacion_grupo2_vectorizacion.md`.)

## 3. Verificación numérica del clasificador (F-03)

La prosa original (`results.tex:607`) citaba SVM-RBF F1=0.900 y Random Forest F1=0.995; la extracción vectorizada
(`experiments/_plotting/vectorized/classifier_fig5.csv`) dio SVM-RBF F1≈0.857 y Random Forest F1≈0.947 — una
diferencia de ~4-5 puntos porcentuales. Las cifras de latencia (`results.tex:616`) sí coincidían casi exactamente
con la extracción (1.64 vs 1.63 µs, 23.5 vs 23.4 µs, 41.0 vs 40.7 µs, 0.54 vs 0.53 µs), apuntando a que solo el
panel (a) tenía el problema. **El autor confirmó que la extracción vectorizada es la correcta y la prosa era la
desactualizada** (mismo patrón que M-01–M-04) — `results.tex:607` corregido a F1=0.857/0.947.

## 4. `sections/results.tex` — cambios aplicados

- Promoción de las 12 figuras + fusión (`scripts/promote_figure.sh --force` para las que reemplazan nombre
  existente; sin `--force` para `fig_classifier_tradeoff_fused.png`, nombre nuevo).
- `git rm` de los 4 `*_Real_Plot_2_Basal_Ganglia_Dynamics.png` (sin referencias tras el cambio de caption) y de
  `fig5_classifier_comparison.png`/`fig6_computational_cost.png` (superseded por la fusión).
- Los 4 bloques `figure*` físicos (Appetitive/Aversive/Complex/Obstacle): subfigura `_Real_Plot_2` eliminada,
  paneles re-letrados automáticamente por `subcaption`, captions externas reescritas a mano para narrar el panel
  compuesto — texto exacto verificado en `sections/results.tex` líneas ~799, ~822, ~849, ~872.
- Reemplazo de los 2 bloques `fig5`/`fig6` por uno solo → `\label{fig:classifier_tradeoff}`; actualizadas las
  referencias en `results.tex:607` y `:616` (párrafos de prosa NO fusionados, quedan como dos párrafos separados
  citando la misma figura — decisión editorial explícita).
- Todo el texto nuevo/cambiado envuelto en `\revblue{}`.
- `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` pasaron antes de cada commit.

## 5. Trazabilidad

- Patch: `patches/n-03-physical-figure-promotion-classifier-fusion.tex`
- `PROGRESS.md`: fila `N-02` → `applied`; fila `N-03` → `applied`
- Commit: `d93adbd` (patch: N-03/N-04 physical figure promotion, F-03 classifier fusion, M-01-M-04 text redaction)
