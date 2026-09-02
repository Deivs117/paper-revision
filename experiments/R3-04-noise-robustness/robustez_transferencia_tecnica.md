# Documento de Transferencia Técnica — Experimentos de Robustez Sensorial (Reviewer #3.4)

**Estado:** experimentos YA EJECUTADOS. Este documento describe exclusivamente lo que se hizo, con base en el código fuente (`red_neuronal` con el bloque "ROBUSTEZ REVISION 2") y los resultados entregados en `familia_.zip` (6 suites, 112 trials registrados). No se diseñan experimentos nuevos ni se proponen pruebas adicionales.

**Origen de la evidencia usada en este documento:**
- Código fuente del nodo ROS 2 (`NetworkPublisher`), versión con `pruebaDeTerreno=True`, `pruebaInclinado=True` hardcodeados en `initctes()`.
- 6 carpetas de resultados: `familia_a_apetitivo`, `familia_a_aversivo`, `familia_a_obstaculo`, `familia_b_compleja`, `familia_c1_terreno_rugoso`, `familia_c2_pendiente`. Cada una con `suite_execution_manifest.json` + un `trial_summary.json` / `unified_metrics.csv` / `metrics_raw.csv` (y, en c1/c2, `stability_log.csv`) por trial.

**Nota sobre datos anidados no utilizados:** dentro de `familia_c1_terreno_rugoso/` existen tres archivos zip adicionales (`test_0.zip`, `test2 sin robustness.zip`, `suite_execution_manifest.zip`) cuyo manifiesto interno (36 entradas) no coincide con el manifiesto oficial de la carpeta (63 entradas). Todo lo reportado en este documento para c1 usa exclusivamente las carpetas `test_NNN_*` extraídas directamente en el nivel superior de `familia_c1_terreno_rugoso/` y su `suite_execution_manifest.json` de nivel superior. La relación exacta de esos tres zips anidados con el conjunto de datos final es **NO DISPONIBLE EN LOS ARCHIVOS PROPORCIONADOS** — se recomienda que el equipo confirme si son corridas previas/descartadas antes de citarlas.

---

## 1. Summary of New Robustness Experiments

**Qué se añadió:** un sistema de perturbación por sensor, sustituyendo el ruido gaussiano genérico único de la versión anterior por tres mecanismos distintos — deriva de IMU (random-walk), ruido de rango del LiDAR (gaussiano proporcional) y distorsión de iluminación de cámara (sesgo sistemático + dropout + jitter) — más 6 suites de simulación (Gazebo/ROS 2) que ejercitan estos mecanismos sobre los escenarios comportamentales y de terreno ya existentes en el paper.

**Por qué se añadió:** para responder al comentario de Reviewer #3: *"No noise interference robustness experiments are designed for the whole perception-decision pipeline... IMU drift, LiDAR distance noise, and camera illumination distortion..."*

**¿Son pruebas basadas en simulación?** Sí, exclusivamente. El robot físico no está disponible (fue desensamblado); todas las 6 suites se ejecutaron en el mismo entorno de simulación Gazebo/ROS 2 ya usado en el resto del paper para los resultados de simulación.

**Componentes del pipeline evaluados:** IMU (acelerómetro + orientación), LiDAR (anillo de 16 sectores), cámara (bounding boxes rojo/azul), el módulo de ganglios basales (StN/Gpi/Gpe/StR), el módulo de decisión de marcha (z14/z15/z16), y las métricas de estabilidad/latencia ya definidas en el paper (Tswitch, roll_rms, pitch_rms, SM/TR cuando aplica).

### Tabla comparativa: versión anterior vs. versión nueva

| Aspect | Previous Version | New Version |
|---|---|---|
| IMU | Un único ruido gaussiano proporcional aplicado a ax/ay/az (media cero, sin persistencia) | Deriva por random-walk acumulativo (`_update_imu_drift`) aplicada a ax/ay/az **y** a roll/pitch; el ruido blanco gaussiano heredado (`_gaussian_noise` con `_sigma_imu_noise`) permanece en el código pero está **fijado a `0.0` en esta corrida** (`self._sigma_imu_noise = 0.0`, código actual), es decir, deshabilitado en la práctica |
| LiDAR | Ruido gaussiano proporcional al rango medido | Mismo modelo (sin cambios de fórmula), ahora indexado por su propio arreglo `LidarNoiseLevels = [0.0, 0.05, 0.10, 0.15, 0.20]` |
| Camera | Ruido gaussiano proporcional aplicado directamente a posición/área del bounding box | Distorsión de iluminación (`_apply_illumination_distortion`): sesgo sistemático del área + dropout probabilístico + jitter de posición dependiente de la severidad; controlado por `IllumLevels` y, de forma acoplada, por `AreaIllumLevels` (ver Sección 4) |
| Sensor perturbation | Un solo parámetro de ruido (`nl`) compartido por los tres sensores | Un único índice compartido `noise_level_idx` (antes llamado `nl`/`noise_lvl` en versiones intermedias) sigue controlando LiDAR + deriva de IMU + iluminación **simultáneamente** — ver nota de acoplamiento en la Sección 6 |
| End-to-end evaluation | No documentada como tal en el paper actual | 6 suites de simulación (aproximación apetitiva, evitación aversiva, evasión de obstáculo, escenario complejo, terreno rugoso, pendiente), cada una barriendo 5 niveles de perturbación, con métricas registradas desde el sensor hasta el resultado de la tarea |
| Gait arbitration evaluation | No se medía explícitamente el efecto del ruido sobre la arbitración de marcha | `Tswitch`, `mode` final, y (cuando aplica) `SM`/`TR`/`tr` quedan registrados por trial, permitiendo observar el efecto de la perturbación sobre la selección/transición de marcha |
| Robustness metrics | Roll/Pitch RMS, Tswitch (ya existentes) | Se mantienen las mismas métricas; se añade el registro del `noise_level_idx`, `illum_direction` y (solo en `familia_a_*`) una perturbación de posición inicial del estímulo (`stimulus_x`/`stimulus_y`), como metadato de cada trial |

---

## 2. Propagación de la perturbación a través del pipeline completo

```
Sensor (IMU / LiDAR / Cámara)
   → perturbación (drift / ruido gaussiano / distorsión de iluminación)
   → percepción (ángulos roll/pitch, accel_std, activaciones LiDAR, área/posición de bounding box)
   → procesamiento neuronal (red Response/Aux del anillo LiDAR; entradas R/G/B al circuito StN/Gpi/Gpe/StR)
   → arbitraje de ganglios basales (StN → Gpi/Gpe → StR, competencia R/G/B)
   → selección de marcha (z[14]/z[15]/z[16], competencia C/H/X)
   → locomoción (cmd_vel, publish_mode)
   → métricas de evaluación (Tresponse, Tswitch, roll_rms, pitch_rms, SM/TR, verdict de la tarea)
```

**Qué parte del código implementa cada etapa** (nombres de función/atributo tal como aparecen en el archivo fuente):

