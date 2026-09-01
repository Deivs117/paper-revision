# Auditoría + Plan de Estructuración — R2-02 (FSM Gait Arbitration Baseline)

**Estado:** análisis/planificación únicamente. No se ha movido, renombrado ni editado ningún
archivo de `experiments/`, `sections/`, `patches/` ni `PROGRESS.md` todavía.

**Origen:** auditoría de `experiments/R2-02_fsm_results/` (5 familias FSM entregadas: apetitivo,
aversivo, obstáculo, compleja, inspección) + verificación exhaustiva de
`intake/pending/R2-02_fsm_baseline_reference.md` (758 líneas, documento de referencia que el
equipo ya dejó preparado) contra los datos crudos y el código fuente real, para responder al
comentario de Reviewer #2: *"Add finite state machine (FSM) gait arbitration baseline comparisons
under identical experimental conditions."*

---

## 1. Lo que ya existe — no hay que reinventarlo

El documento de referencia (`R2-02_fsm_baseline_reference.md`) es, a diferencia de R3-04, un
análisis **ya terminado y muy profundo** para las 5 familias con datos disponibles: arquitecturas
comparadas, infraestructura de pruebas, métricas, resultados con interpretación mecanicista
familia por familia, síntesis comparativa, notas de redacción, e incluso un párrafo de respuesta
al referee listo para copiar. También trae instructivos completos (§9-11) para las 2 familias de
terreno que faltan (C1/C2) — **no dupliqué esos instructivos aquí**, ver ese documento
directamente cuando llegue el momento de ejecutarlos.

Mi aporte en esta auditoría es: (a) verificar que las cifras del documento sean fieles a los datos
crudos (no una alucinación ni un error de cálculo), (b) verificar la descripción de la arquitectura
FSM contra el código fuente real (no solo confiar en la prosa del equipo), (c) identificar qué
pipeline reproducible falta construir para que las tablas/figuras no vivan solo como texto Markdown
manual, y (d) las preguntas abiertas antes de construir nada.

---

## 2. Verificación de exactitud — todo lo revisado coincide

**Arquitectura FSM vs. código fuente real** (`PETER_SIMULATION`, rama `fsm`, commit
`10e8aac9c480a31ac21003a411e7382717b595bb`, `ros2_ws/src/peter_robot/src/fsm_gait_arbitration.py`):
confirmado línea por línea contra el bloque de arbitraje real (líneas ~524-565): reglas de
prioridad exactas (`pitch>Upitch→H`, `terrainchanger→C`, `G>0→X` persist 6s, `R>0.5→C` persist 6s,
`B>0.5→H` persist 4s, default H), parámetros ROS (`nl`, `ignore_imu_terrain` default `True`,
`usigma_az` default `100.0`), `Upitch=1`. Todo coincide exactamente con la Sección 1.2 del
documento del equipo — no hay alucinación ni desactualización.

**Cifras spot-checked contra los datos crudos** (recalculadas independientemente desde
`trial_summary.json`, no confiando en el markdown del equipo):

| Claim del documento | Verificado | Resultado |
|---|---|---|
| A-Apetitivo FSM: N=15, 100%, sim_time 39.0±1.8, roll_rms 0.526±0.003, tswitch 0.0054±0.001 | ✅ | sim_time=38.964±1.833, roll_rms=0.5255±0.0032, tswitch=0.0054±0.0013 — coincide |
| B-Compleja FSM: 0/15 SUCCESS (14× TIMEOUT + 1× TIPOVER) | ✅ | Confirmado exacto, incluido el único TIPOVER en trial 12 |
| C1-Terreno Neural: 15/15, sim_time 35.0±3.4 | ✅ | 34.91±3.41 — coincide |

**Origen de los datos "Neural" (columna de comparación) — confirmado, no asumido:**
- Familias A1-A3/B: `experiments/simulation/` (el dataset viejo, ya usado por `macro_robustness.py`
  en el pipeline de R3-04) — conteos de trial coinciden exactamente (19/17/15/15).
