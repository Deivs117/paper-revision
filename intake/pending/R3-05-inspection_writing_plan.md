# R3-05 — Plan de escritura: Reactive Inspection Task (Experimento E)

**Estado (2026-08-29):** plan cerrado, listo para ejecutar el patch. **No reemplaza**
`intake/pending/R3-05_inspection_handoff.md` — ese documento sigue siendo la fuente del
diagnóstico técnico completo (por qué no se mide coverage rate, análisis del código
`red_neuronal.py`, definición operativa del evento de evasión). Este documento es la
**estructuración previa a escribir**: tabla, figura, pseudo-texto listo para pegar en
`\revblue{}`, y el checklist de ejecución — derivado de una conversación con el autor para
zanjar las decisiones de alcance que el handoff dejaba abiertas.

**Origen:** fila `R3-05` de `PROGRESS.md`. **Reviewer:** #3.5 (HIGH). **Owner:** Deivi.

---

## 0. Decisiones de alcance acordadas con el autor (2026-08-29)

| Decisión | Elegido | Descartado |
|---|---|---|
| Forma de la tabla principal | Tabla agregada (μ±σ/min/max sobre los 17 éxitos) + SR aparte | Tabla completa de 20 filas |
| Figura nueva | Sí — un scatter, un solo panel | Ninguna figura / figura de trayectoria tipo `fig:RES_EST_MUL` |
| Relación con `tab:consolidated_simulation_metrics` | Tabla nueva independiente (columnas no coinciden: `d_final`/`N_lidar`/`T_acquisition` no existen ahí) | Forzar el Experimento E como quinta fila de esa tabla |
| Hallazgo "dos modos de navegación" (§9.3 del handoff) | Sí, 2-3 líneas de prosa, ligado directamente al análisis de fallos | Cortarlo |
| Definiciones de métrica (`d_final`, `N_lidar`, `T_acquisition`) | Definición local en esta subsección, siguiendo el patrón ya usado en el resto de `results.tex` | Abrir ahora la consolidación cross-secciones que pide R2 (tarea propia, mayor, fuera de alcance aquí) |
| Las 4 limitaciones del handoff §8 | Van a `\label{ssec:Limitations}` (consolidado existente), **no** repetidas inline en la subsección nueva | Repetirlas en la subsección nueva |
| Procedencia del código | `PETER_SIMULATION`, rama `sam`, commit `6d5a2e6` — registrado en `intake/SOURCES.md` | — |
| Estructura de `experiments/` | `experiments/R3-05-inspection/{data,scripts,output}` (ya ejecutado, ver §1) | Dejar el volcado plano `experiments/R3-05_inspection_results/` |

**Razón de la tabla independiente (no fusionar con `tab:consolidated_simulation_metrics`):** esa
tabla reporta Success/T_sim/Roll/Pitch para las 4 suites de estímulo único — atributos de
estabilidad cinemática. El Experimento E no reporta esas columnas (el robot permanece en modo H
todo el ensayo, sin transición de marcha — `stability_log.csv` vacío en los 20 trials, ver §9.7
del handoff) y en cambio reporta columnas que ninguna otra suite tiene (`d_final`, eventos LiDAR,
tiempo de adquisición visual). Forzarlo en la tabla existente perdería exactamente la información
que responde al reviewer.

**Razón de no repetir las limitaciones inline:** el Referee 2 pide explícitamente "consolidate all
limitations into a dedicated section" — ya existe `\subsection{Limitations of the Present Work}`
(`\label{ssec:Limitations}`, `sections/results.tex` línea ~910) con contenido de la misma
naturaleza (restricciones de hardware, de entorno de simulación, de fusión sensorial). Repetir las
4 limitaciones del handoff §8 dentro de la subsección nueva sería exactamente el tipo de
restatement que el Referee 2 pide cortar en la instrucción citada en el encabezado de esta tarea.

---

## 1. Infraestructura de datos — ✅ ya ejecutada (2026-08-29)

- `git mv experiments/R3-05_inspection_results/ → experiments/R3-05-inspection/data/` (sin cambios
  de contenido, solo de ruta, para alinear con la convención `experiments/<ID>-<slug>/` de
  `README.md` §9.1).