| Etapa | Implementación en código |
|---|---|
| Perturbación IMU (deriva) | `_update_imu_drift()`, invocada dentro de `imu_callback()`; acumula `imu_drift_accel_bias` (m/s², vector de 3) e `imu_drift_roll_bias`/`imu_drift_pitch_bias` (deg) |
| Perturbación IMU (ruido blanco, deshabilitado) | `_gaussian_noise()` aplicado a `ax, ay, az, roll, pitch` dentro de `imu_callback()`, con `sigma_fraction = self._sigma_imu_noise = 0.0` |
| Perturbación LiDAR | `_gaussian_noise_array()` aplicado a `ranges` dentro de `lidar_callback()`, con `sigma_fraction = self._sigma_lidar_noise` |
| Perturbación cámara (iluminación) | `_apply_illumination_distortion()`, invocada dentro de `red_callback()`, `green_callback()` y `blue_callback()`, antes de aplicar el ruido gaussiano genérico de cámara |
| Percepción → representación neuronal (LiDAR) | `activaciones_totales` (16 neuronas de dirección preferida) → `self.Response`/`self.Aux` (dentro de `run_network()`) → `self.lidar[0..4]` |
| Percepción → representación neuronal (IMU) | `self.roll`, `self.pitch`, `self.accel_std` (buffer `accel_buffer`, ventana de 100 muestras) → alimentan `self.z[0]`, `self.z[1]`, `self.z[2]` (umbrales `Usigma_az`, `Upitch`, `Uroll`) |
| Arbitraje de ganglios basales | Ecuaciones de `self.StN`, `self.Gpi`, `self.Gpe`, `self.StR` dentro de `run_network()` (bloque "IMPLEMENTACIÓN MÓDULO IMU" — el nombre del bloque en el código es engañoso; ahí es donde vive el circuito StN/Gpi/Gpe/StR que arbitra R/G/B) |
| Selección de marcha | `self.z[14]`, `self.z[15]`, `self.z[16]` (competencia C/H/X) → lógica de histéresis (`min_dwell_time`, o bien la rama `if self.pruebaDeTerreno:` que publica el modo directamente sin histéresis — ver Sección 6) |
| Locomoción | `publish_twist()`, `publish_mode()` |
| Métricas | `self.metricsArr` (publicado en `/Metrics`), `unified_metrics.csv`, `metrics_raw.csv`, `stability_log.csv`, `trial_summary.json` (generados por el harness de pruebas externo — su código no fue proporcionado, solo sus salidas) |

**Verificación de que la perturbación llega a la decisión de marcha, no solo al sensor:** los datos confirman esta propagación. Por ejemplo, en `familia_a_apetitivo`, el trial 7 en su intento `FAILURE_TIMEOUT` (`noise_level_idx=1`) registra `blue_present_frac ≈ 0.01` (el objetivo azul fue detectado en ~1% de las muestras de todo el trial), mientras que el mismo `trial_index=7` en su reintento `SUCCESS` registra `blue_present_frac ≈ 0.99`. Esto es observación directa de datos, no una estadística agregada: un evento de pérdida de detección (dropout, coherente con el mecanismo de `_apply_illumination_distortion`) coincide con un fallo de la tarea completa (timeout), evidenciando que la perturbación de cámara se propaga hasta el resultado final de la tarea.

---

## 3. Tabla completa de parámetros nuevos

Extraídos literalmente del código fuente (`initctes()`), no inferidos:

| Parameter | Sensor | Meaning | Unit | Values Tested (índice → valor) | Default | Implementation |
|---|---|---|---|---|---|---|
| `noise_level_idx` (declarado como parámetro ROS `noise_level_idx`, antes `noise_lvl`) | Compartido (LiDAR + deriva IMU + iluminación) | Índice que selecciona simultáneamente el nivel de perturbación de LiDAR, deriva de IMU e iluminación (ver Sección 6 sobre acoplamiento) | índice entero 0–4 | 0, 1, 2, 3, 4 (verificado en manifiestos: `noise_level_idx` toma valores 0–4 en las 6 suites) | 0 | `self.ACTIVE_NOISE_IDX = self.get_parameter('noise_level_idx')...` |
| `IMUNoiseLevels` | IMU | Fracción de ruido blanco gaussiano sobre ax/ay/az/roll/pitch | fracción del valor medido | `[0.0, 0.05, 0.10, 0.20, 0.30]` — **array presente en el código pero NO indexado por `ACTIVE_NOISE_IDX`** | `self._sigma_imu_noise = 0.0` (hardcodeado, no varía con el índice) | `_gaussian_noise(rng, value, sigma_fraction)` en `imu_callback()` |
| `IMUDriftLevels_accel` | IMU | Paso (σ) de la caminata aleatoria (random walk) del sesgo acumulado de aceleración, por ciclo de control (0.15 s) | m/s² por paso | `[0.0, 0.01, 0.03, 0.06, 0.09]` | índice 0 → `0.0` | `self._sigma_drift_accel = self.IMUDriftLevels_accel[self.ACTIVE_NOISE_IDX]`; consumido en `_update_imu_drift()` |
| `IMUDriftLevels_angle` | IMU | Paso (σ) de la caminata aleatoria del sesgo acumulado de roll/pitch, por ciclo de control | deg por paso | `[0.0, 0.01, 0.04, 0.08, 0.12]` | índice 0 → `0.0` | `self._sigma_drift_angle = self.IMUDriftLevels_angle[self.ACTIVE_NOISE_IDX]`; consumido en `_update_imu_drift()` |
| `LidarNoiseLevels` | LiDAR | Fracción de ruido gaussiano proporcional al rango medido | fracción del rango medido | `[0.0, 0.05, 0.10, 0.15, 0.20]` | índice 0 → `0.0` | `self._sigma_lidar_noise = self.LidarNoiseLevels[self.ACTIVE_NOISE_IDX]`; consumido en `lidar_callback()` vía `_gaussian_noise_array()` |
| `IllumLevels` | Cámara | Severidad de la distorsión de iluminación (gain sistemático del área + probabilidad de dropout + jitter de posición) | severidad adimensional 0–1 | `[0.0, 0.10, 0.20, 0.30, 0.30]` — nótese que los índices 3 y 4 comparten el mismo valor (`0.30`) | índice 0 → `0.0` | `self._illum_severity = self.IllumLevels[self.ACTIVE_NOISE_IDX]`, salvo que `self.pruebaDeTerreno` sea `True`, en cuyo caso se fuerza a `0.0` (ver Sección 6) |
| `AreaIllumLevels` | Cámara (indirecto) | Umbral de área (`self.Area`) usado por la neurona de "stop" de aproximación (`z[17]`); se reduce a medida que sube el índice, simulando que bajo peor iluminación el blob detectado es más pequeño | unidades de área del bounding box (mismas unidades que `areaBoundingBoxX`) | `[28, 24, 20, 18, 14]` | índice 0 → `28` | `self.Area = self.AreaIllumLevels[self.ACTIVE_NOISE_IDX]`; a diferencia de `_illum_severity`, **este valor se aplica siempre, sin quedar condicionado por `pruebaDeTerreno`** |
| `illum_direction` | Cámara | Dirección de la distorsión de iluminación: `-1` = escena oscurecida (el blob se encoge y puede perderse), `+1` = sobreexposición (el blob se satura/agranda). Fijo durante todo el trial | categórico {-1, +1} | Ambos valores aparecen en los manifiestos de las 6 suites | `-1` (default del parámetro ROS) | `self.declare_parameter('illum_direction', -1)`; consumido en `_apply_illumination_distortion()` |
| `NoiseSeed` | Todos (RNG) | Semilla base para los generadores de números aleatorios de cada modalidad | entero | `42` (fijo, no varía entre trials según el código) | `42` | `self._rng_imu_noise = np.random.default_rng(self.NoiseSeed+1)`, y análogos +2/+3/+4 para drift/LiDAR/iluminación |
| `stimulus_x` / `stimulus_y` (`base`/`delta`) | No es un parámetro de sensor — es una perturbación de la **posición inicial del estímulo** en el escenario de Gazebo | Jitter aleatorio de la posición inicial (x,y) del objeto-estímulo (apetitivo/aversivo) respecto a una posición base | metros (`delta`) | Ver valores por trial en el manifiesto de `familia_a_*` (p.ej. trial 1 de `familia_a_apetitivo`: `base_x=4.0, delta_x=-0.0588`) | N/A | **No aparece en el código de `red_neuronal` proporcionado** — se registra en `suite_execution_manifest.json`, por lo que su mecanismo de generación es NO DISPONIBLE EN LOS ARCHIVOS PROPORCIONADOS (pertenece al harness externo de lanzamiento de pruebas, no al nodo de control) |

