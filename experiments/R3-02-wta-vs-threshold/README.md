# R3-02 — Ablation study: WTA (ganglios basales) vs. lógica de umbral

**Reviewer ask:** "Comparative tests removing neural layers/inhibitory connections to justify WTA
over threshold logic" (R3-02), y "Ablation analysis on basal ganglia arbitration network" (R3-01
— mismo dataset, ver `experiments/R3-01-basal-ganglia-ablation/README.md`).

## Goal

Justificar cuantitativamente por qué el circuito de ganglios basales STN/GPi/GPe/STR (winner-take-all
dinámico, `methodology.tex` §"Basal Ganglia Module") es superior a una arbitración de lógica de
umbral estática — la misma familia de lógica que el propio Módulo de Locomoción ya usa en otro punto
(umbral de 20° en X5/X6, `Ar=28.0` en X17), lo que hace de esta comparación un contraste natural
dentro del propio diseño del paper.

## Método

Se implementó un parámetro ROS `ablation_mode` en `red_neuronal.py` (rama `Deiv` de
`PETER_SIMULATION`) con 4 variantes:

- **`full`** (control): circuito STN/GPi/GPe/STR intacto, sin cambios.
- **`no_lateral_inhibition`**: se anulan (gain `xg=0`) los términos de inhibición cruzada entre los
  3 canales (Gpe→STN, STN→Gpi); los términos del mismo canal (auto-inhibición, Gpe/StR propios) se
  mantienen intactos. Responde a "remove... inhibitory connections" del comentario del referee.
- **`threshold_only`**: se bypasea por completo la dinámica STN/GPi/GPe/STR; el canal ganador se
  decide con umbrales de prioridad fija sobre el estímulo crudo (hostil > obstáculo > apetente,
  misma asimetría `ω_GpeR=2.0 > ω_GpeG=1.0` que ya usa el Módulo de Locomoción), y pasa su
  intensidad a Gpe con las mismas ganancias por canal que `full` (×5 obstáculo, ×0.7×0.5 apetente)
  — para que la única diferencia real entre variantes sea el mecanismo de arbitraje, no la escala
  de salida. Responde a "...over simple threshold decision logic".
- **`no_stn_str`** (agregada 2026-08-31, 4a variante): a diferencia de `no_lateral_inhibition`
  (que solo apaga conexiones puntuales dejando STN/STR funcionando), aquí las **capas neuronales**
  STN y STR dejan de computar por completo (quedan en 0) — GPi/GPe reciben el estímulo crudo
  directamente en su lugar, con las mismas ganancias por canal que STN habría aplicado, preservando
  la estructura competitiva cruzada de GPi/GPe pero sin la dinámica recurrente propia de STN ni la
  retroalimentación de STR. Responde específicamente a "remove **key neural layers**" del
  comentario del referee — la pieza que `no_lateral_inhibition` (conexiones) y `threshold_only`
  (todo el circuito reemplazado) no cubrían por separado.

Cada variante se corrió en 2 escenarios (reusando nombres/parámetros ya publicados en
`tab:consolidated_simulation_metrics` de `results.tex`):

- **Appetitive Targeting** (`ablation_appetitive_*`, escenario `single_stimulus.launch.py`, un solo
  estímulo azul) — control sin conflicto.
- **Complex Navigation** (`ablation_complex_*`, `multiple_stimuli.launch.py`, 3 estímulos
  rojo+verde+azul simultáneos) — el escenario de conflicto real, donde se espera que la arbitración
  importe.

`nl` (nivel de ruido) fijo en 0 en las 12 réplicas de cada suite (`fixed_noise_level_idx: 0`), para
no confundir el efecto estructural de la ablación con la robustez a ruido — esa ya está cubierta
por separado para el modelo `full` en `tab:consolidated_simulation_metrics` ($\sigma\in[0,4]$).

## Parámetros / semilla

Ver `config.yaml` (copia completa de `experiments_config.yaml` de `PETER_SIMULATION`, tomada
2026-08-30 — las 2 suites `no_stn_str` se agregaron ahí un poco después, 2026-08-31, mismos
parámetros que sus hermanas; solo las 8 suites `ablation_*` son relevantes aquí — el resto son las
familias A/B/C ya publicadas). N=12 réplicas por variante×escenario = 96 corridas totales (72 de
la primera pasada + 24 de `no_stn_str`). Sin semilla determinista explícita
(`random_perturbation: false` en las 8 suites — la variabilidad entre réplicas viene enteramente de
la dinámica no lineal del sistema + Gazebo, no de ruido inyectado).

## Data provenance

- Datos generados corriendo `scripts/test_manager.py` dentro del contenedor `peter_simulation`
  (`PETER_SIMULATION/docs/Makefile` → `run-experiments SUITE_FILTER=...`).