- Familia E (inspección): **`experiments/R3-05-inspection/data/`** — el mismo dataset que ya
  produjo `fig_dfinal_vs_nlidar.png` para la fila `R3-05`, **ya publicado y `synced-to-overleaf`
  en el paper actual**. N=20 coincide exactamente. **Implicación importante:** la comparación FSM
  de la Familia E no es un experimento nuevo del lado neuronal — reutiliza datos que el lector ya
  vio en otra sección del paper. Hay que decidir cómo presentarlo sin duplicar contenido (ver
  Pregunta 3).
- C1/C2 (terreno): también `experiments/simulation/familia_c1_terreno_rugoso`/`familia_c2_pendiente`
  — mismo dataset detrás de `FigA/B/C_*.png` (R3-04's `ecdf_phase_space.py`).

---

## 3. Auditoría de calidad de datos — qué es útil y qué no

| Campo | Veredicto | Razón |
|---|---|---|
| `stability_log.csv` | **Inconsistente entre familias, no confiar en su cobertura** | `familia_a_apetitivo_fsm`: 0/15 archivos con datos. `familia_a_obstaculo_fsm`: 1/15. `familia_a_aversivo_fsm`, `familia_b_compleja_fsm`, `familia_e_inspeccion_fsm`: 15/15 o 20/20 (completos). Mismo patrón de brecha que R3-04 — el documento de referencia **ya evitó depender de este archivo** en su análisis (usa `roll_rms`/`pitch_rms` de `trial_summary.json` en su lugar), así que no hay nada que corregir, solo confirmar que esa decisión fue correcta. |
| `exp_lambda` (campo único en `trial_summary.json.final_metrics`) | **Constante en 1.0, no usar para el argumento de conflicto** | Verificado: siempre `1.0` en Familia B, igual que en R3-04. **No es el mismo campo** que el documento cita como "λ-eficiencia en conflicto: 0.982 vs 0.837" (Sección 5.2) — ese viene de la serie temporal `lambda_efficiency` de `metrics_raw.csv` (rango real 0.0-1.0, verificado), promediada durante la ventana de conflicto, no del valor final del trial. **Dos campos con nombre similar, semántica distinta** — al redactar, aclarar explícitamente que la cifra 0.982/0.837 es un promedio de serie temporal durante una ventana específica (el equipo debe confirmar exactamente cómo definió esa ventana si se va a citar el número con precisión metodológica), no el resumen final del trial. |
| Nombres de carpeta (`familia_a_apetitivo_fsm`, `test_NNN_SUCCESS`) | **No citar crudos en prosa** | Misma regla README §11.1 ya aplicada en R3-04 — describir funcionalmente ("la familia FSM de aproximación apetitiva"), nunca el nombre de carpeta. |

**No se encontraron datos fabricados ni inconsistencias entre lo documentado y lo real** — a
diferencia de la auditoría inicial de R3-04 (que sí encontró una incertidumbre real sin resolver
sobre `pruebaDeTerreno`), aquí la única precisión necesaria es la distinción de los dos campos
`lambda`.

---

## 4. Qué falta construir — pipeline reproducible (hoy todo vive como Markdown manual)

El documento de referencia calculó todas sus tablas/estadísticas ad hoc (probablemente con scripts
sueltos no conservados) — no hay ningún script en el repo que regenere la Tabla Maestra §7.1, la
gráfica SR-vs-NL, ni las figuras de timeline modal que el propio documento pide en §8.1. Antes de
que la sesión de escritura use estas cifras, conviene que existan como algo ejecutable y
versionado, mismo criterio que se aplicó en R3-04:

| Pieza pedida por el equipo (§8.1) | Estado | Qué falta |
|---|---|---|
| Tabla maestra §7.1 (SR, sim_time, roll_rms, λ-efic. por familia × sistema) | Solo Markdown manual en el intake doc | Script que la recalcule desde `experiments/simulation/` + `experiments/R2-02_fsm_results/` + `experiments/R3-05-inspection/data/` |
| Gráfica SR vs. nivel de ruido (Familias A) | No existe como imagen | Nuevo builder, mismo patrón que `experiments/_plotting/builders/` |
| Timeline modal — Familia B (neural vs. FSM, función escalonada del modo en el tiempo) | No existe | Nuevo builder — lee la columna `mode` de `metrics_raw.csv` por timestep |
| Timeline modal — Familia E (mismo formato) | No existe | Ídem |
| Conteo de dithering de modo (§10.3, para C1/C2 cuando lleguen) | Función Python ya escrita en el propio intake doc, no integrada a ningún script del repo | Portar a `experiments/_plotting/` o al script del experimento cuando C1/C2 estén listos |

No hay builder existente en `experiments/_plotting/builders/` que produzca timelines modales o
comparaciones SR-vs-NL — confirmado por búsqueda exhaustiva. Sería trabajo nuevo, no una extensión
de algo existente (a diferencia de R3-04, donde el pipeline ya existía parcialmente).

---

## 5. Reorganización pendiente (mismo criterio que R3-04)

`experiments/R2-02_fsm_results/` no sigue la convención `_TEMPLATE` (`<ID>-<slug>/README.md/
config.yaml/data/output/scripts`) — es solo las 5 carpetas `familia_*_fsm/` crudas, sin
`README.md` ni separación `data/`/`output/`. Análogo a como estaba `R3-04_simulation/` antes de
reorganizarla. Plan (no ejecutado): renombrar a `experiments/R2-02-fsm-baseline/`, mover las 5
familias a `data/` (gitignored), documentar en `README.md` la proveniencia (commit
`10e8aac9` de `PETER_SIMULATION` rama `fsm`) y que **reutiliza** `experiments/simulation/` +
`experiments/R3-05-inspection/data/` como el lado "Neural" de la comparación (no los duplica).

---

## Preguntas — resueltas 2026-09-01

1. **RESUELTO: construir ya el pipeline reproducible para las 5 familias completas** (A×3, B, E).
   Se extenderá cuando lleguen C1/C2, mismo patrón "Ronda 1/Ronda 2" que funcionó bien en R3-04.

2. **RESUELTO: Familia E amplía la subsección `R3-05` ya existente en `results.tex`** (columna/
   curva FSM añadida a lo ya publicado), en vez de crear una subsección separada — evita duplicar
   la figura `fig_dfinal_vs_nlidar.png` ya publicada.

3. **Investigado — hallazgo, no totalmente resuelto.** La fórmula de λ SÍ está documentada en
   código: `PETER_SIMULATION` rama `fsm`, `neural_recorder.py::_compute_lambda_efficiency()`
   (+ `docs/README_experiments.md` §"Eficiencia de resolución de conflictos λ"): `λ=1.0` sin
   conflicto (no ambos rojo+azul presentes); con conflicto, `λ = |cmd_vel| / (‖actividad
   neuronal‖ + ε)`, acotado [0,1]. **Pero la cifra citada (0.982 Neural / 0.837 FSM) no se
   reprodujo exactamente** al recalcularla desde los CSV crudos con las dos interpretaciones más
   naturales:
   - Promedio de **todo el trial** (incluye instantes sin conflicto, que valen 1.0 por
     definición): Neural=0.976, FSM=0.943 — en el rango correcto, pero no exacto.
   - Promedio **solo de instantes con conflicto real** (`red_present` Y `blue_present`
     simultáneos): Neural=0.034, FSM=0.006 — muy lejos de 0.982/0.837.

   No se inventó una tercera forma de agregación para forzar el número. **Queda pendiente que el
   autor confirme con el equipo el criterio exacto de agregación** — la fórmula per-timestep es
   confiable y reproducible, pero el promedio reportado específico no. Mientras tanto, el pipeline
   de esta sección recalculará y expondrá **ambos** promedios (todo-el-trial y solo-conflicto) de
   forma transparente, dejando explícito cuál es cuál, en vez de citar 0.982/0.837 sin poder
   defenderlos.

4. **RESUELTO: C1/C2 aún no se han lanzado.** Seguimos en el punto que describe el documento del
   equipo (§9) — sin acción inmediata de mi parte; se coordina con el equipo de simulación cuando
   corresponda.

---

## 6. Pipeline construido esta sesión

Reorganizado `experiments/R2-02_fsm_results/` → `experiments/R2-02-fsm-baseline/`
(`data`/`output`/`scripts`, `README.md`, `config.yaml` con el mapeo explícito Neural↔FSM por
familia). Tres scripts nuevos en `scripts/`, ejecutados y verificados:

| Script | Salida | Verificación |
|---|---|---|
| `build_master_table.py` | `table_master_comparison.csv` | Recalcula SR/sim_time/roll_rms/λ (dos agregaciones) por familia × sistema, con las 2 familias de terreno marcadas `pending`. **Corregido un bug propio durante la verificación:** la primera versión deduplicaba intentos por `trial_index` (copiando una convención de `macro_robustness.py` pensada para otra tabla), inflando artificialmente la tasa de éxito en familias con reintentos (p.ej. Aversive Neural habría salido 100% en vez del 88.2% real). Corregido a contar carpetas crudas, igual que hace el documento del equipo. Tras el fix, `n_attempted`/`success_rate` coinciden exactamente con el documento (19/78.9%, 17/88.2%, etc.). |
| `build_sr_vs_nl.py` | `fig_sr_vs_noise_level.png` | Tasa de éxito por nivel de ruido, 3 paneles (Appetitive/Aversive/Obstacle), Neural vs FSM. Verificado: coincide exactamente con la tabla §4.2 del documento del equipo. |
| `build_mode_timelines.py` | `fig_mode_timeline_complex.png`, `fig_mode_timeline_inspection.png` | Modo activo (C/H/X) como función escalonada del tiempo, un trial representativo (el primero encontrado, sin selección manual) por sistema. **Corregido proactivamente durante la verificación visual** (misma regla §11.1 ya aplicada en R3-04): el primer intento mostraba nombres de carpeta crudos (`test_001_SUCCESS`, `test_001_FAILURE_TIMEOUT`) en los títulos de panel — reemplazados por descripciones humanas ("representative successful trial" / "representative failed trial (timeout)"). El contraste visual resultante (Neural: trial corto y rico en transiciones; FSM: trial largo con bloqueo prolongado en X) coincide con la narrativa del documento del equipo. |

**Hallazgo crítico, no introducido por este trabajo — preexistente y ya documentado en otro lugar:**
al recalcular `roll_rms`/`sim_time` para el lado "Neural" de las familias A-Apetitivo/Aversivo/
Obstáculo/Compleja desde `trial_summary.json`, los valores **no coinciden** con los publicados en
`tab:consolidated_simulation_metrics` del paper actual (p. ej. Obstacle Roll recalculado
3.93±8.92° vs. 0.55±0.02° publicado) — esta es la **misma discrepancia exacta** ya flagged sin
resolver en la fila `N-01` de `PROGRESS.md` desde antes de esta sesión ("tab_consolidated...csv
does not match... not investigated or acted on here"). No se intentó resolver aquí (fuera de
alcance, preexistente). **Implicación para R2-02:** el lado "Neural" de la tabla maestra de este
experimento hereda la misma incertidumbre — los números recalculados aquí son trazables al código
y a `trial_summary.json`, pero no necesariamente coinciden con lo que ya está impreso en el paper
para esas mismas familias. La sesión de escritura debe decidir: ¿citar los números recalculados
(defendibles por código, pero inconsistentes con Table 6 ya publicada) o los ya publicados
(consistentes con el resto del paper, pero de proveniencia no reproducible)? Recomendación: esto
merece resolverse junto con el hallazgo ya abierto de `N-01`, no por separado — son el mismo
problema visto desde dos tareas distintas. Confirmado que el lado terreno (`familia_c1_terreno_
rugoso`) NO tiene este problema (34.91±3.41 recalculado vs. 35.0±3.4 publicado — coincide).

## 7. Qué falta (sin resolver, fuera de alcance de esta sesión)

- Confirmar con el equipo el criterio exacto de agregación de λ-eficiencia (Pregunta 3).
- Investigar/resolver el mismatch Neural recalculado-vs-publicado (compartido con `N-01`).
- ~~Ejecutar C1/C2 FSM~~ **RESUELTO 2026-09-02** — ver §8.
- Redacción de `sections/methodology.tex`/`results.tex` (fuera de alcance — sesión de escritura).

---

## 8. Ronda 2 (2026-09-02) — auditoría de imágenes + llegada de Familia C (terreno)

### 8.1 Correcciones de la Ronda 1, según `r202_audit_notes_2026-09-01.md`

| Pieza | Veredicto | Corrección aplicada |
|---|---|---|
| Tabla maestra (`table_master_comparison.csv`) | ❌ Rechazar/re-hacer | Nueva `table_master_comparison_display.csv` (`build_display_table()` en `build_master_table.py`): elimina `n_attempted`/`n_success` (Success Rate ya los resume), renombra `sim_time` → "Task Completion Time (s)" y `roll_rms` → "Roll RMS (deg)" (sin guion bajo, no el nombre crudo del CSV), y distingue explícitamente las dos agregaciones de λ ("λ (whole trial)" / "λ (conflict only)") con `LAMBDA_NOTE` explicando la diferencia — antes no había ninguna aclaración de por qué existían dos números λ. El CSV crudo se conserva sin tocar como respaldo trazable, mismo criterio que R3-04's Tabla R1/R2. |
| `fig_sr_vs_noise_level.png` | ⚠ Ajustar | Eje Y recortado al rango real de los datos (antes -5 a 108, ahora ajustado dinámicamente al mínimo real menos margen — el mínimo observado es 60%, Apetitivo `noise_level_idx=3`). Panel Obstacle: ambos sistemas están en 100% en los 5 niveles (verificado numéricamente, solapamiento perfecto) — la línea Neural ahora se dibuja punteada sobre la línea FSM (gruesa, sólida) para que ambas sean visibles, más una anotación explícita "curves fully overlap". |
| `fig_mode_timeline_complex.png` | ✅ OK, promover | Sin cambios de código — nota para la sesión de escritura: explicar en prosa por qué el modo FSM fluctúa de forma abrupta (comportamiento esperado de una jerarquía de prioridad con temporizadores de persistencia fijos, a diferencia de la transición más suave de la inhibición lateral continua de la red). |
| `fig_mode_timeline_inspection.png` | ✅ OK, promover | Misma nota que arriba. |

Bug de infraestructura encontrado durante la Ronda 2 (no introducido por el trabajo de esta
sesión, latente desde antes): `experiments/_plotting/loaders.py::list_trial_dirs()` no filtraba
por `os.path.isdir()` cuando `verdict=None` — rompía al toparse con los 3 archivos `test_*.zip`
sueltos de `familia_c1_terreno_rugoso` (mismo problema ya resuelto solo dentro de
`R3-04-noise-robustness/scripts/build_tables.py`, nunca portado al loader compartido). Corregido
en el loader compartido, no solo en el script que lo disparó — cualquier otro consumidor del
loader se beneficia del fix.

### 8.2 Familia C (terreno) — datos y análisis del equipo llegaron 2026-09-01/02

El equipo entregó `familia_c_fsm/` (25 trials C1, 21 trials C2) **junto con su propio análisis
exhaustivo**, `data/familia_c_fsm/experiment_c_terrain.md` — no fue necesario redactarlo desde
cero, solo integrarlo al pipeline reproducible y verificar sus cifras.

**Verificación:** conteos de verdict (SUCCESS/TIPOVER/CRASH por familia y sistema), valores crudos
per-trial de la tabla §4 del documento, y el hallazgo de que `noise_level_idx` no tiene efecto real
en el código FSM — todo reproducido de forma independiente contra `trial_summary.json` y coincide
exactamente.

**Hallazgo de proveniencia de datos, corregido antes de integrar:** el lado "Neural" (BG/WTA) de
C1/C2 vive en `experiments/R3-04-noise-robustness/data/familia_c1_terreno_rugoso|c2_pendiente`
(27/15 trials — coincide con lo que cita `experiment_c_terrain.md`), **no** en
`experiments/simulation/familia_c1_terreno_rugoso|c2_pendiente` (15/15, una copia más chica y
desactualizada de la misma familia que había quedado ahí desde antes de la reorganización de
R3-04). `config.yaml` apunta ahora a la fuente correcta.

**Tres diferencias metodológicas encontradas por el equipo (`experiment_c_terrain.md` §1),
verificadas contra el código, no resueltas — decisión pendiente del autor:**
1. `Upitch` (umbral de inclinación): 0.9 en BG/WTA vs. 1.30 en FSM.
2. `tchange` (origen de `Tresponse`): `starttime+98s` en BG/WTA vs. `starttime+80s` en FSM.
3. Fórmula de `Tswitch`: BG/WTA suma un margen fijo de +1s (comentado en el propio código como
   intencional), FSM no lo suma; además `tcmd` se actualiza de forma asimétrica entre modos en el
   código BG/WTA pero de forma consistente en el FSM — probable causa principal de la brecha de
   ~1s observada entre ambos `Tswitch`.

**Consecuencia para el pipeline:** `Tswitch`/`Tresponse` **no se incluyeron** en la tabla maestra
para C1/C2 — no son comparables "bajo condiciones idénticas" tal como pide el reviewer sin antes
re-ejecutar con parámetros igualados. `success_rate`, `sim_time` y `roll_rms` sí se incluyeron
(no dependen de esos tres parámetros). Se añadió un campo `note` con la advertencia completa a
cada fila de C1/C2 en `table_master_comparison.csv`/`_display.csv`, más una advertencia sobre el
tamaño de muestra reducido del lado Neural (N=6 en C1, N=3 en C2 — el equipo mismo señala en su
documento que esto es insuficiente para concluir nada firme sobre tasa de vuelco en C2, donde BG
tuvo 0/3 TIPOVER contra 6/21 de FSM).

**Decisión recomendada para la sesión de escritura** (documentada, no ejecutada aquí — ver
`experiment_c_terrain.md` §6 para el detalle completo del equipo): o bien (a) re-ejecutar ambos
códigos con los tres parámetros igualados antes de citar `Tswitch`/`Tresponse`, o (b) mantener los
datos actuales y describir explícitamente las tres diferencias como limitación metodológica del
baseline en el paper, sin presentar la brecha de latencia como una ventaja de diseño real de la
FSM.

---

## 9. Ronda 3 (2026-09-02) — cierre del hallazgo λ + correcciones mínimas

### 9.1 Pregunta 3, RESUELTA definitivamente por el equipo

El autor consultó directamente al desarrollador de la FSM sobre la cifra "0.982 Neural / 0.837
FSM" citada en `R2-02_fsm_baseline_reference.md` §5.2. Diagnóstico completo del equipo:

- **Ninguna agregación la reproduce** — probaron 5 métodos: valor final de `trial_summary.json`
  (da 1.0/1.0, es una captura de estado al cierre del trial, no un promedio), pooled sobre todo el
  trial (0.976/0.943), per-trial mean sobre todo el trial (0.965/0.934), pooled solo-conflicto
  (0.034/0.006), per-trial mean solo-conflicto (0.029/0.009). Conclusión del equipo: **es un error
  de documentación de una sesión anterior**, no un dato real.
- **El promedio solo-conflicto tampoco es una métrica válida**, incluso si se reprodujera: la
  fórmula `cmd_mag / ‖actividad neuronal‖` mezcla escalas incompatibles (velocidad lineal en m/s,
  típicamente 0.1–0.5, contra la norma de un vector de activación con valores en decenas/cientos)
  — el ratio es pequeño por diseño de la fórmula, no porque el sistema decida peor.
- **Métrica de reemplazo, propuesta y verificada por el equipo:** exposición al conflicto —
  cuánto tiempo permanece cada sistema en conflicto simultáneo real (`red_present=1` Y
  `blue_present=1`) antes de resolverlo. Familia B: Neural ≈0.2s/trial (1.1% del tiempo del
  trial), FSM ≈6.1s/trial (4.3%) — la FSM no toma peores decisiones durante el conflicto, sino que
  permanece sin resolver ~30 veces más tiempo.

**Verificación independiente en esta sesión:** recalculé la exposición al conflicto desde
`sim_time_s` exacto (no una cadencia de fila asumida de 200ms) en `build_master_table.py::
_conflict_exposure()`. Resultado: Neural 0.2s/trial (1.7% del tiempo), FSM 6.1s/trial (4.7%) —
**los segundos/trial coinciden exactamente** con la cifra del equipo; el % difiere levemente
(1.7 vs. 1.1, 4.7 vs. 4.3) por la definición del denominador (mi cálculo usa el span exacto de
`sim_time_s` del trial; el del equipo probablemente asume una cadencia de fila constante) — ambas
formas coinciden en que la FSM permanece sin resolver ~3x más como fracción de su propio trial y
~30x más en segundos absolutos. Diferencia documentada por transparencia, no oculta.

**Acción tomada:** `λ (conflict only)` eliminada de la tabla maestra; reemplazada por "Conflict
Exposure (%)" y "Conflict Exposure (s/trial)" (`build_display_table()`). `λ (whole trial)` se
conserva como indicador general de eficiencia (no ligado al argumento de conflicto). El texto
"0.982/0.837" no debe citarse en el paper bajo ninguna circunstancia — confirmado como error, no
como número con incertidumbre.

### 9.2 Correcciones mínimas de `r202_audit_notes_2026-09-01.md` (ronda 3)

| Pieza | Nota | Corrección |
|---|---|---|
| Tabla maestra | "Sin la columna Nota. Sin la columna conflict only PERO poner esos dos valores en el escrito NO en la tabla LaTeX" | Columna `Note` eliminada de `table_master_comparison_display.csv` (los caveats de terreno siguen en el CSV crudo + prosa de README/este doc, no en la tabla que va al paper). Columna `λ (conflict only)` eliminada — no reemplazada por los mismos valores en prosa (están confirmados como inválidos, ver §9.1), sino por la métrica de exposición al conflicto, que sí es válida y reproducible. |
| `fig_sr_vs_noise_level.png` | "El texto solapa con el eje, quítalo. Pero necesito que en la descripción se explique el solapamiento en Obstacle" | Anotación en la imagen eliminada. La explicación pasa al pie de figura textual (README.md, audit tool): ambos sistemas están en 100% en los **5** niveles de ruido evaluados (no un subconjunto — verificado numéricamente), solapamiento perfecto explicado por la línea Neural punteada sobre la FSM sólida. |
| Mode timelines (B, E) | ✅ sin notas | Sin cambios. |

### 8.3 Estado tras esta ronda

Las 7 familias (5 completas desde la Ronda 1 + C1/C2 de esta ronda) están en el pipeline
reproducible. Piezas para promover: `table_master_comparison_display.csv`,
`fig_sr_vs_noise_level.png`, `fig_mode_timeline_complex.png`, `fig_mode_timeline_inspection.png`
— todas re-generadas/ajustadas y verificadas visualmente. Pendiente: revisión conjunta con el
autor (próxima sesión) antes de dar por cerrada esta fase de auditoría de imágenes.