---

## 4. IMU — documentación detallada

### 4.1 Ruido gaussiano (Gaussian noise)

- **Niveles definidos en el código:** `IMUNoiseLevels = [0.0, 0.05, 0.10, 0.20, 0.30]`.
- **Estado real en esta corrida:** **deshabilitado**. La línea `self._sigma_imu_noise = 0.0  # Ahora es opcional entonces se pone en 0 para conveniencia` fija el valor a `0.0` de forma incondicional, sin indexar por `ACTIVE_NOISE_IDX`. El arreglo `IMUNoiseLevels` queda declarado pero no se usa en esta corrida.
- **Fórmula (cuando está activo):** `sigma_abs = max(|value| × sigma_fraction, 1e-4)`; `value_ruidoso = value + N(0, sigma_abs)`.
- **Variables afectadas (si estuviera activo):** `ax`, `ay`, `az` (aceleración lineal), `roll`, `pitch`.
- **Conclusión para el equipo de escritura:** en los resultados actuales, cualquier efecto observado sobre la IMU proviene exclusivamente de la deriva (Sección 4.2), no de ruido blanco. No debe describirse esta corrida como una prueba de "ruido gaussiano de IMU en niveles 0–30%".

### 4.2 Deriva (drift)

- **Modelo implementado:** caminata aleatoria (random walk) acumulativa — **no** es ruido de media cero ni un sesgo fijo constante. En cada ciclo de `imu_callback()` se añade un incremento aleatorio al sesgo acumulado, que persiste y se arrastra a los ciclos siguientes: `imu_drift_accel_bias += N(0, sigma_drift_accel)` (vector de 3 componentes), `imu_drift_roll_bias += N(0, sigma_drift_angle)`, `imu_drift_pitch_bias += N(0, sigma_drift_angle)`.
- **Variables que acumulan deriva:** `imu_drift_accel_bias[0..2]` (ax, ay, az), `imu_drift_roll_bias`, `imu_drift_pitch_bias`.
- **Cómo se aplica:** el sesgo acumulado se suma a la lectura antes de calcular `accel_mag` y antes de asignar `self.roll`/`self.pitch`, de modo que la deriva llega hasta los umbrales de decisión (`Usigma_az`, `Upitch`, `Uroll`) que alimentan `self.z[0]`, `self.z[1]`, `self.z[2]`.
- **Parámetros:** `IMUDriftLevels_accel = [0.0, 0.01, 0.03, 0.06, 0.09]` (m/s² por paso de la caminata aleatoria); `IMUDriftLevels_angle = [0.0, 0.01, 0.04, 0.08, 0.12]` (deg por paso).
- **Niveles utilizados:** los 5 índices (0–4) aparecen efectivamente en las 6 suites, según los manifiestos.
- **Duración de la perturbación:** la deriva se acumula de forma continua durante todo el trial (no se reinicia); no hay un mecanismo de "duración" separado en el código — el sesgo crece (o decrece, al ser una caminata aleatoria sin arrastre direccional forzado) mientras el nodo está activo.
- **Semilla:** `self._rng_imu_drift = np.random.default_rng(self.NoiseSeed + 2)`, es decir `seed = 44`.

---

## 5. LiDAR — documentación detallada

- **Tipo de ruido:** gaussiano, proporcional al rango medido (mismo modelo que la versión anterior, sin cambios de fórmula).
- **Cálculo de la desviación estándar:** `sigma_abs = max(|range| × sigma_lidar_noise, 1e-4)`; se aplica solo a los valores finitos del escaneo (`np.isfinite(ranges)`).
- **Niveles utilizados:** `LidarNoiseLevels = [0.0, 0.05, 0.10, 0.15, 0.20]`, indexados por `ACTIVE_NOISE_IDX` (0–4), confirmado en las 6 suites.
- **Tratamiento de valores inválidos:** los valores `NaN`/`Inf` del escaneo original se preservan sin perturbar (`valid = np.isfinite(ranges)`, solo se perturban los índices válidos).
- **Clipping de distancias:** sí — tras añadir ruido, los valores se recortan a un mínimo de 0: `noisy[valid] = np.maximum(noisy[valid], 0.0)`.
- **Cómo afecta la detección de obstáculos:** el escaneo ruidoso alimenta directamente `lidar_callback()`, que descarta lecturas fuera de `[r_min=0.2, r_max=1.0]` m y calcula `activaciones_totales` (16 neuronas direccionales) a partir de los rangos ya perturbados.
- **Cómo llega al sistema de arbitraje:** `activaciones_totales` → `self.Response`/`self.Aux` → `self.lidar[0..4]` (frente/atrás/izquierda/derecha/"nivel de amenaza agregado") → alimenta directamente las variables `G` (canal "obstáculo") y las ecuaciones `z[5]`–`z[13]` de evitación, que a su vez compiten con el resto de canales dentro del circuito StN/Gpi/Gpe/StR.

---

## 6. Cámara — distorsión de iluminación (documentación detallada)

**Mecanismo real implementado** (distinguiendo explícitamente los cuatro efectos, como pide el comentario del reviewer):

1. **Sesgo sistemático de área (no ruido de media cero):** `gain = 1.0 + illum_direction × illum_severity`; `area_distorted = max(0.0, area × gain)`. Es persistente durante todo el trial (no se resamplea por muestra), porque `illum_direction` se fija una única vez al iniciar el nodo.
2. **Dropout de detección:** con probabilidad `p_dropout = min(0.9, illum_severity × 0.6)`, el área perturbada se fuerza a `0.0` en esa muestra, simulando pérdida total de detección del blob.
3. **Jitter de posición:** `pos_distorted = pos + N(0, illum_severity × 8.0)` (grados), aplicado siempre que `illum_severity > 0`.
4. **Ruido de medición genérico adicional:** después de la distorsión de iluminación, se aplica el mismo `_gaussian_noise()` genérico usado para IMU (`sigma_fraction = self._sigma_imu_noise`) — pero como se documentó en la Sección 4.1, este valor está fijado a `0.0` en esta corrida, así que en la práctica **no añade ruido adicional** más allá de la distorsión de iluminación.

