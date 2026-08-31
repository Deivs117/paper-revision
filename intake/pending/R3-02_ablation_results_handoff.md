# R3-01 / R3-02 — Ablation study del circuito de ganglios basales: datos listos, sin redactar todavía

**Reviewers atendidos:** R3-01 ("Ablation analysis on basal ganglia arbitration network"), R3-02
("Comparative tests removing neural layers/inhibitory connections to justify WTA over threshold
logic"). Ambas filas en `PROGRESS.md` siguen en `pending` — este documento es la entrada de intake
para que se triage (no una redacción ya lista).

**Estado:** datos crudos generados + análisis estadístico numérico calculado. **Sin gráficas, sin
tablas con formato de publicación, sin texto de manuscrito todavía** — eso queda para un paso
posterior, deliberadamente.

## Qué se hizo

1. Se implementó un parámetro `ablation_mode` en `red_neuronal.py` (rama `Deiv` de
   `PETER_SIMULATION`) con 4 variantes: `full` (control), `no_lateral_inhibition` (quita la
   inhibición cruzada entre canales del circuito STN/GPi/GPe/STR — commit `e29d9a1`),
   `threshold_only` (bypasea el circuito completo por una lógica de umbral de prioridad fija,
   análoga a la que el propio Módulo de Locomoción ya usa en otro punto del diseño — commit
   `e29d9a1`), y `no_stn_str` (remoción real de las capas STN y STR, no solo de una conexión —
   commit `e343cce`, agregada 2026-08-31 para cubrir específicamente "remove key neural layers"
   del comentario del referee, que las otras dos no cubrían por separado).
2. Se corrieron 96 simulaciones (4 variantes × 2 escenarios × 12 réplicas) vía el orquestador
   `test_manager.py` ya existente en `PETER_SIMULATION` — *Appetitive Targeting* (sin conflicto,
   control) y *Complex Navigation* (conflicto real de 3 estímulos), reusando los nombres/parámetros
   de escenario ya publicados en `tab:consolidated_simulation_metrics` de `results.tex`. (72 en la
   primera pasada + 24 de `no_stn_str` en una segunda pasada aislada.)
3. Se calculó tasa de éxito (Fisher exact vs. `full`) y medias/IC95%/Mann-Whitney U (vs. `full`)
   sobre latencia de decisión, `Tswitch`, `roll_rms`, `pitch_rms` y λ (eficiencia de conflicto),
   por escenario, para las 4 variantes.

Durante el proceso se encontraron y corrigieron 4 bugs preexistentes en `PETER_SIMULATION` (no
relacionados con el paper en sí, pero bloqueaban poder correr esto): offset de índices en
`test_manager.py` (leía neuronas equivocadas del vector `/neuron_activity`), overrides de debug de
inclinación activos en `red_neuronal.py` (rompían la arbitración multi-estímulo real), `red_neuronal`
lanzándose sin ningún parámetro en los launch files (el barrido de ruido nunca llegaba al nodo), y
descubrimiento `gz-transport` fallando en Docker (arreglado con `GZ_IP`/`IGN_IP`). Todos documentados
con detalle en los mensajes de commit de la rama `Deiv`.

## Dónde está todo

- **Dataset completo + método + provenance + resultados numéricos:**
  `experiments/R3-02-wta-vs-threshold/` (README.md ahí tiene el detalle completo — no se repite aquí).
- **Referencia cruzada para R3-01:** `experiments/R3-01-basal-ganglia-ablation/README.md` (mismo
  dataset, sin duplicar).
- `experiments/R3-02-wta-vs-threshold/data/` — los 96 `trial_summary.json`/`metrics_raw.csv`/
  `unified_metrics.csv` crudos (gitignored, regenerable desde `PETER_SIMULATION`).
- `experiments/R3-02-wta-vs-threshold/output/ablation_stats_summary.{json,csv}` — el análisis
  estadístico ya calculado, ya incluye las 4 variantes (committeado, es pequeño).

## Resultado (resumen — el detalle completo con tablas está en el README del experimento)

Sin conflicto (Appetitive), las 4 variantes rinden igual (100%/91.7%/91.7%/91.7% de éxito, ninguna
diferencia significativa) — la ablación no rompe el caso simple, como se esperaba.

Con conflicto real (Complex Navigation), gradiente claro:
- `full` → 100% de éxito.
- `threshold_only` → 83.3% de éxito (p=0.478 vs. `full`, no significativo en esta métrica sola) —
  **pero** sí muestra degradación significativa en latencia de decisión (p=0.014), `roll_rms`
  (p=0.017) y `pitch_rms` (p=0.0029).
- `no_stn_str` → 33.3% de éxito (Fisher exact **p=0.00135** — significativo), con degradación
  significativa adicional en `roll_rms` (p=0.00031) y `pitch_rms` (p=0.0043), sin degradar
  latencia (p=0.84, n.s.).
- `no_lateral_inhibition` → 25% de éxito (Fisher exact **p=0.00034** — el más significativo de
  los tres), con el mismo patrón: `roll_rms`/`pitch_rms` significativos, latencia no significativa.

**Lectura conjunta:** las dos ablaciones que tocan el circuito de ganglios basales en sí
(`no_lateral_inhibition` = conexiones, `no_stn_str` = capas) degradan fuerte la tasa de éxito y la
estabilidad de actitud, pero no la latencia de decisión. `threshold_only` (reemplazo completo por
umbral) es la única que sí degrada la latencia — consistente con que un umbral estático no
anticipa/suaviza la transición como la dinámica continua del WTA. Las 3 juntas cubren exactamente
el trío que pide el comentario del referee: "remove key neural layers" (`no_stn_str`) **or**
"inhibitory connections" (`no_lateral_inhibition`) **+** comparación contra "simple threshold
decision logic" (`threshold_only`).

**Limitación conocida:** λ (eficiencia de conflicto) sale 1.0 en las 96 corridas por una limitación
de `neural_recorder.py::_compute_lambda_efficiency()` (solo dispara con rojo+azul simultáneos, no
incluye verde) — no es un resultado nulo real, ver detalle en el README del experimento.

## Qué falta (a triage — no decidido aquí)

- [ ] Decidir en equipo cuánto de esto se convierte en subsección de `methodology.tex`/`results.tex`
      vs. solo una tabla/mención breve.
- [ ] Generar la(s) figura(s)/tabla(s) con formato de publicación desde
      `output/ablation_stats_summary.csv` (barras de tasa de éxito por variante/escenario;
      posiblemente una tabla en el formato de `tab:consolidated_simulation_metrics` con una columna
      extra de variante).
- [ ] Decidir si vale la pena arreglar `_compute_lambda_efficiency()` (incluir verde + ventana de
      "conflicto reciente") y re-correr antes de reportar λ, o si se omite esa métrica del reporte
      final y se reporta solo tasa de éxito + latencia + roll/pitch RMS.
- [ ] Redactar la prosa (fuera de alcance de este documento — este es solo el hallazgo/handoff).
- [ ] Una vez redactado: asignar `Category=Pruebas`, `Owner`, actualizar `PROGRESS.md` R3-01/R3-02
      de `pending` a `drafted`, y `git mv` este archivo a `intake/processed/`.
