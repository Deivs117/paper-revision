# R3-01 / R3-02 — Plan de escritura: Basal Ganglia Ablation Study

**Estado (2026-08-31):** plan cerrado, listo para ejecutar el patch. **No reemplaza**
`intake/pending/R3-02_ablation_results_handoff.md` (diagnóstico técnico completo: método, 4 bugs
corregidos, provenance) ni `intake/pending/R3-01-02_ablation_presentation_analysis.md` (análisis de
enfoque). Este documento es la estructuración lista para pegar — 2 figuras ya generadas e
inspeccionadas, pseudo-texto en `\revblue{}`, y checklist de ejecución.

**Origen:** filas `R3-01`/`R3-02` de `PROGRESS.md`. **Owner:** Diego (dato) / a asignar (redacción).

---

## 0. Decisiones de alcance

| Decisión | Elegido | Descartado |
|---|---|---|
| Subsección para R3-01 y R3-02 | Una sola (`Basal Ganglia Ablation Study`), narrativa dividida en dos mitades | Dos subsecciones separadas — duplicaría tabla/figura del mismo dataset |
| Ubicación en `results.tex` | Nueva `\subsubsection` justo después de `\subsubsection{Quantitative Validation: Multi-Modal Simulation Performance}` (línea 153, antes de `Response to Variable Topographies`) | Insertar cerca de `Quantitative Stability Analysis of Locomotion Mode Transitions` (línea 241) — mide algo distinto (transiciones de modo, no ablación) |
| Ubicación en `methodology.tex` | Párrafo corto (solo método) al final de `Basal Ganglia Module`, antes de `\subsubsection{Locomotion Module}` (línea 203) | Nueva subsubsection propia en methodology — es solo 4 líneas de método, no lo amerita |
| Tabla de tasa de éxito | **No** — decisión revisada 2026-08-31 (ver abajo) | Tabla `tabularx` (descartada) |
| Figura de tasa de éxito | Sí, promovida — **un solo panel (Complex Navigation)**, no dos. El panel Appetitive se descartó: las 4 variantes rinden ~92–100% con p=1.000 en las 4 comparaciones — cero separación visual, no aporta información que una tabla o figura no comuniquen mejor que una frase de texto | Panel Appetitive (descartado, 2026-08-31, pedido del autor); tabla de tasa de éxito (descartada — la figura de un panel ya comunica el número exacto y el p de Fisher con más impacto visual que la fila de una tabla) |
| Tabla de métricas continuas (latencia/roll/pitch) | No — se reportan en prosa + la figura de estabilidad, para no duplicar la misma información en tabla y figura | Tabla adicional |
| Figura de estabilidad (roll/pitch RMS, Complex Navigation) | Sí, promovida | — |
| Appetitive (caso sin conflicto), todas las métricas | Una sola frase de texto (91.7–100% de éxito, p=1.000 en las 3 comparaciones; ninguna métrica continua difiere significativamente) — sin tabla ni gráfica | Panel/fila/tabla dedicados |
| λ (`exp_lambda`) | Omitido de toda tabla/figura de resultados; una frase en Limitations | Reportarlo con su valor 1.0 sin contexto |
| `firing_variance`/`temporal_consistency` | No mencionados como dato (no existen) — una frase en Limitations sobre la mejora futura posible | Especular con su efecto probable |

---

## 0bis. Hallazgo de verificación — dirección real de `pitch_rms` (2026-08-31)

**Protocolo aplicado** (mismo que estableció el plan de R3-05, §0bis de ese documento): antes de
escribir cualquier interpretación de una figura/métrica, se generó el gráfico real
(`scripts/plot_ablation.py`, ver §1) y se inspeccionó pixel a pixel contra los datos numéricos
crudos (`output/ablation_stats_summary.csv`), en vez de asumir la lectura que traía el handoff.

**Resultado: la lectura del handoff y del README del experimento ("roll_rms/pitch_rms significativos"
para las 3 variantes, implícitamente en la misma dirección de "más inestable") es correcta para
`roll_rms` pero **incorrecta en dirección para `pitch_rms` en 2 de las 3 variantes**:

| Variante (Complex Navigation) | `roll_rms` vs. `full` | `pitch_rms` vs. `full` |
|---|---|---|
| `no_lateral_inhibition` | **+43.6%**, p<0.001 (peor) | **−11.3%**, p<0.001 (**mejor/menor**, no peor) |
| `no_stn_str` | **+45.9%**, p<0.001 (peor) | **−5.7%**, p=0.0043 (**mejor/menor**, no peor) |
| `threshold_only` | **+22.0%**, p=0.017 (peor) | **+6.4%**, p=0.0029 (peor, consistente) |