**Lo que NO se hizo:** no se aplicó ninguna transformación a nivel de imagen/píxel (no se modificó brillo/contraste de una imagen sintética en Gazebo). La distorsión actúa exclusivamente sobre las características ya extraídas por el detector de blobs (posición y área del bounding box), tal como llegan al nodo por el tópico `/bounding_box/red` y `/bounding_box/blue`. Esto debe describirse en el paper como una distorsión a nivel de *características extraídas*, no como una simulación de degradación óptica/fotométrica.

**Niveles y su significado:** `IllumLevels = [0.0, 0.10, 0.20, 0.30, 0.30]` (severidad 0–1; nótese que los índices 3 y 4 comparten el mismo valor de severidad, `0.30` — no hay progresión en el último escalón para este parámetro específico). En paralelo, `AreaIllumLevels = [28, 24, 20, 18, 14]` reduce el umbral de "stop" de aproximación en cada nivel, representando una compensación deliberada del sistema (un blob más pequeño esperado bajo peor iluminación sigue disparando el stop).

**Advertencia importante sobre activación condicional — `pruebaDeTerreno`:**

```python
self._illum_severity = self.IllumLevels[self.ACTIVE_NOISE_IDX]
if self.pruebaDeTerreno: self._illum_severity = 0.0
```

En la versión de código proporcionada, `self.pruebaDeTerreno = True` está hardcodeado, lo que **fuerza `_illum_severity = 0.0`** (distorsión de iluminación deshabilitada) cada vez que este flag es `True`. El propio comentario del código indica que estos flags booleanos existen para alternar manualmente entre configuraciones de prueba ("para no tener que manipular" múltiples líneas dispersas), lo que implica que **se editaron entre corridas de distintas suites**. Como solo se nos entregó una única fotografía del código (con `pruebaDeTerreno=True`), **no es posible determinar con certeza, solo a partir del código, qué valor tenía este flag durante la ejecución de cada una de las 6 suites** — esta información es NO DISPONIBLE EN LOS ARCHIVOS PROPORCIONADOS.

Evidencia indirecta de los datos (no una confirmación definitiva): en `familia_a_*` y `familia_b_compleja`, el manifiesto registra `illum_direction` alternando entre `-1` y `+1` de forma deliberada entre trials, y se observó al menos un caso (`familia_a_apetitivo`, trial 7) donde `blue_present_frac` cae a ~1% en un intento fallido — un patrón consistente con dropout de iluminación activo. En `familia_c1_terreno_rugoso` y `familia_c2_pendiente`, `bb_blue` y `bb_red` son `0.0` en prácticamente todos los trials (coherente con que en esos escenarios no hay estímulo de color relevante para la tarea de terreno, más que con la activación/desactivación de la iluminación). **Se recomienda que el equipo de escritura confirme con el registro de ejecución real (o con quien ejecutó las suites) qué valor tenía `pruebaDeTerreno` en cada una de las 6 corridas antes de afirmar en el paper que la distorsión de iluminación estuvo activa en todos los escenarios.**

---

## 7. Perturbaciones combinadas / simultáneas

**Hallazgo importante:** en esta corrida, **no existe una condición que aísle un solo sensor a la vez**. El único parámetro barrido (`noise_level_idx`, 0–4) escala **simultáneamente**:
- la deriva de IMU (`IMUDriftLevels_accel`/`_angle`),
- el ruido de rango del LiDAR (`LidarNoiseLevels`),
- y (condicionado a `pruebaDeTerreno`, ver Sección 6) la distorsión de iluminación de cámara (`IllumLevels`, `AreaIllumLevels`).

Es decir, cada nivel > 0 es ya, por construcción, una condición **multisensor combinada** — no existen en los datos entregados trials con "solo LiDAR perturbado" o "solo IMU perturbada" de forma aislada. La única condición sin ninguna perturbación activa es `noise_level_idx = 0` (nivel base).

**Qué sensores fueron perturbados simultáneamente:** LiDAR + IMU (deriva) siempre; + cámara (iluminación) cuando `pruebaDeTerreno = False` (ver advertencia de la Sección 6 sobre incertidumbre de este flag por suite).

**Qué combinación corresponde a cada condición:** una única combinación por índice — no hay una matriz de combinaciones distintas (p. ej. "solo IMU + LiDAR sin cámara") en los datos entregados.

**Cómo se evaluó el resultado:** mediante las 6 suites de escenario (familia_a_apetitivo/aversivo/obstaculo, familia_b_compleja, familia_c1_terreno_rugoso, familia_c2_pendiente), cada una ejecutando 3 réplicas por nivel de perturbación (0–4), con el conjunto de métricas descrito en la Sección 9.

**Consecuencia para la redacción del paper:** dado que las tres modalidades (cuando `pruebaDeTerreno=False`) o dos modalidades (cuando `pruebaDeTerreno=True`) escalan juntas bajo un único índice, **no es posible, con estos datos, atribuir un cambio observado en las métricas de arbitración a un sensor específico** (p. ej., no se puede afirmar "la deriva de IMU por sí sola causó X" porque el LiDAR y potencialmente la cámara se perturbaron al mismo tiempo). El paper debe describir esto como una evaluación de robustez ante **degradación multisensor combinada, indexada por un único nivel de severidad**, no como un barrido independiente por sensor.

---

## 8. Condiciones reales de las pruebas

### A. Parámetros del sistema

| Parámetro | Valor | Fuente |
|---|---|---|
| Simulador | Gazebo + ROS 2 (confirmado por los imports `rclpy`, `ros_gz_interfaces`, tópicos `/scan`, `/imu/data`, `/bounding_box/*`) | código fuente |
| Robot/modelo | El mismo modelo usado en el resto del paper (no se declara un modelo distinto en el código de robustez) | inferido — el nodo es el mismo `network_publisher` |
| Frecuencia del lazo de control | `self.timer = self.create_timer(0.15, self.run_network)` → periodo 0.15 s ≈ 6.67 Hz | código fuente |
| Modos de locomoción | C (cuadrúpedo), H (rodante diferencial), X (omnidireccional) — mismos tres modos del paper | código fuente + campo `mode` en `trial_summary.json` |
| Modo inicial | `self.current_mode = 'H'` (código de robustez) — nótese que difiere del `'C'` usado en versiones anteriores del nodo | código fuente |
| Semilla base de RNG | `NoiseSeed = 42` (offsets +1 a +4 por modalidad) | código fuente |

### B. Parámetros de perturbación

Ver tabla completa en la Sección 3. Resumen: `noise_level_idx` (0–4) como único índice barrido; `illum_direction` (-1/+1) alternado entre trials; `pruebaDeTerreno`/`pruebaInclinado` como flags de configuración de escenario cuyo valor exacto por suite es NO DISPONIBLE EN LOS ARCHIVOS PROPORCIONADOS (solo se dispone del snapshot con ambos en `True`).