- **Commit exacto de `PETER_SIMULATION` pineado:**
  - Primera pasada (`full`/`no_lateral_inhibition`/`threshold_only`, 72 corridas):
    `e29d9a161e65209051e5508b7d6bff0cb20cdbcd` (rama `Deiv`, 2026-08-30) — incluye el parámetro
    `ablation_mode`, el cableado end-to-end `ablation_mode`/`nl` en los launch files, el fix de
    offset de índices en `test_manager.py` (`Z_OFFSET`), y el fix de descubrimiento `gz-transport`
    (`GZ_IP`/`IGN_IP`) necesario para que Gazebo funcionara de forma headless dentro de Docker.
  - Segunda pasada (`no_stn_str`, 24 corridas): `e343cce` (rama `Deiv`, 2026-08-31) — agrega la
    4a variante y el soporte de `SUITE_FILTER` con lista separada por comas para poder apuntar
    exactamente a las 2 suites nuevas sin re-correr las 6 ya cerradas.
- Corrida: primera pasada 2026-08-30 22:14 a 2026-08-31 00:09; segunda pasada (`no_stn_str`)
  2026-08-31 00:39 a 01:39 (hora local), sin intervención manual entre suites dentro de cada pasada.
- **No reproducible bit-a-bit** desde `config.yaml` solo — depende de la física no determinista de
  Gazebo (timing real de arranque de controladores, física del contacto, etc.); las tasas de éxito
  y las tendencias sí deberían replicarse cualitativamente en una re-corrida.

## Cómo regenerar

```bash
# Dentro de PETER_SIMULATION, rama Deiv, commit e343cce o posterior:
make docker-rm && make docker-create   # contenedor limpio, evita colisiones DDS entre corridas
make -f ros2_ws/src/peter_robot/docs/Makefile build
make run-experiments SUITE_FILTER=ablation_   # ~2.3h, 72 corridas (full/no_lateral_inhibition/threshold_only)

# Solo la 4a variante (aislada, sin tocar las 6 anteriores):
make run-experiments SUITE_FILTER=ablation_appetitive_no_stn_str,ablation_complex_no_stn_str

# Copiar resultados crudos (bind-mount directo, no requiere export):
cp -r PETER_SIMULATION/ros2_ws/src/peter_robot/docs/resultados/ablation_* \
      paper-revision/experiments/R3-02-wta-vs-threshold/data/

# Analisis estadistico:
cd paper-revision/experiments/R3-02-wta-vs-threshold/scripts
python3 analyze_ablation.py   # requiere scipy — output/ablation_stats_summary.{json,csv}
```

## Resultado (2026-08-31, actualizado con la 4a variante — sin gráficas/tablas de publicación todavía)

### Tasa de éxito (`test_manager.py` verdict SUCCESS/FAILURE_TIMEOUT), Fisher exact vs. `full`

| Escenario | `full` | `no_lateral_inhibition` | `threshold_only` | `no_stn_str` |
|---|---|---|---|---|
| Appetitive (sin conflicto) | 100% (12/12) | 91.7% (11/12), p=1.0 | 91.7% (11/12), p=1.0 | 91.7% (11/12), p=1.0 |
| **Complex (conflicto real)** | **100% (12/12)** | **25.0% (3/12), p=0.00034** | **83.3% (10/12), p=0.478** | **33.3% (4/12), p=0.00135** |

**Lectura:** sin conflicto, las 4 variantes rinden igual (~92-100%, como se esperaba — ninguna
ablación rompe el caso simple). Con conflicto real aparece un gradiente claro:
`full` (100%) > `threshold_only` (83.3%, no significativo con n=12 en esta métrica sola) >
`no_stn_str` (33.3%, **p=0.00135**, significativo) > `no_lateral_inhibition` (25.0%, **p=0.00034**,
el más significativo). Las dos ablaciones que remueven mecanismo del circuito de ganglios basales
en sí (`no_lateral_inhibition` y `no_stn_str`) degradan la tasa de éxito de forma altamente
significativa; reemplazar todo por lógica de umbral (`threshold_only`) degrada menos en esta
métrica binaria — pero ver más abajo: sus métricas continuas sí muestran degradación significativa.

### Métricas continuas, Mann-Whitney U vs. `full` (solo escenario Complex, el relevante para R3-02)

| Métrica | `no_lateral_inhibition` vs `full` | `threshold_only` vs `full` | `no_stn_str` vs `full` |
|---|---|---|---|
| `exp_latency` (latencia de decisión) | p=0.341 (n.s.) | **p=0.014** (más lento) | p=0.840 (n.s.) |
| `roll_rms` | **p=0.00016** (más inestable) | **p=0.017** (más inestable) | **p=0.00031** (más inestable) |
| `pitch_rms` | **p=0.00006** | **p=0.0029** | **p=0.0043** |
| `exp_lambda` (eficiencia de conflicto) | ver limitación abajo | ver limitación abajo | ver limitación abajo |

