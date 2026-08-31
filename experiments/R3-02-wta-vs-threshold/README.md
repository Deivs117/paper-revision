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
`PETER_SIMULATION`) con 3 variantes:

- **`full`** (control): circuito STN/GPi/GPe/STR intacto, sin cambios.
- **`no_lateral_inhibition`**: se anulan (gain `xg=0`) los términos de inhibición cruzada entre los
  3 canales (Gpe→STN, STN→Gpi); los términos del mismo canal (auto-inhibición, Gpe/StR propios) se
  mantienen intactos.
- **`threshold_only`**: se bypasea por completo la dinámica STN/GPi/GPe/STR; el canal ganador se
  decide con umbrales de prioridad fija sobre el estímulo crudo (hostil > obstáculo > apetente,
  misma asimetría `ω_GpeR=2.0 > ω_GpeG=1.0` que ya usa el Módulo de Locomoción), y pasa su
  intensidad a Gpe con las mismas ganancias por canal que `full` (×5 obstáculo, ×0.7×0.5 apetente)
  — para que la única diferencia real entre variantes sea el mecanismo de arbitraje, no la escala
  de salida.

Cada variante se corrió en 2 escenarios (reusando nombres/parámetros ya publicados en
`tab:consolidated_simulation_metrics` de `results.tex`):

- **Appetitive Targeting** (`ablation_*_full/no_lateral_inhibition/threshold_only`, escenario
  `single_stimulus.launch.py`, un solo estímulo azul) — control sin conflicto.
- **Complex Navigation** (`ablation_complex_*`, `multiple_stimuli.launch.py`, 3 estímulos
  rojo+verde+azul simultáneos) — el escenario de conflicto real, donde se espera que la arbitración
  importe.

`nl` (nivel de ruido) fijo en 0 en las 12 réplicas de cada suite (`fixed_noise_level_idx: 0`), para
no confundir el efecto estructural de la ablación con la robustez a ruido — esa ya está cubierta
por separado para el modelo `full` en `tab:consolidated_simulation_metrics` ($\sigma\in[0,4]$).

## Parámetros / semilla

Ver `config.yaml` (copia completa de `experiments_config.yaml` de `PETER_SIMULATION` en el momento
de la corrida; solo las 6 suites `ablation_*` son relevantes aquí — el resto son las familias A/B/C
ya publicadas). N=12 réplicas por variante×escenario = 72 corridas totales. Sin semilla determinista
explícita (`random_perturbation: false` en las 6 suites — la variabilidad entre réplicas viene
enteramente de la dinámica no lineal del sistema + Gazebo, no de ruido inyectado).

## Data provenance

- Datos generados corriendo `scripts/test_manager.py` dentro del contenedor `peter_simulation`
  (`PETER_SIMULATION/docs/Makefile` → `run-experiments SUITE_FILTER=ablation_`).
- **Commit exacto de `PETER_SIMULATION` pineado:** `e29d9a161e65209051e5508b7d6bff0cb20cdbcd`
  (rama `Deiv`, 2026-08-30) — incluye el parámetro `ablation_mode`, el cableado end-to-end
  `ablation_mode`/`nl` en los launch files, el fix de offset de índices en `test_manager.py`
  (`Z_OFFSET`), y el fix de descubrimiento `gz-transport` (`GZ_IP`/`IGN_IP`) necesario para que
  Gazebo funcionara de forma headless dentro de Docker.
- Corrida: 2026-08-30 22:14 a 2026-08-31 00:09 (hora local), sin intervención manual entre
  suites — corrido de punta a punta vía `test_manager.py`.
- **No reproducible bit-a-bit** desde `config.yaml` solo — depende de la física no determinista de
  Gazebo (timing real de arranque de controladores, física del contacto, etc.); las tasas de éxito
  y las tendencias sí deberían replicarse cualitativamente en una re-corrida.

## Cómo regenerar