### C. Parámetros de evaluación

| Parámetro | Valor observado en los datos |
|---|---|
| Escenarios/familias | 6: apetitivo, aversivo, obstáculo, compleja, terreno rugoso, pendiente |
| Trials por combinación (familia × noise_level_idx) | 3 réplicas exitosas retenidas por combinación (verificado contando `verdict=SUCCESS` por `noise_level_idx` en las 6 suites: siempre 3, salvo reintentos fallidos descartados) |
| Total de intentos registrados en los manifiestos | 112 (incluyendo reintentos fallidos que fueron re-ejecutados hasta obtener 3 SUCCESS por nivel, cuando fue posible) |
| Verdicts posibles observados | `SUCCESS`, `FAILURE_TIMEOUT`, `FAILURE_TIPOVER`, `FAILURE_CRASH` |
| Duración de trial (`sim_time_s`) | Varía ampliamente por familia — ver tablas de la Sección 10 (de ~6 s en `familia_a_obstaculo` a ~80 s en `familia_c2_pendiente`) |

---

## 9. Métricas disponibles, organizadas por nivel

### Perception-level metrics

| Métrica | Definición | Unidad | Dónde se obtuvo |
|---|---|---|---|
| `bb_red`, `bb_blue`, `bb_green` | Área del bounding box detectado para cada canal de color al final del trial | píxeles² (o unidad de área nativa del detector) | `trial_summary.json` → `final_metrics` |
| `red_present`, `blue_present` | Indicador binario por muestra de si el blob fue detectado | booleano (0/1) | `metrics_raw.csv`, por timestep |
| `firing_var` / `firing_variance` | Varianza de la actividad de disparo neuronal | adimensional | `unified_metrics.csv` / `metrics_raw.csv`, por timestep |
| `temp_consistency` / `temporal_consistency` | Consistencia temporal de la señal neuronal (rango 0–1 observado en los datos) | adimensional | `unified_metrics.csv` / `metrics_raw.csv`, por timestep |
| `rmse_ct` | Columna presente **solo** en `familia_c1_terreno_rugoso` (1322 muestras no vacías, 0 en el resto de familias); su definición exacta más allá del nombre de columna es **NO DISPONIBLE EN LOS ARCHIVOS PROPORCIONADOS** | numérico (valores observados en el rango ~0.1–0.3 en las muestras inspeccionadas) | `unified_metrics.csv`, solo c1 |

### Decision/arbitration-level metrics

| Métrica | Definición | Unidad | Dónde se obtuvo |
|---|---|---|---|
| `Tswitch` / `tswitch` | Retardo de cambio de modo, medido desde el comando de cambio hasta que se cumple la condición de estabilidad | s | `trial_summary.json` → `final_metrics.tswitch`; también serie temporal en `unified_metrics.csv` |
| `mode` | Modo de locomoción activo al final del trial (C/H/X) | categórico | `trial_summary.json` → `final_metrics.mode` |
| `lambda_efficiency` / `exp_lambda` | Campo presente en ambos CSV/JSON; su definición precisa no está documentada más allá del nombre — valor observado consistentemente en `1.0` en las muestras inspeccionadas | adimensional | `unified_metrics.csv`, `trial_summary.json` |
| `active_noise_level` / `noise_idx` | Nivel de perturbación activo durante ese timestep/trial (equivale a `noise_level_idx`) | índice 0–4 | `unified_metrics.csv` (por timestep), `trial_summary.json` (final) |

### Locomotion-level metrics

| Métrica | Definición | Unidad | Dónde se obtuvo |
|---|---|---|---|
| `roll_rms`, `pitch_rms` | RMS del historial de roll/pitch centrado, acumulado durante el trial | grados | `imu_callback()` (cálculo); reportado en `trial_summary.json` y `unified_metrics.csv` |
| `SM`, `SM_norm`, `TR`, `triangle_area`, `inradius` | Margen de estabilidad, margen normalizado, riesgo de vuelco y geometría del polígono de apoyo (mismas métricas ya usadas en el paper, Tabla 7) | m / adimensional / m² / m | `stability_log.csv` — **con datos reales solo en algunos trials de `familia_c2_pendiente` (7 de 15) y prácticamente vacío en el resto de trials de c1/c2 inspeccionados** (ver nota abajo) |
| `tr` (campo en `trial_summary.json`, distinto de la serie `TR` de `stability_log.csv`) | Valor de riesgo de vuelco reportado al final del trial | adimensional | `trial_summary.json` → `final_metrics.tr` |

**Nota sobre `stability_log.csv`:** de los 27 trials de `familia_c1_terreno_rugoso` y 15 de `familia_c2_pendiente` inspeccionados, la mayoría de los archivos `stability_log.csv` contienen únicamente la fila de encabezado (0 filas de datos); solo 7 trials de `familia_c2_pendiente` (`test_003`, `004`, `008`, `010`, `011`, `012`, `015`) presentan filas de datos reales (entre 1 y 8 filas). Esto significa que la geometría de apoyo (SM/TR por muestra de pie) está disponible de forma muy parcial para este lote de experimentos — el campo `tr` de `trial_summary.json` sí está poblado de forma más consistente y debe usarse como fuente principal si el paper reporta riesgo de vuelco agregado.

### Task-level metrics

| Métrica | Definición | Unidad | Dónde se obtuvo |
|---|---|---|---|
| `verdict` | Resultado final del trial: `SUCCESS`, `FAILURE_TIMEOUT`, `FAILURE_TIPOVER`, `FAILURE_CRASH` | categórico | `trial_summary.json`, `suite_execution_manifest.json` |
| `sim_time_s` | Tiempo total de simulación transcurrido en el trial | s | `trial_summary.json` → `final_metrics.sim_time_s` |
| `tresponse` / `Tresponse` | Tiempo de respuesta ante el cambio de condición relevante (terreno/pendiente, según la familia) | s | `trial_summary.json`, `unified_metrics.csv` |
| `exp_latency` | Latencia experimental reportada; en algunos trials fallidos aparece con valor `-1.0` (posible código de "no medida") | s (o -1.0 como centinela) | `trial_summary.json` → `final_metrics.exp_latency` |

---

## 10. Resultados por familia (valores reales, trials `SUCCESS` únicamente)

Se listan los valores **tal como aparecen** en `trial_summary.json` de cada trial exitoso. No se calculan medias, desviaciones estándar ni porcentajes agregados — el equipo de escritura debe derivar cualquier estadística a partir de estos valores (o del CSV consolidado adjunto, `consolidated_results.csv`, con las 112 filas parseadas).