**Lectura de las 4 variantes juntas:** `no_lateral_inhibition` y `no_stn_str` — las dos ablaciones
que tocan el circuito de ganglios basales en sí (conexiones y capas, respectivamente) — degradan
significativamente tanto la tasa de éxito como la estabilidad de actitud (`roll_rms`/`pitch_rms`)
bajo conflicto, pero no la latencia de decisión. `threshold_only` es la única que degrada la
latencia de forma significativa (más lento en decidir), además de la estabilidad — consistente con
que un umbral estático no anticipa/suaviza la transición como sí lo hace la dinámica continua del
WTA. Juntas, las 3 ablaciones cubren exactamente el trío que pide el referee: conexiones
inhibitorias removidas (`no_lateral_inhibition`), capa neuronal removida (`no_stn_str`), y
arbitración reemplazada por lógica de umbral simple (`threshold_only`) — las 3 degradan el
desempeño bajo conflicto respecto al circuito completo, cada una en un aspecto distinto.

**Limitación conocida — `exp_lambda` sale 1.0 en las 96 corridas, en las 4 variantes:**
`neural_recorder.py::_compute_lambda_efficiency()` solo calcula λ real cuando rojo Y azul están
presentes *simultáneamente* en la ventana de muestreo (además, no incluye verde) — condición que
casi nunca se cumple en la práctica dentro de una sola corrida, así que devuelve el default
"sin conflicto" (1.0) casi siempre. **No es un resultado nulo real** — es un límite de la métrica
tal como está instrumentada hoy, no del efecto de la ablación. Si se retoma este análisis, ajustar
`_compute_lambda_efficiency()` para incluir el canal verde y una ventana de "conflicto reciente" en
vez de "conflicto en este instante exacto" antes de confiar en este número.

**Segunda limitación conocida — falta `firing_variance`/`temporal_consistency` en las 96 corridas:**
`neural_recorder.py` ya calcula y publica ambas métricas en `/experiment/metrics` como
`[latencia, firing_variance, temporal_consistency, λ]`, pero `test_manager.py::_cb_exp_metrics`
(línea ~136-140) solo lee los índices `[0]` (latencia) y `[3]` (λ) — descarta silenciosamente
`[1]`/`[2]`. No están en ningún `trial_summary.json`, no se pueden recuperar retroactivamente.

Esto importa específicamente para el argumento `threshold_only` vs. `full`: `threshold_only` es,
por construcción, una decisión siempre "nítida" (un `if/elif` nunca mezcla canales), así que λ
probablemente no distinguiría su modo de falla real — que es más plausible que sea **oscilación
cerca del límite del umbral** (parpadeo entre decisiones cuando el estímulo está justo en el borde,
ej. `R≈0.5`, sin la histéresis que la dinámica continua del WTA aporta de forma natural) que
"parálisis/indecisión" (lo que λ mide). `firing_variance` (oscilación de actividad en el tiempo) y
`temporal_consistency` (estabilidad del patrón de decisión entre ciclos) sí capturarían ese
parpadeo — pero no están disponibles en este dataset.

**No arreglar esto invalida el argumento actual** (tasa de éxito + latencia + `roll_rms`/`pitch_rms`
ya sustentan la comparación con significancia estadística donde importa) — pero si se quiere reforzar
específicamente el caso `threshold_only`, el camino es: (1) agregar `self._firing_variance =
msg.data[1]` / `self._temporal_consistency = msg.data[2]` a `_cb_exp_metrics`, exponerlas en el
snapshot/`trial_summary.json`, y (2) volver a correr las 4 variantes × Complex Navigation (48
corridas, ~2h) — no es necesario re-correr Appetitive (sin conflicto, ya sin diferencias
significativas en ninguna métrica). **Al redactar la prosa del paper, no sobrevender la comparación
`threshold_only` vs. `full` solo con lo que hay hoy** — la tasa de éxito (83.3% vs 100%) no llegó a
significancia por sí sola (p=0.478); el argumento se sostiene en latencia + estabilidad, no en la
tasa de éxito aislada.

## Archivos en `output/`

| Archivo | Contenido |
|---|---|
| `ablation_stats_summary.json` | Resultado completo: tasa de éxito + Fisher exact, medias/IC95%/Mann-Whitney por métrica, por escenario |
| `ablation_stats_summary.csv` | Mismo contenido en formato tabular plano, para consumo directo por scripts de gráficas/tablas |
| `fig_ablation_success_rate.png` | Figura de publicación: tasa de éxito por variante, un solo panel (Complex Navigation), generada por `scripts/plot_ablation.py` |
| `fig_ablation_complex_stability.png` | Figura de publicación: roll/pitch RMS por variante (Complex Navigation), generada por `scripts/plot_ablation.py` |

**Promovido a `assets/`** (2026-08-31, `scripts/promote_figure.sh`): `fig_ablation_success_rate.png`
y `fig_ablation_complex_stability.png`, referenciadas en la nueva subsección
`\subsubsection{Basal Ganglia Ablation Study}` de `results.tex` (párrafo de método en
`methodology.tex`) — ver `patches/r3-01-02-basal-ganglia-ablation-study.tex` y
`intake/processed/R3-01-02_ablation_writing_plan.md`. El panel Appetitive Targeting se descartó de
la figura de tasa de éxito (sin separación significativa entre variantes, p=1.000 en las 3
comparaciones) y se reporta en una frase de texto en su lugar.