- `experiments/R3-05-inspection/README.md` — goal/method/provenance/regeneración, según plantilla.
- `experiments/R3-05-inspection/scripts/aggregate_and_plot.py` — genera:
  - `output/inspection_summary_stats.csv` (μ/σ/min/max de `d_final_m`, `N_lidar_events`,
    `N_mode_X_events`, `T_acquisition_s`, `sim_time_s` sobre los 17 éxitos, más SR).
  - `output/fig_dfinal_vs_nlidar.png` (scatter, ver §3).
- Ejecutado y verificado: los números del CSV coinciden exactamente con la §9.6 del handoff
  (`d_final`=1.076±0.038, `N_lidar`=7.71±6.42, `N_mode_X`=3.29±2.80, `T_acquisition`=32.2±14.1,
  `sim_time`=51.6±12.3, n=17; SR=85% sobre n=20).
- `intake/SOURCES.md` actualizado con la nota de procedencia (rama `sam`@`6d5a2e6`).

**Pendiente de ejecución (no hecho todavía, ver checklist §6):** `promote_figure.sh` de
`output/fig_dfinal_vs_nlidar.png` hacia `assets/`.

---

## 2. Tabla — especificación LaTeX lista para pegar

```latex
\begin{table}[htbp]
\centering
\caption{\revblue{Reactive Inspection Task --- Aggregate Performance Metrics (Experiment E, 17/20 successful trials, obstacle field with initially non-visible target).}}
\label{tab:inspection_metrics}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Metric} & \textbf{Mean $\pm$ SD} & \textbf{Min} & \textbf{Max} \\
\midrule
$d_{final}$ (m)              & 1.076 $\pm$ 0.038 & 0.991 & 1.130 \\
$N_{lidar\_events}$          & 7.71 $\pm$ 6.42   & 4     & 28    \\
$N_{mode\_X\_events}$        & 3.29 $\pm$ 2.80   & 1     & 10    \\
$T_{acquisition}$ (s)        & 32.2 $\pm$ 14.1   & 20.7  & 70.8  \\
$T_{task}$ (s)               & 51.6 $\pm$ 12.3   & 42.8  & 86.8  \\
\bottomrule
\end{tabularx}
\\[2pt]
{\footnotesize Success rate: 17/20 (85\%); three timeouts at 90~s (trials 7, 11, 17), analyzed below. Statistics computed over the 17 successful trials only.}
\end{table}
```

Mismo estilo tabular (`tabularx` + `booktabs`) que `tab:consolidated_simulation_metrics` para
consistencia visual. Fuente de los números: `experiments/R3-05-inspection/output/inspection_summary_stats.csv`.

---

## 3. Figura — especificación e inclusión LaTeX

Ya generada en `experiments/R3-05-inspection/output/fig_dfinal_vs_nlidar.png` (scatter de un panel,
17 puntos, `N_lidar_events` en X vs `d_final_m` en Y, color/forma por patrón limpio
(`N_lidar_events < 10`, círculo azul, n=12) vs elevado (`N_lidar_events ≥ 10`, triángulo naranja,
n=5) — paleta Okabe-Ito del repo vía `experiments/_plotting/style.py`). Muestra visualmente que
`d_final` se mantiene en un rango comparable independientemente de cuántos eventos de evasión tomó
el recorrido — la evidencia visual directa de la robustez del criterio de parada.

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.7\textwidth]{fig_inspection_dfinal_vs_nlidar.png}
    \caption{\revblue{Final approach precision ($d_{final}$) versus sensory evasion-event count ($N_{lidar\_events}$) across the 17 successful Reactive Inspection Task trials, split into a clean-traversal pattern ($N_{lidar\_events} < 10$, $n=12$) and an elevated-evasion pattern ($N_{lidar\_events} \geq 10$, $n=5$). $d_{final}$ remains within a comparable range across both patterns despite the roughly $5\times$--$7\times$ spread in evasion-event count, indicating that final approach precision is robust to route complexity.}}
    \label{fig:inspection_dfinal_scatter}
\end{figure}
```

**Antes de parchear:** correr `scripts/promote_figure.sh experiments/R3-05-inspection/output/fig_dfinal_vs_nlidar.png assets/fig_inspection_dfinal_vs_nlidar.png` (checklist §6, paso 2).

---

## 4. Pseudo-texto de la subsección — listo para `\revblue{}`

Insertar como `\subsubsection{Reactive Inspection Task}` inmediatamente antes de
`\subsection{Physical Implementation Results}` (línea 471 de `sections/results.tex` al
2026-08-29 — **reverificar el número de línea antes de editar**, puede haber corrido si otro
patch se aplicó antes).

```latex
\subsubsection{Reactive Inspection Task}