```bash
# Dentro de PETER_SIMULATION, rama Deiv, commit e29d9a1 o posterior:
make docker-rm && make docker-create   # contenedor limpio, evita colisiones DDS entre corridas
make -f ros2_ws/src/peter_robot/docs/Makefile build
make run-experiments SUITE_FILTER=ablation_   # ~2.3h, 72 corridas

# Copiar resultados crudos (bind-mount directo, no requiere export):
cp -r PETER_SIMULATION/ros2_ws/src/peter_robot/docs/resultados/ablation_* \
      paper-revision/experiments/R3-02-wta-vs-threshold/data/

# Analisis estadistico:
cd paper-revision/experiments/R3-02-wta-vs-threshold/scripts
python3 analyze_ablation.py   # requiere scipy — output/ablation_stats_summary.{json,csv}
```

## Resultado (2026-08-31, primera pasada — sin gráficas/tablas de publicación todavía)

### Tasa de éxito (`test_manager.py` verdict SUCCESS/FAILURE_TIMEOUT), Fisher exact vs. `full`

| Escenario | `full` | `no_lateral_inhibition` | `threshold_only` |
|---|---|---|---|
| Appetitive (sin conflicto) | 100% (12/12) | 91.7% (11/12), p=1.0 | 91.7% (11/12), p=1.0 |
| **Complex (conflicto real)** | **100% (12/12)** | **25.0% (3/12), p=0.00034** | **83.3% (10/12), p=0.478** |

**Lectura:** sin conflicto, las 3 variantes rinden igual (como se esperaba — la ablación no debería
romper el caso simple). Con conflicto real, quitar la inhibición lateral colapsa la tasa de éxito
de forma altamente significativa (p<0.001); reemplazar todo el circuito por lógica de umbral
degrada la tasa de éxito pero no llega a significancia con n=12 en esta métrica binaria sola —
sin embargo, ver más abajo: las métricas continuas sí muestran degradación significativa de
`threshold_only` en el escenario de conflicto.

### Métricas continuas, Mann-Whitney U vs. `full` (solo escenario Complex, el relevante para R3-02)

| Métrica | `no_lateral_inhibition` vs `full` | `threshold_only` vs `full` |
|---|---|---|
| `exp_latency` (latencia de decisión) | p=0.341 (n.s.) | **p=0.014** (más lento) |
| `roll_rms` | **p=0.00016** (más inestable) | **p=0.017** (más inestable) |
| `pitch_rms` | **p=0.00006** | **p=0.0029** |
| `exp_lambda` (eficiencia de conflicto) | ver limitación abajo | ver limitación abajo |

**Limitación conocida — `exp_lambda` sale 1.0 en las 72 corridas, en las 3 variantes:**
`neural_recorder.py::_compute_lambda_efficiency()` solo calcula λ real cuando rojo Y azul están
presentes *simultáneamente* en la ventana de muestreo (además, no incluye verde) — condición que
casi nunca se cumple en la práctica dentro de una sola corrida, así que devuelve el default
"sin conflicto" (1.0) casi siempre. **No es un resultado nulo real** — es un límite de la métrica
tal como está instrumentada hoy, no del efecto de la ablación. Si se retoma este análisis, ajustar
`_compute_lambda_efficiency()` para incluir el canal verde y una ventana de "conflicto reciente" en
vez de "conflicto en este instante exacto" antes de confiar en este número.

## Archivos en `output/`

| Archivo | Contenido |
|---|---|
| `ablation_stats_summary.json` | Resultado completo: tasa de éxito + Fisher exact, medias/IC95%/Mann-Whitney por métrica, por escenario |
| `ablation_stats_summary.csv` | Mismo contenido en formato tabular plano, para consumo directo por scripts de gráficas/tablas |

**No promovido a `assets/` todavía** — pendiente de generación de gráficas/tablas con formato de
publicación y de la redacción de la subsección correspondiente en `methodology.tex`/`results.tex`
(ver `intake/pending/R3-02_ablation_results_handoff.md`).