Verificado tanto en el CSV (`ci_low`/`ci_high`/`value` por fila) como visualmente en
`output/fig_ablation_complex_stability.png` (panel derecho: las barras naranja y rosa quedan
**por debajo** de la barra azul de control, no por encima).

**Interpretación honesta (no sobreclamada):** `no_lateral_inhibition` y `no_stn_str` — las dos
ablaciones que rompen el circuito de ganglios basales en sí — colapsan la tasa de éxito (25%/33.3%
vs. 100%) y sí degradan `roll_rms`. Su `pitch_rms` más bajo **no** debe presentarse como "mejor
estabilidad de cabeceo"; el patrón más plausible, dado el colapso simultáneo de la tasa de éxito,
es que la mayoría de esos ensayos terminan en fallo/timeout con menor locomoción neta (menos
transiciones de marcha completadas, más tiempo en una sola postura) en vez de ejecutar el ciclo
normal de cabeceo asociado a una navegación exitosa — es decir, un `pitch_rms` menor por **menor
actividad locomotora real**, no por mejor control. Esta es una lectura consistente con los datos
disponibles, no verificada contra trayectorias por ensayo (que no están en este dataset) — el
pseudo-texto de §5 la redacta con ese matiz, sin afirmar causalidad probada.

**Segunda verificación — la línea base `full` de este experimento no es la misma cifra que
`tab:consolidated_simulation_metrics`:** la fila "Complex Navigation" de esa tabla ya publicada
reporta Roll $0.58\pm0.03$°/Pitch $1.12\pm0.04$° (promediado sobre $\sigma\in[0,4]$); el `full` de
este dataset da Roll $0.815\pm0.06$°/Pitch $1.043\pm0.02$° (con `nl` fijo en 0, por diseño — ver
README del experimento). Son la misma métrica y likely el mismo orden de magnitud (confirma que
las unidades son grados, no una escala distinta), pero **no el mismo número** por la diferencia de
condición de ruido — el pseudo-texto de §5 no debe implicar que son intercambiables ni citarlos
juntos como si fueran una sola medición.

---

## 1. Infraestructura de datos — ✅ ejecutada (2026-08-31)

- `experiments/R3-02-wta-vs-threshold/scripts/plot_ablation.py` (nuevo, revisado 2026-08-31) — lee
  `output/ablation_stats_summary.csv`, genera:
  - `output/fig_ablation_success_rate.png` — **un solo panel, Complex Navigation** (el panel
    Appetitive se quitó del script por pedido del autor: sin separación significativa entre
    variantes, se reporta en una frase de texto en vez de gráfica — ver §0 y §2).
  - `output/fig_ablation_complex_stability.png` — roll/pitch RMS, Complex Navigation, 4 variantes,
    barras de error = IC95%, anotación de p de Mann-Whitney.
- Corrido con `experiments/.venv_plotting` (paleta/estilo compartido de `experiments/_plotting/style.py`,
  Okabe-Ito, mismo `.mplstyle` que el resto del repo).
- Ambas imágenes inspeccionadas pixel a pixel (§0bis) — confirman los números del CSV exactamente.

**Pendiente de ejecución (checklist §7):** `promote_figure.sh` de ambas imágenes hacia `assets/`.

---

## 2. Figura de tasa de éxito — especificación e inclusión LaTeX

