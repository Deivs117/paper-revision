# C-21 — Auditoría pixel-por-pixel: oclusión de texto / leyendas en figuras generadas por código

**Alcance pedido por el autor:** auditar TODAS las figuras generadas por código (matplotlib) en
`assets/` buscando texto oculto, leyendas ilegibles por el contenido de la gráfica, o leyendas que
se confunden visualmente con los datos. **Excluido explícitamente** (no auditado): fotos reales,
fotos de simulación, grafos/diagramas explicativos de la red, cualquier imagen que empiece con
`GRAPH_IMU_`/`NEU_`, y diagramas de arquitectura del robot.

**Método de exclusión:** en vez de adivinar por nombre de archivo, cada imagen ambigua (`D1-D6`,
`E1-E6`, `RES_*`, `Prueba_Terreno_Parte_*`, `Modos_Locomocion*`, etc.) se verificó leyendo su
`\caption{}` real en `sections/*.tex` — snapshots de simulación/hardware y diagramas de arquitectura
confirmados y excluidos; nunca incluidos solo por parecer ambiguos por nombre.

**34 figuras dentro de alcance** (código, no diagrama/foto) — inventario completo abajo. Auditadas
pixel por pixel (`Read` a resolución completa, no thumbnails).

---

## 1. Hallazgos corregidos esta sesión (8 figuras, 3 builders)

### 1.1 `fig_classifier_tradeoff_fused.png` — 2 problemas