#### familia_a_apetitivo (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tresponse | tswitch | roll_rms | pitch_rms | tr | bb_blue | bb_red |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | H | 39.653 | 0.0 | 0.2829 | 0.535 | 1.0731 | 0.0 | 41658.0 | 0.0 |
| 11 | 0 | 1 | — | 40.917 | 0.0 | 0.0 | 0.5257 | 1.0682 | 0.0 | 41860.0 | 0.0 |
| 6 | 0 | -1 | — | 37.0 | 0.0 | 0.0 | 0.5373 | 1.0672 | 0.0 | 41796.0 | 0.0 |
| 12 | 1 | 1 | H | 36.22 | 0.0 | 0.1928 | 0.5272 | 1.0513 | 0.0 | 34068.0 | 0.0 |
| 2 | 1 | -1 | H | 40.723 | 0.0 | 0.0011 | 0.5288 | 1.1115 | 0.0 | 41184.0 | 0.0 |
| 7 | 1 | -1 | — | 39.078 | 0.0 | 0.0 | 0.5256 | 1.0653 | 0.0 | 39960.0 | 0.0 |
| 13 | 2 | 1 | H | 30.41 | 0.0 | 0.0012 | 0.5331 | 1.2941 | 0.0 | 28220.0 | 0.0 |
| 3 | 2 | -1 | H | 37.548 | 0.0 | 0.4047 | 0.525 | 1.2178 | 0.0 | 40108.0 | 0.0 |
| 8 | 2 | 1 | H | 33.7 | 0.0 | 0.0012 | 0.5291 | 1.2441 | 0.0 | 31150.0 | 0.0 |
| 14 | 3 | 1 | H | 37.387 | 0.0 | 0.001 | 0.5214 | 1.7573 | 0.0 | 28896.0 | 0.0 |
| 4 | 3 | -1 | H | 37.762 | 0.0 | 0.0008 | 0.5371 | 1.7653 | 0.0 | 41580.0 | 0.0 |
| 9 | 3 | 1 | H | 29.911 | 0.0 | 0.2227 | 0.5226 | 1.8555 | 0.0 | 24335.0 | 0.0 |
| 10 | 4 | 1 | — | 30.315 | 0.0 | 0.0 | 0.5367 | 2.1195 | 0.0 | 21462.0 | 0.0 |
| 15 | 4 | 1 | H | 33.722 | 0.0 | 0.2814 | 0.5397 | 2.1155 | 0.0 | 23408.0 | 0.0 |
| 5 | 4 | -1 | H | 49.786 | 0.0 | 0.0009 | 0.5255 | 2.0832 | 0.0 | 40238.0 | 0.0 |

*Nota de trials fallidos no incluidos arriba:* 4 intentos `FAILURE_TIMEOUT` (índices 6, 7, 10, 11) fueron re-ejecutados y sustituidos por reintentos `SUCCESS` con el mismo `trial_index`. El intento fallido `test_007_FAILURE_TIMEOUT` registró `blue_present_frac ≈ 0.01` (ver Sección 2).

#### familia_a_aversivo (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tresponse | tswitch | roll_rms | pitch_rms | tr |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | H | 8.632 | 0.0 | 0.0 | 1.5437 | 1.0077 | 0.5797 |
| 11 | 0 | 1 | H | 8.0 | 0.0 | 0.0 | 1.7059 | 1.0536 | 0.0 |
| 6 | 0 | -1 | H | 8.222 | 0.0 | 0.0 | 1.6232 | 1.0226 | 0.5797 |
| 12 | 1 | 1 | H | 8.522 | 0.0 | 0.0 | 1.4405 | 1.1956 | 0.5797 |
| 2 | 1 | -1 | H | 9.493 | 0.0 | 3.9514 | 1.5147 | 1.3507 | 0.5797 |
| 7 | 1 | -1 | H | 8.827 | 0.0 | 5.6464 | 1.2645 | 1.3619 | 0.5797 |
| 13 | 2 | 1 | H | 8.142 | 0.0 | 0.0 | 1.6636 | 1.6082 | 0.0 |
| 3 | 2 | -1 | H | 7.777 | 0.0 | 0.0 | 1.7522 | 1.5176 | 0.5797 |
| 8 | 2 | 1 | H | 7.96 | 0.0 | 0.0 | 1.6954 | 1.6506 | 0.6049 |
| 14 | 3 | 1 | H | 8.126 | 0.0 | 0.0 | 1.6873 | 2.2697 | 0.0 |
| 4 | 3 | -1 | H | 8.3 | 0.0 | 0.0 | 1.5496 | 2.2525 | 0.0 |
| 9 | 3 | 1 | H | 8.211 | 0.0 | 0.0 | 1.8074 | 2.3157 | 0.0 |
| 10 | 4 | 1 | H | 17.066 | 0.0 | 1.5714 | 1.2584 | 2.4947 | 0.9885 |
| 15 | 4 | 1 | H | 9.193 | 0.0 | 0.0 | 1.22 | 2.7089 | 0.9885 |
| 5 | 4 | -1 | H | 9.044 | 0.0 | 0.0 | 1.6192 | 2.6269 | 0.5797 |

#### familia_a_obstaculo (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tswitch | roll_rms | pitch_rms |
|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | X | 8.321 | 0.001 | 0.6106 | 2.0882 |
| 11 | 0 | 1 | X | 6.771 | 0.0006 | 0.5596 | 1.3015 |
| 6 | 0 | -1 | X | 6.816 | 0.0008 | 0.5634 | 1.0822 |
| 12 | 1 | 1 | X | 6.676 | 0.0008 | 0.588 | 1.2098 |
| 2 | 1 | -1 | X | 6.755 | 0.0007 | 0.5156 | 1.2355 |
| 7 | 1 | -1 | X | 6.797 | 0.0007 | 0.5638 | 1.1841 |
| 13 | 2 | 1 | X | 6.881 | 0.001 | 0.56 | 1.437 |
| 3 | 2 | -1 | X | 6.808 | 0.0009 | 0.5648 | 1.4719 |
| 8 | 2 | 1 | X | 6.797 | 0.0013 | 0.7469 | 1.3609 |
| 14 | 3 | 1 | X | 6.592 | 0.0007 | 0.4983 | 1.7521 |
| 4 | 3 | -1 | X | 6.815 | 0.0009 | 0.4894 | 1.8724 |
| 9 | 3 | 1 | X | 6.776 | 0.0009 | 0.6788 | 1.724 |
| 10 | 4 | 1 | X | 6.749 | 0.0009 | 0.4659 | 1.9464 |
| 15 | 4 | 1 | X | 6.792 | 0.0012 | 0.7165 | 1.8457 |
| 5 | 4 | -1 | X | 5.791 | 0.0007 | 0.5368 | 1.818 |

*Todos los 15 trials de esta familia terminaron en `SUCCESS` en el primer intento (sin reintentos registrados).*

