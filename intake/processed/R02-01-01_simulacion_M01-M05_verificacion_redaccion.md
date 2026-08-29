# R02-01-01 — Discrepancias texto↔figura en simulación (M-01–M-05): verificación y redacción

**Estado: ✅ CERRADO (2026-08-27).** Verificación de datos + redacción, ambas confirmadas por `grep` exacto
contra `sections/results.tex` el 2026-08-27 (ver §4). Sin acción pendiente.

**Origen:** hallazgo de auditoría de `intake/pending/R02-01_metric_and_figure_audit.md` (§2, "Informe 1") +
verificación de datos de `intake/pending/R02-01_data_traceability_and_plotting_plan.md` (§0, "Informe 2") —
ambos documentos fueron eliminados tras atomizarse (ver `intake/R02-01_INDEX.md`); este archivo es la fuente
completa y autocontenida de este bloque específico.

## 1. Qué se encontró (diagnóstico original)

Auditoría de `sections/results.tex` cruzando cada valor numérico citado en prosa contra el valor real leído en
la figura/tabla que la prosa dice sustentar, para la subsección de simulación. Cuatro discrepancias críticas
(M-01–M-04) y un control positivo (M-05):

| ID | Texto afirmaba | Figura mostraba | Severidad |
|---|---|---|---|
| M-01 | Decision latency "≈47 ms, constante" (`results.tex:77,178,973`) | Panel C de `fig1_*_macro.png`: 50–2000+ ms, variable con ruido; solo `fig1_Complex_macro.png` ronda 47ms, pero el texto lo atribuye a Appetitive | Crítica |
| M-02 | Tipover Risk "$\mu_{TR}\approx0.42$ ... escalada monótona a $TR\approx0.58$" (`results.tex:276`) | `FigA_Stability_Profile.png`: plano en TR≈0.58–0.60 en ambos terrenos, sin escalada, con un pico transitorio aislado en rugoso (t=-1.3 a -0.5s, hasta TR≈0.77) | Crítica |
| M-03 | Roll/Pitch RMS "$\mu_\phi\approx1.36°,\mu_\theta\approx1.25°$ rugoso vs. $0.43°/6.95°$ pendiente, zero cluster overlap" (`results.tex:281` + caption) | `FigC_Terrain_Adaptability.png`: rugoso roll≈1.3–1.6°/pitch≈1.2–1.8°; pendiente roll≈1.4–1.65°/pitch≈2.0–3.25°; el rango de roll de pendiente está **contenido dentro** del de rugoso — justo lo opuesto de "zero overlap" | Crítica (la más extrema, medias citadas ~3-4× distintas) |
| M-04 | $T_{switch}$ "invariante a 0.3ms, perfect Heaviside step, sin chattering" (`results.tex:279`) | `FigB_Decision_Delay.png` panel B (rugoso): cola real hasta 600ms en 13% de ensayos; panel C (pendiente): escalera de 5-6 saltos entre 0.8-1.9ms, no un valor único | Menor pero real |
| M-05 | accuracy=0.800, precision=0.747, recall=0.918 (n=120) del clasificador MLP (`results.tex:571`) | `fig1_confusion_matrix.png` (TP=56,FN=5,FP=19,TN=40) reproduce esas cifras exactas | **Control positivo — sin problema, no requirió acción** |

## 2. Verificación de datos crudos (2026-08-27)

Se recalcularon las cuatro estadísticas directamente contra `experiments/simulation/` (CSV/JSON crudos, no solo
inspección visual):

- **M-01:** `trial_summary.json.exp_latency`, 15 réplicas `familia_a_apetitivo` — rango real 0.015s–3.07s, media≈60ms
  solo en $\sigma=0$, subiendo a 1.6–2.0s en $\sigma\geq1$.
- **M-02:** `stability_log.csv`/`TR`, 15+15 réplicas C1/C2 — media global rugoso=0.600 (rango 0.549–0.605 salvo 2
  picos a 1.86), media global pendiente=0.593 (rango 0.580–0.605 salvo 2 picos a 1.66).
- **M-03:** `trial_summary.json.roll_rms`/`pitch_rms`, 30 réplicas — rugoso media roll=1.586°, pitch=1.667°;
  pendiente media roll=1.469°, pitch=2.290°.
- **M-04:** `trial_summary.json.tswitch`, 30 réplicas — rugoso: 0.0002–0.0007s en 13/15, pero 2/15 (13.3%) en
  0.5999s/0.6006s; pendiente: 0.0009–0.0018s, 15 valores distintos sin agruparse.

**Veredicto en los 4 casos: la figura coincide con el dato crudo; el texto es el que estaba desactualizado**
(probablemente escrito contra una corrida anterior o una generalización optimista sin releer las figuras
finales). **No es un problema de validez del experimento** — es un problema de qué documento (texto vs. figura)
refleja el dataset que hoy vive en el repositorio.

## 3. Redacción aplicada

Los 5 pasajes se reescribieron con los valores reales de arriba, envueltos en `\revblue{}` (regla permanente del
proyecto):

- `results.tex:77` (Appetitive Targeting)
- `results.tex:178` (caption `tab:consolidated_simulation_metrics`)
- `results.tex:276` (Tipover Risk)
- `results.tex:279` ($T_{switch}$/Heaviside)
- `results.tex:269` + `results.tex:281` (phase-space, caption + párrafo)

## 4. Confirmación final (2026-08-27, verificación con `grep` exacto)

Se verificó línea por línea contra `sections/results.tex` (no solo contra `PROGRESS.md`) que los 5 pasajes
contienen efectivamente los valores reales:

- L.77: `\revblue{...≈60 ms mean...1.6–2.0 s range...}` ✅
- L.178: caption genérica sin cifra desactualizada ✅
- L.276: `\revblue{...μ≈0.58–0.60, no monotonic escalation...}` ✅
- L.279: `\revblue{...sub-millisecond...not fully invariant...}` ✅
- L.269/281: `\revblue{...μφ≈1.59°/1.67° vs 1.47°/2.29°...}` ✅

No hay ninguna acción de redacción pendiente para este bloque.

## 5. Trazabilidad

- Patch: `patches/n-04-m01-m04-text-redaction.tex`
- `PROGRESS.md`: fila `N-04`, estado `applied`
- Commit: incluido en `d93adbd` (patch: N-03/N-04 physical figure promotion, F-03 classifier fusion, M-01-M-04
  text redaction)
