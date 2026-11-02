# C-74 — Figura 20 restaurada a R3-04 + auditoría de procedencia del ruido en `experiments/simulation/` (2026-11-01)

Autor: Diego (agente). Decisión del autor: restaurar la Fig. 20 de R3-04 (no adaptar el texto a la figura de C-22).
Fila: `C-74` (`PROGRESS.md`). Patch: `patches/c-74-restore-fig20-r304-grid.tex`.

## 1. Qué se corrigió (C-74)

- **Regresión de asset.** `C-22` (`5e92625`, 2026-09-01) sobrescribió `assets/fig1_noise_robustness_grid.png`
  con la salida de N-01 (`macro_robustness.py` sobre `experiments/simulation/`, sha1 `d4eaff59`, 3000x3300:
  eje "Sensory Noise Index (σ)", 3 columnas, Pitch fijo 0–4°). El caption y la prosa (R3-04, R2b-02, R3b-03)
  describían la versión R3-04 (sha1 `0957b3df`, 3900x3300: 4 columnas con $T_{switch}$, eje "Combined
  Perturbation Level", nota interna sobre la inyección conjunta). Re-promovida con
  `scripts/promote_figure.sh experiments/R3-04-noise-robustness/output/fig1_noise_robustness_grid.png fig1_noise_robustness_grid.png --force`.
  La versión enviada en R2 (`82b93ab`) ya llevaba el asset equivocado.
- **Caption de la Fig. 20.** La frase de escala decía "per-row scale (ceiling at 1.1× that row's maximum)";
  `noise_sweep_grid.py` usa un techo común a las 4 filas (1.1 × el mayor media+1σ). Corregida.
- **Tabla 9 (`tab:consolidated_simulation_metrics`).** El párrafo previo la presentaba como el resumen agrupado
  de la batería de la Fig. 20. Recalculada desde los logs: sus 24 valores (T_sim, Roll, Pitch; media ± SD
  poblacional; 4 suites) coinciden exactamente con los ensayos `SUCCESS` de `experiments/simulation/familia_{a_*,b_compleja}`
  (Obstacle `test_007` excluido), es decir los mismos ensayos que las filas Neural de `tab:fsm_comparison`, no la
  batería combinada de R3-04. El párrafo ahora lo dice; los valores no cambian.
- Referencias a la Fig. 20 revisadas (results.tex l.73, 82, 91, 128, 130, 176): todas describen la batería combinada
  y son coherentes con la figura restaurada; solo l.130 necesitó cambio. §2.3.5 no necesita cambios.
- Prevención: `experiments/N-01-simulation-figure-regeneration/README.md` advierte que su `fig1_noise_robustness_grid.png`
  no se debe volver a promover (mismo nombre de archivo que la Fig. 20 publicada).

## 2. Hallazgo abierto — el ruido no consta como activo en `experiments/simulation/` (no se tocó el texto)

**Evidencia (datos versionados en el repo):**
- En las 6 familias de `experiments/simulation/` (96 intentos), `trial_summary.json.final_metrics.noise_idx` y la columna
  por paso `unified_metrics.csv.active_noise_level` valen **0 en todos los intentos**, aunque el manifiesto asigna
  `seed_info.noise_level_idx` = 0–4 (3 misiones por nivel).
- Según `experiments/R3-04-noise-robustness/robustez_transferencia_tecnica.md:215`, ese campo es el "nivel de
  perturbación activo"; en el dataset de R3-04 sí sigue el índice 0–4.

**Mecanismo probable (código de `sammcar/PETER_SIMULATION@main`, solo lectura):**
- `red_neuronal.py` toma el nivel del parámetro ROS `nl` (`declare_parameter('nl', 0)`), deriva de él
  `_sigma_noise = NoiseLevel[nl]` (`[0, 0.05, 0.10, 0.20, 0.30]`) y publica ese mismo índice como `metricsArr[4]`,
  que `metrics_recorder.py` guarda como `active_noise_level` (así desde `3c0b9726`, 2026-06-06).
- `scripts/test_manager.py` pasa un argumento de launch `noise_level_idx:=<idx>`; `single_stimulus.launch.py` y
  `multiple_stimuli.launch.py` no lo declaran, y `terrain_navigation`/`slope_navigation.launch.py` lo declaran pero
  lanzan `red_neuronal` sin parámetros. Nada lo traduce a `nl`, así que el controlador corre con σ = 0.
- No se conoce el commit exacto que generó estos datos (`SIMULATION_TEAM_ACTION_ITEMS.md` §9), pero el esquema del
  recorder implica código ≥ 2026-06-06. Ítem §2 del mismo documento: el mapeo índice→σ nunca se documentó.

**Afirmaciones del manuscrito que dependen de esto (sin cambiar; requieren decisión del owner + confirmación de Sam):**
- §3.1.8 (`C-61`): "zero-mean Gaussian noise proportional to the measured value was added ... at five levels
  (σ = 0, 5, 10, 20, and 30%)" y "filtered out the injected sensor noise" (datos: `familia_c1/c2` de
  `experiments/simulation/`, vía N-01).
- §3.1.10: Fig. 36 (`fig:attempts_vs_noise_level`, línea Neural = estos ensayos) y su prosa ("at the noisiest levels
  tested"); filas Neural A/B de `tab:fsm_comparison`; §2.3.6 "under matching ... noise levels". El lado FSM no está
  en el repo (`data/` gitignored): hay que comprobar si sus corridas sí recibieron `nl`.
- Tabla 9: tras C-74 ya no afirma nada sobre ruido ("separate archived simulation battery"). Si se confirma σ = 0,
  conviene decirlo explícitamente.

**Siguiente paso sugerido:** Sam revisa los logs de arranque de esas corridas (`[ROBUSTEZ] Nivel de ruido activo:
σ = …%`, impreso por `red_neuronal.py` al iniciar) o el commit usado. Si σ = 0, el owner decide la redacción (p. ej.
describir esas baterías como réplicas sin ruido con posición de estímulos aleatorizada) en filas `C-xx` nuevas.