#### familia_b_compleja (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tswitch | roll_rms | pitch_rms | tr | bb_blue |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | H | 43.317 | 0.0009 | 0.8996 | 1.1018 | 0.6049 | 41580.0 |
| 11 | 0 | 1 | H | 40.535 | 0.0009 | 0.7913 | 1.0937 | 0.5797 | 42054.0 |
| 6 | 0 | -1 | H | 43.355 | 0.0008 | 0.8439 | 1.1154 | 0.0 | 42183.0 |
| 12 | 1 | 1 | H | 38.048 | 0.0012 | 1.0199 | 1.0934 | 0.454 | 34440.0 |
| 2 | 1 | -1 | H | 57.147 | 0.0007 | 1.0563 | 0.9368 | 0.5797 | 41629.0 |
| 7 | 1 | -1 | H | 35.343 | 0.0016 | 1.1277 | 1.033 | 1.5416 | 41610.0 |
| 13 | 2 | 1 | H | 39.508 | 0.0009 | 0.9217 | 1.2697 | 0.454 | 31304.0 |
| 3 | 2 | -1 | H | 55.233 | 0.0007 | 0.8775 | 1.2039 | 0.9885 | 37950.0 |
| 8 | 2 | 1 | H | 38.263 | 0.0007 | 0.9504 | 1.1852 | 0.4729 | 28724.0 |
| 14 | 3 | 1 | H | 39.905 | 0.0013 | 1.0171 | 1.8305 | 0.5262 | 30275.0 |
| 4 | 3 | -1 | H | 56.646 | 0.0376 | 1.2411 | 2.2091 | 0.5797 | 40920.0 |
| 9 | 3 | 1 | H | 35.013 | 0.2611 | 1.0669 | 1.6357 | 0.9885 | 28390.0 |
| 10 | 4 | 1 | H | 31.822 | 0.0051 | 1.2669 | 1.9523 | 0.5494 | 21024.0 |
| 15 | 4 | 1 | H | 48.467 | 0.0008 | 1.5738 | 2.1092 | 0.9885 | 21316.0 |
| 5 | 4 | -1 | H | 50.018 | 0.0015 | 1.0564 | 2.1408 | 1.0115 | 39015.0 |

*Trials fallidos no incluidos: 1 `FAILURE_TIMEOUT` (nivel 0) y 3 `FAILURE_TIPOVER` (niveles 2, 3, 4) fueron re-ejecutados hasta obtener `SUCCESS`.*

#### familia_c1_terreno_rugoso (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tresponse | tswitch | roll_rms | pitch_rms | tr |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | C | 51.11 | 4.5695 | 0.0004 | 1.7889 | 1.3899 | 0.6049 |
| 11 | 0 | 1 | C | 56.5 | 3.3306 | 1.0003 | 1.8684 | 1.358 | 0.6049 |
| 6 | 0 | -1 | C | 57.21 | 4.242 | 1.0003 | 1.8237 | 1.2494 | 0.6049 |
| 12 | 1 | 1 | C | 56.04 | 7.3453 | 1.0004 | 1.7242 | 1.2801 | 0.5797 |
| 2 | 1 | -1 | C | 55.02 | 0.7547 | 1.0006 | 1.7691 | 1.2704 | 0.0 |
| 7 | 1 | -1 | C | 56.35 | 3.3284 | 1.0006 | 1.7352 | 1.1217 | 0.5797 |
| 13 | 2 | 1 | C | 59.5 | 6.3749 | 1.0003 | 1.7776 | 1.4204 | 0.0 |
| 3 | 2 | -1 | C | 56.85 | 11.6863 | 1.0003 | 1.6547 | 1.3827 | 0.5797 |
| 8 | 2 | 1 | C | 63.8 | 16.7463 | 1.0003 | 1.6792 | 1.263 | 0.6049 |
| 14 | 3 | 1 | C | 56.2 | 39.2149 | 1.0003 | 1.8786 | 1.7536 | 0.0 |
| 4 | 3 | -1 | C | 56.93 | 40.2075 | 1.2554 | 1.8846 | 1.7092 | 0.5797 |
| 9 | 3 | 1 | C | 55.05 | 20.7969 | 1.0003 | 1.6967 | 1.7016 | 0.6049 |
| 10 | 4 | 1 | C | 60.68 | 17.194 | 1.0002 | 1.7024 | 2.4772 | 1.0115 |
| 15 | 4 | 1 | C | 54.18 | 8.7637 | 1.0004 | 1.8433 | 2.2202 | 0.0 |
| 5 | 4 | -1 | C | 56.92 | 8.2016 | 1.0004 | 1.927 | 2.2831 | 0.6049 |

*Esta familia registró el mayor número de fallos: 4 `FAILURE_CRASH` y 8 `FAILURE_TIPOVER` adicionales (sobre 63 intentos totales registrados en el manifiesto) antes de completar las 15 réplicas `SUCCESS` mostradas.*

#### familia_c2_pendiente (verdict=SUCCESS)
| trial | noise_level_idx | illum_direction | mode | sim_time_s | tresponse | tswitch | roll_rms | pitch_rms | tr | bb_red |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | -1 | H | 75.67 | 63.384 | 1.0002 | 1.613 | 3.6763 | 0.6049 | 0.0 |
| 11 | 0 | 1 | H | 76.68 | 11.8386 | 1.0002 | 1.7643 | 2.3605 | 0.0 | 0.0 |
| 6 | 0 | -1 | C | 78.7 | 14.8398 | 1.0005 | 16.8761 | 5.7351 | 0.0 | 0.0 |
| 12 | 1 | 1 | H | 74.86 | 5.8331 | 1.0004 | 1.4804 | 2.6366 | 0.0 | 0.0 |
| 2 | 1 | -1 | H | 74.47 | 22.1892 | 1.0004 | 1.4159 | 3.6735 | 0.6049 | 0.0 |
| 7 | 1 | -1 | H | 80.41 | 12.8834 | 1.0003 | 1.5376 | 4.5769 | 0.0 | 0.0 |
| 13 | 2 | 1 | H | 76.53 | 12.4382 | 1.0005 | 1.5835 | 2.3344 | 0.0 | 0.0 |
| 3 | 2 | -1 | H | 78.83 | 15.1894 | 1.0004 | 1.4283 | 4.0194 | 0.5797 | 0.0 |
| 8 | 2 | 1 | H | 76.96 | 14.6897 | 1.0003 | 1.6063 | 3.6925 | 0.0 | 0.0 |
| 14 | 3 | 1 | H | 76.32 | 11.3856 | 1.0003 | 1.4827 | 2.6222 | 0.0 | 0.0 |
| 4 | 3 | -1 | H | 69.61 | 8.8396 | 1.0004 | 1.4725 | 2.3565 | 0.0 | 0.0 |
| 9 | 3 | 1 | H | 72.68 | 9.4659 | 1.0004 | 1.4857 | 2.5936 | 0.5797 | 0.0 |
| 10 | 4 | 1 | H | 77.57 | 11.9935 | 1.0002 | 1.497 | 2.842 | 0.0 | 0.0 |
| 15 | 4 | 1 | H | 75.81 | 7.1895 | 1.0005 | 8.1364 | 5.7343 | 0.6049 | 9118.0 |
| 5 | 4 | -1 | H | 79.81 | 17.6867 | 1.0025 | 1.5721 | 4.7236 | 1.622 | 0.0 |

*Nótese el valor atípico de `roll_rms = 16.88` en el trial 6 (`noise_level_idx=0`, modo final `C` en vez de `H` como el resto de la familia) — dato real, no filtrado; el equipo de escritura debe decidir si se trata de un evento genuino a discutir o un caso a excluir con justificación explícita.*

### Verdicts por familia (conteo literal de trials, no tasas ni porcentajes)