Generada en `experiments/R3-02-wta-vs-threshold/output/fig_ablation_success_rate.png` — un solo
panel (Complex Navigation, el escenario con conflicto real), 4 barras (Full/No lateral
inhibition/No STN-STR/Threshold only), p de Fisher exact anotado sobre cada barra ablada.
Inspeccionada pixel a pixel: la caída 100%→25%/33.3%/83.3% es visualmente inmediata, más clara que
una fila de tabla.

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.6\textwidth]{fig_ablation_success_rate.png}
    \caption{\revblue{Success rate under real stimulus conflict (Complex Navigation scenario, $n=12$ trials/variant; Fisher's exact test vs. the intact circuit). The two ablations that remove basal-ganglia mechanism itself collapse success rate significantly (\emph{no lateral inhibition}: $25.0\%$, $p<0.001$; \emph{no STN/STR}: $33.3\%$, $p=0.001$); replacing the circuit with static threshold logic degrades success more mildly and not significantly at this sample size (\emph{threshold only}: $83.3\%$, $p=0.478$). Under the no-conflict Appetitive Targeting scenario (not shown), all four variants perform statistically indistinguishably ($91.7$--$100\%$, $p=1.000$ for all three comparisons).}}
    \label{fig:ablation_success_rate}
\end{figure}
```

**Antes de parchear:** correr
`scripts/promote_figure.sh experiments/R3-02-wta-vs-threshold/output/fig_ablation_success_rate.png assets/fig_ablation_success_rate.png`
(checklist §7, paso 2).

---

## 3. Figura de estabilidad — especificación e inclusión LaTeX

Ya generada e inspeccionada (§0bis) en
`experiments/R3-02-wta-vs-threshold/output/fig_ablation_complex_stability.png` — 2 paneles
(Roll RMS, Pitch RMS), 4 barras cada uno (Full/No lateral inhibition/No STN-STR/Threshold only),
barras de error = IC95%, anotación de p de Mann-Whitney vs. `full` sobre cada barra ablada.

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\textwidth]{fig_ablation_complex_stability.png}
    \caption{\revblue{Attitude stability under real conflict (Complex Navigation scenario, $n=12$ trials/variant) across the four basal-ganglia ablation variants. Roll RMS increases significantly for all three ablations relative to the intact circuit (\emph{no lateral inhibition}: $+43.6\%$, $p<0.001$; \emph{no STN/STR}: $+45.9\%$, $p<0.001$; \emph{threshold only}: $+22.0\%$, $p=0.017$). Pitch RMS shows a different pattern: it increases for \emph{threshold only} ($+6.4\%$, $p=0.0029$), consistent with the roll-instability trend, but decreases for \emph{no lateral inhibition} and \emph{no STN/STR} ($-11.3\%$ and $-5.7\%$, both $p<0.005$) --- plausibly reflecting reduced net locomotor activity in trials that fail outright (Figure~\ref{fig:ablation_success_rate}) rather than improved attitude control.}}
    \label{fig:ablation_complex_stability}
\end{figure}
```

**Antes de parchear:** correr
`scripts/promote_figure.sh experiments/R3-02-wta-vs-threshold/output/fig_ablation_complex_stability.png assets/fig_ablation_complex_stability.png`
(checklist §7, paso 2).

---

## 4. `methodology.tex` — pseudo-texto (párrafo de método, sin resultados)

Insertar como párrafo nuevo al final de `\subsubsection{Basal Ganglia Module}`, inmediatamente
después del párrafo existente que termina en "...intrinsic properties of the proposed design."
(línea ~201 al 2026-08-31 — **reverificar con
`grep -n "intrinsic properties of the proposed design" sections/methodology.tex`** antes de editar,
por si otro patch corrió el archivo) y antes de `\subsubsection{Locomotion Module}` (línea 203).

```latex
\revblue{To empirically ground this architectural choice, rather than relying solely on the citations above, an ablation study was conducted on the basal-ganglia circuit itself. An \texttt{ablation\_mode} parameter was introduced into the simulated implementation with four variants: the intact circuit (\emph{full}, control); \emph{no lateral inhibition}, which zeroes the cross-channel inhibitory terms in Eqs.~\eqref{eq:stn}--\eqref{eq:str} (Gpe$\rightarrow$STN, STN$\rightarrow$Gpi) while leaving same-channel dynamics untouched; \emph{no STN/STR}, which removes the STN and STR layers entirely, routing the raw stimulus directly into GPe/GPi with the same per-channel gains STN would otherwise apply; and \emph{threshold-only}, which bypasses the STN/GPi/GPe/STR dynamics altogether in favor of a static fixed-priority threshold over the raw stimulus --- the same threshold-logic family already used elsewhere in this architecture's own Locomotion Module. Each variant was evaluated across the Appetitive Targeting (no-conflict control) and Complex Navigation (three simultaneous, conflicting stimuli) scenarios ($n=12$ replicates/variant/scenario); results are reported in Section~\ref{sec:results}.}
```

---

## 5. `results.tex` — pseudo-texto de la subsección — listo para `\revblue{}`

Insertar como `\subsubsection{Basal Ganglia Ablation Study}` inmediatamente después de
`\end{table}` de `tab:consolidated_simulation_metrics` (línea 153 de `sections/results.tex` al
2026-08-31, confirmada vigente — **reverificar con `grep -n "subsubsection{Response to Variable Topographies}" sections/results.tex`
antes de editar y tomar la PRIMERA ocurrencia (línea 153, dentro de Simulation Results) — el mismo
título de subsubsection se repite en Physical Implementation Results (línea 594), que no es el
punto de inserción**.

```latex
\subsubsection{Basal Ganglia Ablation Study}

\revblue{To directly address the reviewer's request for an ablation analysis of the basal-ganglia arbitration network and a quantitative comparison against simple threshold-based decision logic, the four-variant ablation described in Section~\ref{sec:methodology} was evaluated across the Appetitive Targeting (no-conflict) and Complex Navigation (three-stimulus conflict) scenarios, reusing the same scenario parameters as Table~\ref{tab:consolidated_simulation_metrics} ($n=12$ trials/variant/scenario, noise level fixed at zero to isolate the structural effect of each ablation from sensory-noise robustness, which is characterized separately in Section~\ref{sec:results} for the intact circuit). This study is simulation-only; no equivalent ablation was run on the physical platform.}

\revblue{Without stimulus conflict, all four variants perform statistically indistinguishably: $91.7$--$100\%$ success in the Appetitive Targeting scenario, $p=1.000$ for all three comparisons against the intact circuit --- removing an ablation target does not break the simple case, as expected when only one channel is ever active. Under real conflict (Complex Navigation, Figure~\ref{fig:ablation_success_rate}), a clear gradient emerges. The two ablations that remove basal-ganglia mechanism itself --- \emph{no lateral inhibition} (inhibitory connections) and \emph{no STN/STR} (neural layers) --- collapse the success rate to $25.0\%$ and $33.3\%$ respectively (Fisher's exact $p<0.001$ and $p=0.001$ vs.\ the intact circuit's $100\%$), directly addressing the reviewer's request to quantify the consequence of removing inhibitory connections or key neural layers (R3-01). Replacing the entire circuit with static threshold logic (\emph{threshold only}) degrades success more mildly and not significantly on this metric alone ($83.3\%$, $p=0.478$); the case against threshold logic instead rests on the continuous metrics below.}

% FIGURA fig:ablation_success_rate va aquí (ver §2)

\revblue{Decision latency under conflict is unaffected by removing basal-ganglia mechanism ($81.7$~ms, 95\%~CI $[56.9, 106.4]$, for \emph{no lateral inhibition}, $p=0.34$; $66.6$~ms, 95\%~CI $[41.9, 91.2]$, for \emph{no STN/STR}, $p=0.84$; vs.\ $75.9$~ms, 95\%~CI $[59.3, 92.6]$, for \emph{full}), but is significantly slower under \emph{threshold only} ($109.1$~ms, 95\%~CI $[89.2, 129.0]$, $p=0.014$) --- consistent with a static threshold lacking the anticipatory, continuously-converging dynamics the WTA circuit provides during conflict resolution. Roll RMS increases significantly for all three ablations relative to the intact circuit ($+43.6\%$ \emph{no lateral inhibition}, $p<0.001$; $+45.9\%$ \emph{no STN/STR}, $p<0.001$; $+22.0\%$ \emph{threshold only}, $p=0.017$), indicating that attitude destabilization under conflict is a shared consequence of weakening the arbitration mechanism, regardless of which component is removed. Pitch RMS instead diverges by ablation type (Figure~\ref{fig:ablation_complex_stability}): it increases for \emph{threshold only} ($+6.4\%$, $p=0.0029$), consistent with the roll-instability trend, but decreases for \emph{no lateral inhibition} and \emph{no STN/STR} ($-11.3\%$ and $-5.7\%$, both $p<0.005$) --- plausibly a symptom of reduced net locomotor activity in the majority of trials that fail outright under these two ablations, rather than improved attitude control.}

% FIGURA fig:ablation_complex_stability va aquí (ver §3, distinta de la de §2)

\revblue{Taken together, these results support the winner-take-all arbitration design on two separable grounds. First, the basal-ganglia circuit's own mechanism --- not merely the presence of \emph{some} priority rule --- is responsible for resolving genuine multi-stimulus conflict: disabling its inhibitory connections or removing its neural layers each independently collapses success rate and roll stability under conflict, with neither degrading decision latency (R3-01). Second, replacing that mechanism with the same family of static threshold logic already used elsewhere in this architecture's Locomotion Module is measurably worse specifically where the WTA circuit's continuous dynamics matter most: it is the only variant that significantly slows decision-making under conflict, in addition to degrading attitude stability (R3-02) --- though, as noted above, this comparison is supported by latency and attitude metrics rather than by success rate alone, which did not reach significance at this sample size.}
```

**Nota de extensión:** ~340 palabras de prosa + 2 figuras — similar en tamaño al plan de R3-05. Si
el crecimiento de `results.tex` se ve ajustado en la revisión final
(`scripts/check_word_growth.sh`), el primer candidato a recortar es la oración de latencia
(números completos con IC ya están en el CSV, podrían moverse a una nota al pie).

---

## 6. Limitaciones — texto a agregar a `\label{ssec:Limitations}` (no repetir inline)

Insertar como párrafo nuevo en `results.tex`'s `\subsection{Limitations of the Present Work}`
(~línea 902+, después del párrafo consolidado por `R2-03`):

```latex
\revblue{Regarding the basal-ganglia ablation study (Section~\ref{sec:results}): the conflict-efficiency metric $\lambda$ was excluded from the reported results because its current implementation only registers active conflict when two specific channels are simultaneously present within the sampling window, a condition rarely met in practice across these trials --- this is a limitation of the metric's present instrumentation, not evidence that conflict efficiency is unaffected by the ablations. Additionally, per-cycle firing-variance and temporal-consistency diagnostics, which could further characterize the \emph{threshold-only} variant's failure mode (e.g.\ oscillation near the decision boundary, as opposed to outright deadlock), were not captured for this dataset; the threshold-versus-WTA comparison therefore relies on decision latency and attitude stability rather than on these more targeted diagnostics.}
```

---

## 7. Checklist de ejecución

1. Reverificar líneas de inserción (`methodology.tex` línea ~201, `results.tex` línea ~153 y
   ~902+) — pueden haber corrido si otro patch tocó esos archivos desde 2026-08-31.
2. `scripts/promote_figure.sh experiments/R3-02-wta-vs-threshold/output/fig_ablation_success_rate.png assets/fig_ablation_success_rate.png`
   y `scripts/promote_figure.sh experiments/R3-02-wta-vs-threshold/output/fig_ablation_complex_stability.png assets/fig_ablation_complex_stability.png`
3. Insertar el párrafo de §4 en `sections/methodology.tex`.
4. Insertar el bloque de §5 (subsubsection + figura de §2 + figura de §3) en `sections/results.tex`.
5. Insertar el párrafo de §6 en `sections/results.tex`'s `\label{ssec:Limitations}`.
6. `scripts/reassemble.py` → `scripts/validate_tex.sh` → `scripts/check_roundtrip.sh` → (opcional) `scripts/compile_pdf.sh`.
7. `scripts/check_hardcoded_refs.sh` / `scripts/check_target_conflicts.sh` (advisory) antes de commitear.
8. Registrar el patch en `patches/r3-01-02-basal-ganglia-ablation-study.tex`.
9. Actualizar `PROGRESS.md`: filas `R3-01` y `R3-02` de `pending` a `drafted` (luego `applied` una
   vez el patch esté aplicado), con `Patch file` apuntando al archivo de §7.8 y `Data source` ya
   apuntando a `experiments/R3-02-wta-vs-threshold/` (R3-01) y lo mismo (R3-02, ya está así en la
   tabla actual).
10. `scripts/push_to_overleaf.sh` cuando corresponda (flujo normal pull-guard/validate/push).
11. `git mv` a `intake/processed/`: `R3-02_ablation_results_handoff.md`,
    `R3-01-02_ablation_presentation_analysis.md`, y este mismo archivo — una vez `R3-01`/`R3-02`
    lleguen a `applied` o más (regla de `intake/SOURCES.md`).

---

## 8. Abierto / fuera de alcance de este plan

- **Arreglar `_compute_lambda_efficiency()` o capturar `firing_variance`/`temporal_consistency`**
  (backlog del handoff original) — no se hace aquí; ver §5 del análisis previo
  (`R3-01-02_ablation_presentation_analysis.md`) para la recomendación de no bloquear esta
  redacción en esa mejora.
- **Ablation física** (solo simulación en este dataset) — mencionado como alcance explícito en el
  primer párrafo de §5, no una tarea pendiente de este plan.
