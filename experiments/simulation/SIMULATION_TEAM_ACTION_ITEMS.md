# Información faltante / a confirmar para el equipo de simulación

**Contexto:** el equipo va a re-correr solo la batería simulada (notificado 2026-08-27). Antes de
archivar la nueva corrida en `experiments/simulation/`, esta lista recoge **todo lo que se
encontró faltante o ambiguo al construir el pipeline de regeneración de figuras** (`experiments/
N-01-simulation-figure-regeneration/`) contra los datos actuales — para que la nueva corrida no
repita los mismos vacíos. Cada ítem indica cómo se descubrió (evidencia concreta, no sospecha) y
qué archivo/columna concreta se necesita.

---

## Bloqueante — sin esto, una figura publicada no se puede reproducir desde `experiments/`

### 1. Instrumentación de latencia del escenario Obstacle no está conectada
**Evidencia:** verificado directamente, no solo en `trial_summary.json` — **0 de 15 filas** de
`metrics_raw.csv` en las 15 réplicas de `familia_a_obstaculo` tienen un valor no-nulo en la columna
`latency_s`. Ninguna otra columna del archivo trae esta medición tampoco. El panel C de
`fig1_Obstacle_macro.png` publicado (que sí muestra valores de latencia normales, según el Informe 1)
no puede haberse generado desde este dataset.
**Acción:** confirmar que el mismo mecanismo de medición de latencia usado en Appetitive/Aversive/
Complex (que sí puebla `latency_s`) está conectado también para Obstacle antes de archivar la nueva
corrida. Si el mecanismo es diferente por diseño para este escenario, documentarlo explícitamente
en `experiments_config.yaml` o en un nuevo `README.md` de la familia.

### 2. No hay mapeo documentado entre `noise_level_idx` (0–4) y el valor real de sigma aplicado
**Evidencia:** `experiments_config.yaml` solo trae **un** `variance_sigma` por suite (p. ej. `0.15`
para `familia_a_apetitivo`), comentado además — no hay una tabla o campo que diga qué magnitud de
ruido corresponde a `noise_level_idx=0` vs. `=1` vs. `=2`... Los `fig1_*_macro.png` publicados
grafican explícitamente el eje X como "Sensory Noise Index (σ)" con 5 valores discretos — sin este
mapeo, no se puede saber si el eje X de la figura publicada usa el índice tal cual (0,1,2,3,4) o una
escala de sigma real distinta.
**Acción:** exportar, junto con cada `trial_summary.json`, el valor real de sigma usado para ese
`noise_level_idx` (o publicar una tabla fija índice→sigma en `experiments_config.yaml`, sin
comentar). Aclarar también la relación entre `noise_level_idx` y el campo `perturbations`
(`stimulus_x`/`stimulus_y` delta) del manifest — hoy parecen ser dos mecanismos de ruido distintos
sin relación documentada entre sí (algunos trials con `noise_level_idx` alto tienen
`perturbations: {}` vacío, y viceversa).

### 3. Sin activaciones neuronales individuales ($X_i$) en ningún archivo de `experiments/simulation/`
**Evidencia:** `metrics_raw.csv` (todas las familias) solo trae columnas agregadas
(`firing_variance`, `temporal_consistency`, `lambda_efficiency`) — nunca el valor individual de cada
neurona ($X_0$...$X_{17}$, $L_2$...$L_4$) que los rasters `NEU_EST_UNIB/UNIG/MUL.png` y
`NEU_IMU/NEU_IMU2.png` muestran panel por panel. **Nota relevante:** al vectorizar las versiones
*físicas* de estas figuras (`NEU_IMU_real.png`/`NEU_IMU2_real.png`, Tarea 3) se confirmó que sí es
posible reconstruir esta información leyendo directamente la intensidad de gris de la figura ya
publicada — pero esa vía no sirve para las **futuras** corridas de simulación, que aún no tienen
figura publicada que vectorizar.
**Acción:** exportar la activación de cada neurona individual (al menos las nombradas en el texto
del paper: $X_0,X_1,X_4,X_5,X_7,X_8,X_{11}$-$X_{17}$, $L_2$-$L_4$) a un nuevo
`neural_activations.csv` por réplica, mismo esquema de tiempo que `metrics_raw.csv` — el equivalente
simulado de lo que `experiments/real/*/neural_metrics.csv` ya casi logra para el físico (aunque
tampoco tiene esta granularidad, ver ítem 7).

### 4. Sin aceleración/pitch cruda continua en `familia_c1_terreno_rugoso`/`familia_c2_pendiente`
**Evidencia:** estas dos familias solo traen `stability_log.csv` (geometría del polígono de apoyo —
`SM`, `TR`, posiciones de pata) y el escalar final `roll_rms`/`pitch_rms` en `trial_summary.json` —
ninguna serie continua de aceleración Z ni ángulo de pitch, que es justo lo que
`GRAPH_IMU.png`/`GRAPH_IMU2.png` necesitan graficar.
**Acción:** exportar `ax,ay,az` (o al menos `az`) y el pitch derivado como serie temporal continua
por réplica — el equivalente simulado de `experiments/real/*/imu_ina.csv`, que sí trae esto para el
robot físico.