| Familia | SUCCESS (retenidos) | FAILURE_TIMEOUT | FAILURE_TIPOVER | FAILURE_CRASH | Total intentos en manifiesto |
|---|---|---|---|---|---|
| familia_a_apetitivo | 15 | 4 | 0 | 0 | 19 |
| familia_a_aversivo | 15 | 0 | 0 | 0 | 15 |
| familia_a_obstaculo | 15 | 0 | 0 | 0 | 15 |
| familia_b_compleja | 15 | 3 | 3 | 0 | 21 |
| familia_c1_terreno_rugoso | 15 | 0 | 8 | 4 | 63 (manifiesto) / 27 (carpetas de test conservadas) |
| familia_c2_pendiente | 15 | 0 | 0 | 0 | 15 |

---

## 11. Figuras y tablas propuestas para el paper

Solo se especifica contenido; no se generan gráficos aquí.

**Figura R1 — Robustez de arbitración de marcha vs. nivel de perturbación combinada (todas las familias comportamentales)**
- Datos: `Tswitch` (eje Y) vs. `noise_level_idx` (eje X, 0–4), una serie por familia (apetitivo, aversivo, obstáculo, compleja).
- Condiciones: solo trials `SUCCESS`.
- Métrica: `tswitch` de `trial_summary.json`.
- Propósito científico: mostrar si la latencia de conmutación de marcha se degrada con el nivel de perturbación combinada.
- Reviewer comment addressed: #3.4 (robustez del pipeline completo, específicamente el efecto sobre la arbitración de marcha).

**Figura R2 — Estabilidad postural vs. nivel de perturbación (terreno rugoso y pendiente)**
- Datos: `roll_rms` y `pitch_rms` (dos paneles o dos ejes) vs. `noise_level_idx`, familias `familia_c1_terreno_rugoso` y `familia_c2_pendiente`.
- Condiciones: solo trials `SUCCESS`.
- Propósito científico: mostrar el efecto de la perturbación combinada (LiDAR + deriva IMU) sobre la estabilidad postural en los escenarios más exigentes.
- Reviewer comment addressed: #3.4.

**Tabla R1 — Tasa de fallo por familia y tipo de fallo**
- Contenido: columnas `familia`, `SUCCESS`, `FAILURE_TIMEOUT`, `FAILURE_TIPOVER`, `FAILURE_CRASH`, tal como en la tabla de la Sección 10 de este documento.
- Propósito científico: cuantificar el costo en fiabilidad de operar bajo perturbación combinada, particularmente el contraste entre `familia_c1_terreno_rugoso` (mayor tasa de fallo) y las familias comportamentales sobre terreno plano.
- Reviewer comment addressed: #3.4, con relevancia adicional para la Sec. 3.4 (Limitations) del paper.

**Figura R3 — Evidencia de dropout de detección de cámara y su efecto en el resultado de la tarea**
- Datos: serie temporal de `blue_present`/`red_present` (0/1) para el par de trials `familia_a_apetitivo` trial_index=7 (`FAILURE_TIMEOUT` vs. `SUCCESS` en el reintento), superpuesta con el `verdict` final.
- Propósito científico: ilustrar de forma concreta cómo un evento de dropout de percepción se propaga hasta un fallo de tarea completo — evidencia directa de la propagación end-to-end pedida por el reviewer.
- Reviewer comment addressed: #3.4 (specíficamente la exigencia de no evaluar el ruido "solamente a nivel de sensor").
- **Advertencia:** esta figura solo es defendible si el equipo confirma que la iluminación estuvo efectivamente activa (`pruebaDeTerreno=False`) durante `familia_a_apetitivo` (ver Sección 6); de lo contrario, el dropout observado podría deberse a otra causa no perturbativa y la figura no debe presentarse como evidencia de robustez a iluminación.

**Tabla R2 — Parámetros de perturbación por sensor**
- Contenido: la tabla completa de la Sección 3 de este documento (parámetro, sensor, significado, unidad, valores, implementación).
- Propósito científico: dar reproducibilidad metodológica completa.
- Reviewer comment addressed: #3.4, y de forma general mejora la reproducibilidad exigida por cualquier revisor.

---

## 12. Cambios requeridos en el paper actual

| Current Section | Required Change | New Information | Priority |
|---|---|---|---|
| Sec. 2.3 (Neuronal Control System) — probablemente una nueva subsección 2.3.5 o un párrafo al final de 2.3.4 | AMPLIAR (metodología) | Describir el mecanismo de deriva de IMU (random walk), el modelo de distorsión de iluminación (sesgo + dropout + jitter) y el modelo de ruido de LiDAR ya usado, como parte de la metodología de evaluación de robustez. Debe incluir la advertencia de que el ruido blanco de IMU quedó deshabilitado en esta corrida (Sección 4.1 de este documento) para no sobre-representar lo que realmente se probó | CRITICAL |
| Sec. 3.1 (Simulation Results) — nueva subsección, p.ej. 3.1.8 | AÑADIR RESULTADOS + FIGURAS + TABLAS | Insertar Figura R1, Figura R2, Tabla R1 (Sección 11 de este documento) con los resultados de las 6 familias bajo perturbación combinada | CRITICAL |
| Sec. 3.4 (Limitations of the Present Work) | ACTUALIZAR | Añadir explícitamente que la evaluación de robustez se hizo con perturbaciones **acopladas** (no aisladas por sensor — ver Sección 7 de este documento), y que el ruido blanco de IMU no fue ejercitado en esta ronda (solo la deriva). También incorporar la tasa de fallo elevada observada en `familia_c1_terreno_rugoso` (4 CRASH + 8 TIPOVER) como limitación de robustez en terreno rugoso bajo perturbación | CRITICAL |
| Sec. 4 (Conclusions) | ACTUALIZAR | Si el paper afirma en las conclusiones que el sistema es robusto a ruido sensorial de forma genérica, esa afirmación debe matizarse: se probó robustez ante deriva de IMU + ruido de LiDAR (+ iluminación, condicionalmente) **combinados**, no ruido blanco de IMU aislado ni condiciones de sensor único | HIGH |
| Metodología / Sec. 2.4 (Physical Platform Construction and Experimental Setup) | ACLARAR | Señalar explícitamente que los nuevos experimentos de robustez son exclusivamente de simulación, dado que el robot físico no está disponible actualmente (fue desensamblado) — esto debe quedar dicho de forma explícita para que no se asuma validación física de la robustez | CRITICAL |
| Cualquier tabla de métricas consolidadas ya existente (p. ej. Tabla 6) | EVALUAR SI SE EXTIENDE | Si el equipo decide incorporar las nuevas métricas de robustez en una tabla consolidada existente, debe hacerse como una tabla nueva y separada (Tabla R2), no fusionada con Tabla 6, porque las condiciones experimentales (perturbación combinada vs. escenarios ya reportados) no son directamente comparables | MEDIUM |

---

## Archivo de datos adjunto

Se genera un CSV consolidado (`consolidated_results.csv`, 112 filas) con todos los campos de `final_metrics` + `seed_info` de los 112 trials parseados de las 6 suites, para que el equipo de escritura pueda calcular cualquier estadística agregada directamente sobre los datos reales sin pasar por transcripción manual.