\revblue{To directly address the reviewer's request for inspection-oriented task indicators, a dedicated experiment (Experiment E) evaluates the platform's behavior in a purpose-built obstacle field (\texttt{obstaculos.world}) where a visual target is not visible from the robot's initial pose and only enters the field of view after traversing three static capsule obstacles. Twenty independent trials were executed with a 90~s timeout and no artificial noise injection.}

\revblue{The system does not implement deliberate path planning: it builds no map, retains no spatial memory, and does not compute a global re-route when blocked. What it implements instead is reactive re-routing driven by the basal-ganglia/Winner-Take-All (BG/WTA) arbitration network, which integrates LiDAR and camera information in real time to laterally evade each obstacle while continuing toward the target once visible. Coverage rate --- the percentage of a predefined inspection area visited --- is not reported here, as it presupposes a coverage planner and a known target area that this reactive architecture neither has nor requires (see Section~\ref{ssec:Limitations}). Instead, task-completion indicators that are both measurable with the existing instrumentation and consistent with the system's actual capabilities are used: success rate (SR), final approach precision ($d_{final}$), and time to first visual acquisition of the target ($T_{acquisition}$).}

\revblue{$d_{final}$ is the Euclidean distance between the robot and the target at the instant the inspection-stop neuron activates ($X_{17} > 0.25$, sustained 2~s); $N_{lidar\_events}$ counts sensory-level obstacle-detection transitions (LiDAR channel crossing its 0.3 activation threshold); $N_{mode\_X\_events}$ counts the resulting omnidirectional-mode switches, gated by a 3~s dwell-time hysteresis; $T_{acquisition}$ is the simulation time from post-warmup to the target's bounding-box area first exceeding the visibility threshold.}

\revblue{Twenty trials yielded SR $= 85\%$ (17/20), with three timeouts (trials 7, 11, 17) discussed below. Among the 17 successful trials, $d_{final} = 1.076 \pm 0.038$~m (Table~\ref{tab:inspection_metrics}), directly addressing the reviewer's request for target tracking accuracy: the BG$\rightarrow X_{17}$ loop converges to essentially the same stopping distance from the target regardless of the route taken to reach it.}

% TABLA tab:inspection_metrics va aquí (ver §2)

\revblue{The 17 successful trials separate into two navigation patterns distinguished by $N_{lidar\_events}$: a clean pattern ($n=12$, $N_{lidar\_events} = 4$--$7$, close to one detection per capsule) and an elevated-evasion pattern ($n=5$, $N_{lidar\_events} = 11$--$28$, additional evasive maneuvering before finding a route toward the target). Both patterns converge to a comparable $d_{final}$ (Figure~\ref{fig:inspection_dfinal_scatter}), confirming the stopping criterion is robust to route complexity. The three timeouts are extreme cases of the elevated pattern ($N_{lidar\_events} = 18$, $27$, $33$): in all three, the target was visually detected ($T_{acquisition}$ non-null) but the appetitive channel never accumulated sufficient sustained activation to trigger $X_{17}$ before the deadline, as competing obstacle-channel activation persisted throughout. This is consistent with the architecture's known limitation --- reactive navigation without spatial memory can fail under unfavorable dynamic configurations (Section~\ref{ssec:Limitations}) --- rather than a failure of the inspection-stop mechanism itself.}

% FIGURA fig:inspection_dfinal_scatter va aquí (ver §3)

\revblue{This experiment also provides quantitative evidence responding to the reviewer's request for autonomous re-planning after obstacle blockage: across the 17 successful trials, the sensory-level obstacle signal transitioned $N_{lidar\_events} = 7.71 \pm 6.42$ times on average, while the resulting behavioral mode change transitioned only $N_{mode\_X\_events} = 3.29 \pm 2.80$ times --- $\approx 2.3\times$ fewer mode changes than sensory detections, in every one of the 17 successful trials without exception. This demonstrates that the WTA arbitration converts repeated raw sensory fluctuations into a smaller number of sustained behavioral commitments, avoiding the mode-dithering a simple threshold-triggered controller would exhibit --- the mechanism underlying the reactive re-routing observed in this task.}

\revblue{The target was first visually acquired, on average, $T_{acquisition} = 32.2 \pm 14.1$~s into the trial. This is a first-acquisition metric, not re-acquisition, since the target is not visible from the initial pose in this scenario (Section~\ref{ssec:Limitations}). Visual pursuit is itself conditioned on the absence of a frontal obstacle: during evasion it is suspended, resuming automatically once the obstacle clears --- the system's re-acquisition-like behavior. The robot remained in the wheeled/differential locomotion mode (H) throughout all 20 trials, so no gait-transition stability data applies to this experiment.}
```

**Nota de extensión:** el bloque completo son ~330 palabras de prosa + 1 tabla + 1 figura. Es
consistente con "brevedad prioritaria" del handoff §0, pero si en la revisión final el conteo de
`results.tex` (`scripts/check_word_growth.sh`) se ve ajustado, los párrafos candidatos a recortar
primero son el segundo (definiciones formales de métrica — podrían moverse a una nota al pie de la
tabla) y el último (re-acquisition/modo H — es la parte más "adicional", no responde directamente
a las 3 cláusulas del reviewer).

---

## 5. Ubicación de las limitaciones (no repetir inline)

Las 4 limitaciones del handoff §8 se agregan como oraciones nuevas dentro de
`\subsection{Limitations of the Present Work}` (`\label{ssec:Limitations}`,
`sections/results.tex` ~línea 910), no en la subsección nueva. Redacción propuesta (a insertar
como párrafo nuevo en esa subsección, después del párrafo que ya habla de fusión sensorial/
iluminación):

```latex
\revblue{Regarding the Reactive Inspection Task (Experiment E): the platform performs no deliberate path planning, builds no map, and does not compute a global re-route when blocked --- obstacle traversal emerges from local BG/WTA dynamics rather than global trajectory planning. Coverage rate as a formal area-inspection metric was not evaluated, as it presupposes an explicit coverage planner outside this work's scope; task-completion indicators (success rate, final approach precision, time to first visual acquisition) are reported instead. Visual target pursuit is conditioned on the absence of a frontal obstacle, suspending during evasion and resuming automatically once cleared. Finally, in the obstacle-field scenario used for this experiment the target is not visible from the initial pose, so the reported acquisition metric characterizes first acquisition rather than re-acquisition after occlusion.}
```

---

## 6. Checklist de ejecución (para cuando se abra el patch)

1. Reverificar línea de inserción en `sections/results.tex` (`grep -n "Physical Implementation Results" sections/results.tex`) por si otro patch corrió el archivo desde el 2026-08-29.
2. `scripts/promote_figure.sh experiments/R3-05-inspection/output/fig_dfinal_vs_nlidar.png assets/fig_inspection_dfinal_vs_nlidar.png`
3. Insertar el bloque de §4 (subsubsection + tabla de §2 + figura de §3) en `sections/results.tex`.
4. Insertar el párrafo de §5 en `\label{ssec:Limitations}`.
5. `scripts/reassemble.py` → `scripts/validate_tex.sh` → `scripts/check_roundtrip.sh` → (opcional) `scripts/compile_pdf.sh`.
6. `scripts/check_word_growth.sh` — revisar que el crecimiento de `results.tex` sea proporcional al contenido nuevo, no restatement.
7. Registrar el patch en `patches/r3-05-reactive-inspection-task.tex`.
8. Actualizar `PROGRESS.md`: `R3-05` de `drafted` a `applied` (y `Patch file` con la ruta de arriba).
9. `scripts/push_to_overleaf.sh` cuando corresponda (sigue el flujo normal de pull-guard/validate/push).
10. `git mv intake/pending/R3-05_inspection_handoff.md intake/processed/` y este mismo archivo, una vez el patch llegue a `applied` o más (regla de `intake/SOURCES.md`).

---

## 7. Abierto / fuera de alcance de este plan

- **Consolidación cross-secciones de definiciones de métrica** (pedido general de R2, "merge
  unified metric definitions") — no se resuelve aquí; este plan define `d_final`/`N_lidar`/
  `T_acquisition` localmente, siguiendo el patrón ya existente en el resto de `results.tex`. Si se
  abre esa tarea más adelante, este bloque es uno de los candidatos a revisar.
- El desajuste `repetitions: 15` (handoff §6.1, ejemplo) vs `repetitions: 20` (real, en
  `experiments_config.yaml` de la rama `sam` y en los datos entregados) es cosmético — no afecta
  ningún número de este plan, que usa siempre los 20 trials reales.
