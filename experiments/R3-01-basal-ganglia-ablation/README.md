# R3-01 — Ablation analysis on basal ganglia arbitration network

**Reviewer ask:** "Ablation analysis on basal ganglia arbitration network."

## Este experimento comparte dataset con R3-02

R3-01 ("¿importa el circuito de ganglios basales en sí?") y R3-02 ("¿WTA vs. lógica de umbral?")
se responden con el **mismo batch de 72 corridas** — no se duplicó el dato en dos carpetas.

**Toda la data cruda, el método, la provenance y el análisis estadístico viven en:**
→ `experiments/R3-02-wta-vs-threshold/`

Específicamente para R3-01, las variantes relevantes de ese experimento son:

- `full` (control) vs. `no_lateral_inhibition` — quitar la inhibición cruzada entre canales
  (Gpe→STN, STN→Gpi) remueve el mecanismo de arbitraje del circuito STN/GPi/GPe/STR, dejando los
  3 canales evolucionar desacoplados (ablation de **conexión**). Tasa de éxito cae de 100% a 25%
  bajo conflicto real (Fisher exact p=0.00034).
- `full` (control) vs. `no_stn_str` (4a variante, agregada 2026-08-31) — remoción real de **capa
  neuronal**: los núcleos STN y STR dejan de computar por completo (no solo se apaga una conexión
  puntual), GPi/GPe reciben el estímulo crudo directamente en su lugar. Tasa de éxito cae de 100% a
  33.3% bajo conflicto real (Fisher exact p=0.00135) — la comparación más literal con lo que pide
  R3-01 ("ablation analysis on basal ganglia arbitration network", removiendo capas, no solo
  conexiones).

Ambas ablaciones degradan significativamente `roll_rms`/`pitch_rms` bajo conflicto real
(Mann-Whitney p<0.001), sin degradar significativamente la latencia de decisión — a diferencia de
`threshold_only` (la 3a variante corrida, más específica de R3-02: WTA vs. umbral simple, que sí
degrada la latencia). Detalle completo, con las 4 variantes, en el README de R3-02.

No se creó `data/`/`scripts/`/`output/` propios aquí para evitar mantener dos copias del mismo
dataset desincronizadas — ver `experiments/R3-02-wta-vs-threshold/README.md` para el método completo,
la provenance (commit pineado de `PETER_SIMULATION`), cómo regenerar, y los resultados.
