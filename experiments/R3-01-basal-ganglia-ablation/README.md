# R3-01 — Ablation analysis on basal ganglia arbitration network

**Reviewer ask:** "Ablation analysis on basal ganglia arbitration network."

## Este experimento comparte dataset con R3-02

R3-01 ("¿importa el circuito de ganglios basales en sí?") y R3-02 ("¿WTA vs. lógica de umbral?")
se responden con el **mismo batch de 72 corridas** — no se duplicó el dato en dos carpetas.

**Toda la data cruda, el método, la provenance y el análisis estadístico viven en:**
→ `experiments/R3-02-wta-vs-threshold/`

Específicamente para R3-01, las variantes relevantes de ese experimento son:

- `full` (control) vs. `no_lateral_inhibition` — esta comparación **es** el ablation del circuito de
  ganglios basales: quitar la inhibición cruzada entre canales (Gpe→STN, STN→Gpi) es literalmente
  remover el mecanismo de arbitraje del circuito STN/GPi/GPe/STR, dejando los 3 canales evolucionar
  desacoplados. El resultado (`output/ablation_stats_summary.{json,csv}` en R3-02): tasa de éxito
  cae de 100% a 25% bajo conflicto real (Fisher exact p=0.00034), con degradación significativa
  adicional en `roll_rms`/`pitch_rms` (Mann-Whitney p<0.001).

`threshold_only` (la otra variante corrida) es más específica de R3-02 (WTA vs. umbral) que de R3-01
(¿importa el circuito en sí?), pero el mismo dataset la incluye.

No se creó `data/`/`scripts/`/`output/` propios aquí para evitar mantener dos copias del mismo
dataset desincronizadas — ver `experiments/R3-02-wta-vs-threshold/README.md` para el método completo,
la provenance (commit pineado de `PETER_SIMULATION`), cómo regenerar, y los resultados.