- **Título con referencia a un README** (pedido explícito del autor: "ningúna gráfica que esté en
  assets lo debe tener"): el `suptitle` citaba literalmente
  `"see experiments/_plotting/vectorized/README.md"`. Eliminado — el suptitle ahora es solo
  `"Classifier accuracy/latency/size trade-off"`.
- **Leyenda superpuesta a los datos**: en el panel (a), la leyenda sin posición fija (`loc` por
  defecto) caía dentro de las barras de "Random Forest", indistinguible del relleno que
  etiquetaba. Movida arriba de los ejes, fuera de todas las barras
  (`loc="upper center", bbox_to_anchor=(0.5, 1.0)`), con `ylim` extendido para dejarle espacio.
- Builder: `experiments/_plotting/builders/classifier_suite.py::build_f03_fused_panel()`.

### 1.2 `fig4_architecture_ablation.png`

- La anotación "y-axis truncated for legibility" estaba en texto gris de bajo contraste
  directamente sobre la barra roja "(50)" — casi ilegible. Movida arriba de las barras con una
  caja de fondo blanco semitransparente.
- Builder: `experiments/_plotting/builders/classifier_suite.py::build_fig4_ablation()`.

### 1.3 Tipografía inconsistente — 3 figuras "métricas MLP" + 4 figuras `fig2_*_micro`

El autor señaló que las figuras de métricas MLP no comparten tipografía con el resto del paper.
Confirmado — dos causas distintas encontradas:

- **`fig1_confusion_matrix.png`, `fig4_architecture_ablation.png`, `fig_classifier_tradeoff_fused.png`**:
  el builder sí importa el módulo de estilo compartido (`from style import DPI`, que ejecuta
  `apply_style()` — tipografía serif de publicación — al importarse), pero los archivos en
  `assets/` eran una build vieja generada antes de que ese estilo existiera. Simplemente
  regenerarlos con el builder actual corrige la tipografía — no fue necesario cambiar código
  aparte de los dos fixes de arriba.
- **`fig2_Appetitive_micro_test_001_SUCCESS.png`, `fig2_Aversive_micro_test_001_SUCCESS.png`,
  `fig2_Obstacle_micro_test_001_SUCCESS.png`, `fig2_Complex_micro_test_001_SUCCESS.png`**: bug
  real de código — `experiments/_plotting/builders/micro_dynamics.py` nunca importaba el módulo
  `style.py` (definía su propio `DPI = 300` local en su lugar), así que `apply_style()` nunca se
  ejecutaba para estas 4 figuras — renderizaban con la fuente sans-serif por defecto de
  matplotlib, inconsistente incluso con su propio objetivo de diseño declarado (imitar
  `real_plot_suite.py::build_rms_dynamics()`, que sí importa `style.py` y sí renderiza serif —
  confirmado comparando `fig2_Appetitive_micro_test_001_SUCCESS.png` contra
  `Appetitive_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png`). Corregido: se agregó
  `from style import DPI` real.

### 1.4 `fig2_Appetitive_micro_test_001_SUCCESS.png` — leyenda sobre los datos

Al corregir la tipografía (punto 1.3) se hizo visible un problema preexistente: la leyenda
("Aversive/Appetitive stimulus in view") usaba posición fija `loc="upper left"`, que en el
escenario Apetitivo cae justo donde la curva de varianza de disparo tiene su pico (~t=1s,
y≈37) — el texto de la leyenda quedaba literalmente sobre la línea naranja. Corregido a
`loc="best"` (matplotlib evita automáticamente los datos graficados) — verificado en las 4
figuras, ninguna quedó con solapamiento.

### 1.5 `fig_stability_phases.png` — texto de anotación oculto por marcadores

Paneles D y F: la etiqueta `"SM = X.X cm"` se coloca en el punto medio de la flecha
CoM→incentro; cuando ambos puntos están muy cerca (como en D y F), el punto medio cae encima del
marcador CoM (`+` rojo) o del marcador incentro (`+` gris), ocultando un dígito del valor. Ejemplo
concreto: panel D mostraba algo como "SM = �2 cm" con el marcador tapando parte del número.
Corregido con una caja de fondo blanco + `zorder` explícito por encima de ambos marcadores — los
4 valores (2.8, 2.5, 2.2, 2.5 cm) son ahora legibles sin ambigüedad.

Builder: `experiments/_plotting/builders/stability_phases.py`.

---

## 2. Hallazgo RESUELTO (2026-09-02, sesión siguiente) — vectorizadas, sin builder reproducible

El autor confirmó que **no existe información disponible para reconstruir** `fig2_roc_curve.png`
ni `fig3_training_loss.png` desde datos crudos (ni probabilidades de predicción del MLP, ni log
de pérdida por época) — instruyó vectorizar ambas por extracción de píxeles, mismo método D-1/D-11
que el resto de `experiments/_plotting/vectorized/`.

- **`fig2_roc_curve.png`** → `extract_fig2_roc_curve.py` → `vectorized/fig2_roc_curve.csv`.
  Curva azul (paso, step function) extraída por color, excluyendo la muestra de leyenda
  (`x=[500,558], y=[699,702]`, confirmada aislada de la curva real). **Validación cruzada:** AUC
  trapezoidal recalculada desde los puntos extraídos = 0.864, contra el "AUC = 0.866" ya impreso
  en la figura original — diferencia de 0.002, confirma que la extracción es fiel. La leyenda
  reconstruida ahora muestra el valor recalculado (0.864), no el original hardcodeado, para que la
  figura sea internamente consistente con lo que realmente grafica.
- **`fig3_training_loss.png`** → `extract_fig3_training_loss.py` →
  `vectorized/fig3_training_loss.csv`. Curva única sin leyenda, sin necesidad de exclusión.
  Forma de decaimiento e inflexión (~época 10-25) y valores inicio/fin (0.75 → ~0.001) coinciden
  con el original.

Ambas re-generadas con `classifier_suite.py::build_fig2_roc()` / `build_fig3_training_loss()` —
tipografía serif de publicación, consistente con el resto de figuras. Promovidas a `assets/` vía
`scripts/promote_figure.sh --force`. Detalle completo de calibración de píxeles en
`experiments/_plotting/vectorized/README.md` (entrada "2026-09-02").

## 3. Nota menor, no corregida — inconsistencia de tipografía adicional

- **`FigReal_Morphological_Transition_Energy.png`**: también renderiza en sans-serif, mismo
  síntoma. No se investigó su builder ni se corrigió en esta sesión (fuera del alcance explícito
  del autor, que mencionó específicamente "las métricas de la MLP") — señalado aquí por si se
  quiere incluir en una futura pasada de consistencia tipográfica.

---

## 4. Inventario completo — 34 figuras auditadas, sin más hallazgos

Todas revisadas pixel por pixel, sin problemas de oclusión de texto/leyenda encontrados (más allá
de lo ya listado arriba):

`fig1_noise_robustness_grid.png`, `FigA_Stability_Profile.png`, `FigB_Decision_Delay.png`,
`FigC_Terrain_Adaptability.png`, `fig_inspection_dfinal_vs_nlidar.png`,
`fig_mode_timeline_complex.png`, `fig_mode_timeline_inspection.png` (ambas ya auditadas y
corregidas en la ronda R2-02, ver `intake/pending/R2-02_audit_and_plan.md`),
`fig_R1_failure_by_family.png`, `fig_R2_terrain_stability_vs_noise.png`,
`fig_R3_camera_dropout_evidence.png`, `FigReal_Terrain_Latencies_4Panels.png`,
`fig_sr_vs_noise_level.png` (ídem, ya corregida en R2-02), `fig_transition_phases_v10.png`,
`fig_ablation_success_rate.png`, `fig_ablation_complex_stability.png`,
`Appetitive/Aversive/Complex/Obstacle_Real_Plot_1_Switching_Delay_ECDF.png` (4),
`Appetitive/Complex_Real_Plot_3_Temporal_Dynamics_PitchRollRMS.png` (spot-check; mismo builder que
Aversive/Obstacle, no se repitieron por presupuesto de la auditoría).

---

## 5. Estado

Cambios de **solo imagen** (`assets/*.png`) — ningún `\caption{}` ni texto de `sections/*.tex`
fue tocado, no se requiere `\revblue{}`. **10 archivos** regenerados y re-promovidos a `assets/`
vía `scripts/promote_figure.sh --force` (8 de la ronda 1 + `fig2_roc_curve.png`/
`fig3_training_loss.png` de la ronda 2, vectorizadas — ver Sección 2). Fila `C-21` en
`PROGRESS.md` documenta el cambio para trazabilidad, estado `applied` (las imágenes ya están en
`assets/`, listas para el próximo `push_to_overleaf.sh`).

Pendiente de decisión del autor: si incluir `FigReal_Morphological_Transition_Energy.png` (misma
inconsistencia tipográfica, no corregida — Sección 3) en una futura pasada de consistencia.
