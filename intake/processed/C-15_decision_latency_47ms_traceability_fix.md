# C-15 — Plan de redacción: cifra fantasma "47 ms" de latencia de decisión en `methodology.tex:200`

**Estado: 🔲 Plan listo, ejecutar en esta misma pasada.** No existía ningún plan previo de Sebas para
este hallazgo — su patch (`patches/c-14-redundancy-pass-post-r2-01.tex`) solo lo detectó y lo filed
como fila separada (`PROGRESS.md`, originalmente `C-11`, renumerada a `C-15` en la auditoría de
coherencia del 2026-08-29), sin proponer una solución de texto. Este documento es ese plan.

**Origen:** fila `C-15` de `PROGRESS.md`, `pending`, sin owner. Cita textual del problema en la
propia fila: *"methodology.tex line 200 cites 'the decision latency of approximately 47 ms measured
across all experimental trials (Section~3)', but grepping results.tex for '47' finds no such figure
anywhere in that section"*.

---

## 0. El texto problemático (verbatim, `methodology.tex:201`)

> "Its decentralized winner-take-all dynamics enable low-latency conflict resolution between
> competing sensory drives. As evidenced by the decision latency of approximately $47$~ms measured
> across all experimental trials (Section~\ref{sec:results}), the architecture operates within
> real-time constraints on resource-constrained embedded hardware, without requiring the training
> cycles or inference infrastructure associated with deep reinforcement learning or model predictive
> control frameworks, making interpretability and low runtime overhead intrinsic properties of the
> proposed design."

Esta oración es parte del párrafo de justificación arquitectónica (texto de la ronda R1, ya sin
`\revblue{}` desde el strip del 2026-08-25) que argumenta las ventajas de la arquitectura frente a
RL/MPC. El "~47 ms" es la única pieza de evidencia cuantitativa citada — y no existe.

## 1. Escaneo realizado (imágenes + datos crudos, no solo grep de texto)

### 1.1 Las tres figuras de latencia de decisión existentes en `results.tex`, inspeccionadas visualmente

| Figura | Rango real que muestra | ¿Contiene 47 ms? |
|---|---|---|
| `fig1_Appetitive_macro.png` panel C ("Decision Latency Profile", simulación, eje Y en ms) | σ=0: ~60 ms media; sube a 1600–2000 ms en σ=4 | No — el punto más bajo (σ=0) está cerca pero es ~60 ms, no 47 ms, y de cualquier forma esa cifra ya está correctamente citada en `results.tex:78` como "≈60 ms" |
| `FigB_Decision_Delay.png` panel A ("Reaction Latency $T_{response}$", simulación) | Step function exacta en $t=0.0$ s (determinístico) | No — es 0.0 s, no 47 ms |
| `FigReal_Terrain_Latencies_4Panels.png` paneles A/B ("Neural Processing Latency", hardware real) | Panel A: 184–189 ms; Panel B: 534.5–535.2 ms | No — ningún panel se acerca a 47 ms |

### 1.2 Datos crudos de simulación (96 archivos `trial_summary.json`, campo `exp_latency`)

```
n = 51 trials con exp_latency válido (excluyendo el centinela -1.0 de familia_a_obstaculo)
mean = 730.9 ms   median = 102.6 ms   min = 1.4 ms   max = 3467.6 ms
```

Ninguna cifra agregada (media, mediana) ni ningún trial individual da ~47 ms de forma que pueda
justificar razonablemente el redondeo a "approximately 47 ms". Un trial aislado
(`familia_a_apetitivo/test_001_SUCCESS`) tiene `exp_latency: 0.047` exacto, pero es un único trial
de 51 (ni media ni mediana ni valor destacado en ninguna figura) — coincidencia, no la fuente real
de la cifra citada.

### 1.3 Repositorio de referencia `PETER_SIMULATION` (solo lectura, vía `intake/SOURCES.md`)

`grep -rn "47"` sobre todo el árbol (excluyendo ruido de `numpy`/`.venv`) no encontró ninguna
constante de firmware, configuración de frecuencia de control, ni log relacionado con latencia de
decisión que diera 47 ms.

### 1.4 Conclusión del escaneo

**El "47 ms" no es trazable a ningún dato, figura, ni tabla existente en este repositorio ni en el
repositorio de referencia.** Es, con alta probabilidad, una cifra que quedó de una versión anterior
del manuscrito (pre-R1, nunca recalculada cuando las figuras de latencia se regeneraron en rondas
posteriores) y que sobrevivió intacta porque la oración nunca fue tocada por ninguna de las pasadas
de limpieza (`R2-01`, `C-07`, `C-08`, etc. — todas trabajaron alrededor de este párrafo sin leerlo
línea por línea hasta que `C-14` lo hizo).

## 2. Plan de redacción — reemplazar la cifra fantasma por evidencia real ya verificada

**No hay que inventar ni recalcular nada nuevo.** El párrafo solo necesita apoyarse en números que
ya existen, están verificados y citados en otras partes de `results.tex` con trazabilidad completa:

- **Simulación:** latencia de decisión neuronal determinística, $T_{response} = 0.0$~s (ECDF tipo
  Heaviside, `results.tex:278`, Fig.~`fig:decision_delay`) — el despacho de la decisión ocurre en el
  mismo frame de simulación que la perturbación.
- **Hardware real:** latencia de procesamiento neuronal medida en 15 réplicas de hardware,
  $184$~ms (Quadrupedal→Differential Rolling) y $534$~ms (Differential Rolling→Quadrupedal)
  (`results.tex:900`/`906`, Fig.~`fig:FourPanelLatencies`).

Estos números **sí** cumplen el propósito retórico original de la oración (evidenciar operación en
tiempo real sin infraestructura de entrenamiento/inferencia de RL o MPC) — de hecho son una base más
fuerte porque son reales, medidos en hardware, con figura y trazabilidad, mientras que "47 ms" no
tenía ninguna.

**Redacción propuesta** (reemplaza la oración citada en §0, envuelta en `\revblue{}` por ser cambio
sustantivo de esta ronda):

> "Its decentralized winner-take-all dynamics enable low-latency conflict resolution between
> competing sensory drives. \revblue{This is evidenced by the near-instantaneous neural decision
> dispatch measured across experimental trials — a deterministic $T_{response} = 0.0$~s in
> simulation (Section~\ref{sec:results}) and $184$–$534$~ms of neural processing latency across 15
> hardware replicates (Section~\ref{sec:results}) — well within real-time constraints on
> resource-constrained embedded hardware,} without requiring the training cycles or inference
> infrastructure associated with deep reinforcement learning or model predictive control frameworks,
> making interpretability and low runtime overhead intrinsic properties of the proposed design."

## 3. Notas de ejecución

1. Aplicar el reemplazo de texto en `methodology.tex:201` tal cual la redacción propuesta en §2.
2. Envolver el fragmento nuevo en `\revblue{}` (cambio sustantivo, no un typo).
3. `scripts/reassemble.py` + `scripts/validate_tex.sh` + `scripts/check_roundtrip.sh` +
   `scripts/compile_pdf.sh` (hay toolchain LaTeX disponible en este entorno).
4. Actualizar la fila `C-15` de `PROGRESS.md` a `applied` (o crear una fila nueva `C-xx` que
   reemplace/cierre `C-15` — decisión al ejecutar, ver `PROGRESS.md` por el estado final).
5. `git mv` este documento a `intake/processed/` una vez aplicado.
6. `push_to_overleaf.sh` (cambia `sections/methodology.tex`, sí requiere sync).