---

## Importante — afecta la fidelidad de una figura, no la bloquea por completo

### 5. La corrida "representativa" de $N=268$ (marcha Cuadrúpedo puro) nunca se archivó
**Evidencia:** ninguna de las 30 carpetas `familia_c1`/`familia_c2` tiene 268 filas en
`stability_log.csv` (rango real: 296–1240) — el texto (`results.tex:313-315`) es explícito en que es
**una corrida distinta**, sin cambio de terreno, dedicada a documentar el ciclo de marcha de 6 fases.
**Acción:** al re-correr, archivar esta corrida como su propia carpeta (p. ej.
`experiments/simulation/familia_d_marcha_cuadrupedo/`), no mezclada dentro de C1/C2.

### 6. Ambigüedad en el conteo de "intentos" para calcular Success % (posible artefacto de reintentos)
**Evidencia:** `suite_execution_manifest.json` repite el mismo `trial_index` hasta 3 veces cuando
hay un `FAILURE_TIMEOUT` seguido de reintento(s) (p. ej. `trial_index=6` aparece 3 veces en
`familia_a_apetitivo` con verdicts `FAILURE_TIMEOUT`, `FAILURE_TIMEOUT`, `SUCCESS`). El pipeline de
regeneración (`N-01`) tuvo que **asumir** que cada `trial_index` único cuenta como "un intento" para
calcular `Success %` de `tab:consolidated_simulation_metrics` — no hay un campo explícito que
distinga "reintento válido" de "intento que cuenta para la tasa de éxito real".
**Acción:** confirmar si esta es la semántica correcta, o si el manifest debería traer un flag
explícito (`is_retry`/`superseded_by`) para no depender de inferencia por `trial_index` repetido.

### 7. `unified_metrics.csv` vs. `metrics_raw.csv` — redundancia sin documentar
**Evidencia:** ambos archivos traen columnas muy similares (`latency`/`latency_s`,
`firing_var`/`firing_variance`, `temp_consistency`/`temporal_consistency`) con nombres ligeramente
distintos, más algunas columnas exclusivas de cada uno (`unified_metrics.csv` añade `Tresponse`,
`Tswitch`, `roll_rms`, `pitch_rms`, `active_noise_level`, `rmse_ct`; `metrics_raw.csv` añade `mode`,
`red_present`, `blue_present`). No hay documentación de cuál es la fuente canónica cuando ambos
traen el mismo dato.
**Acción:** documentar (en un `README.md` de `experiments/simulation/`) cuál archivo es la fuente de
verdad para cada columna compartida, o consolidar en un solo archivo si son redundantes por diseño.

### 8. Columna `rmse_ct` completamente vacía — ¿columna muerta o instrumentación pendiente?
**Evidencia:** verificado en las 96 réplicas actuales (`familia_a_apetitivo`) — **0/96** tienen un
solo valor no-nulo en `unified_metrics.csv.rmse_ct`.
**Acción:** confirmar si esta columna es vestigial (se puede quitar del esquema) o si mide algo que
nunca se conectó (en cuyo caso, conectarla en la nueva corrida).

---

## Menor — no bloquea nada hoy, mejora la reproducibilidad a futuro

### 9. Sin versión/commit fijado del stack de simulación por corrida
**Evidencia:** ninguna carpeta de `experiments/simulation/` documenta qué commit de
`PETER_SIMULATION` (o versión del firmware simulado) generó esos datos — dificulta saber en el
futuro si una diferencia entre corridas es un cambio real de comportamiento o un cambio de versión
del código.
**Acción:** incluir un campo `source_commit`/`peter_simulation_version` en
`suite_execution_manifest.json` o en un nuevo `trial_summary.json` de cabecera, al archivar la
próxima corrida.

### 10. Duración/tasa de muestreo no documentada explícitamente
**Evidencia:** el número de filas de `stability_log.csv` varía ampliamente incluso dentro de la
misma familia (296–1240 en C1/C2) sin que quede claro si es solo por duración variable del trial o
también por una tasa de muestreo variable.
**Acción:** confirmar (o documentar) la tasa de muestreo objetivo por familia — ayuda a decidir el
método de remuestreo/alineación al regenerar figuras (ver `experiments/_plotting/loaders.py`,
`load_stability_log_aligned`).

---

## Cómo se usa esta lista

Cada ítem 1–4 (bloqueante) debería resolverse **antes** de archivar la nueva corrida, para que el
pipeline de `experiments/N-01-simulation-figure-regeneration/` pueda regenerar las figuras completas
sin vacíos nuevos. Los ítems 5–10 no bloquean la nueva corrida, pero deberían decidirse en algún
punto para no repetir la misma incertidumbre. Ninguno de estos ítems requiere una respuesta
inmediata para continuar con el trabajo de `paper-revision` — están aquí exclusivamente para
transmitirlos al equipo de `PETER_SIMULATION`.
