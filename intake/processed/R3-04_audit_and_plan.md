# Auditoría + Plan de Reorganización — R3-04 (Robustez sensorial IMU/LiDAR/Cámara)

**Estado:** análisis + planificación, con la reorganización estructural de §5 **ya ejecutada** en
esta misma sesión (mover/renombrar carpetas, crear `README.md`/`config.yaml` del experimento no
cuenta como "redacción del paper" — confirmado explícitamente por el propietario del repo). **Lo
que sigue sin tocarse:** ningún `sections/*.tex`, ningún `patches/`, y `PROGRESS.md` no cambió de
estado — eso queda para la sesión de escritura, junto con generar las figuras/tablas reales
(`scripts/` de este experimento todavía no existen).

**Origen:** auditoría de `experiments/R3-04_simulation/` (datos entregados por el equipo de
simulación) + su documento de transferencia `robustez_transferencia_tecnica.md` + verificación
cruzada contra el código fuente real en `../PETER_SIMULATION` (rama `dieguito`), para responder al
comentario de Reviewer #3.4: *"No noise interference robustness experiments are designed for the
whole perception-decision pipeline... IMU drift, LiDAR distance noise, and camera illumination
distortion..."*

---

## 1. Inventario de lo recibido

```
experiments/R3-04_simulation/                    (carpeta NO trackeada en git todavía — git status: ??)
├── robustez_transferencia_tecnica.md             (429 líneas, documento de transferencia del equipo)
├── consolidated_results.csv                      (112 filas + cabecera, entregado el 2026-08-31 — inicialmente faltaba, ya confirmado presente)
├── familia_a_apetitivo/        (20 subdirs: 1 manifest + 19 intentos test_NNN_*)
├── familia_a_aversivo/         (16 subdirs)
├── familia_a_obstaculo/        (16 subdirs)
├── familia_b_compleja/         (22 subdirs)
├── familia_c1_terreno_rugoso/  (28 subdirs, incluye 3 .zip anidados — ver §3d)
└── familia_c2_pendiente/       (16 subdirs)
```

Cada `test_NNN_<VERDICT>/` trae `trial_summary.json`, `unified_metrics.csv`, `metrics_raw.csv`
(y en c1/c2, `stability_log.csv`). Total: 112 intentos registrados en los manifiestos (90
`SUCCESS` retenidos — 15 por familia × 6 —, 22 fallidos descartados: 7 `FAILURE_TIMEOUT`, 11
`FAILURE_TIPOVER`, 4 `FAILURE_CRASH`). Verificado por conteo directo de carpetas, coincide con lo
que reporta el documento del equipo.

**No sigue la convención `experiments/_TEMPLATE/`:** no hay `README.md`, `config.yaml`,
`scripts/`, ni separación `data/`/`output/`. El nombre de carpeta (`R3-04_simulation`, guion bajo)
tampoco coincide con `PROGRESS.md`, que ya referencia `experiments/R3-04-noise-robustness/`
(guion, con slug descriptivo). Plan de reorganización en §5.

---

## 2. Qué mide el experimento (resumen técnico, ya validado contra el código)

Un único parámetro barrido, `noise_level_idx` (0–4), escala **simultáneamente**:
- Deriva de IMU por random-walk acumulativo (`IMUDriftLevels_accel/_angle`) sobre ax/ay/az/roll/pitch.
- Ruido gaussiano de rango del LiDAR (`LidarNoiseLevels`), proporcional al rango medido.
- Distorsión de iluminación de cámara (`IllumLevels`/`AreaIllumLevels`): sesgo sistemático de área +
  dropout probabilístico + jitter de posición del bounding box (no es degradación óptica de imagen).

**No hay condición que aísle un solo sensor.** Cada nivel >0 es ya una perturbación multisensor
combinada; solo `noise_level_idx=0` es el nivel base sin perturbación. El ruido blanco gaussiano de
IMU (`IMUNoiseLevels`) está declarado en el código pero fijado a `0.0` en esta corrida — no se debe
describir esto como "ruido gaussiano de IMU 0–30%", solo como deriva.

6 suites de simulación (Gazebo/ROS 2), 5 niveles × 3 réplicas `SUCCESS` cada una: apetitivo,
aversivo, evasión de obstáculo, escenario complejo, terreno rugoso, pendiente. Frecuencia de
control 0.15 s (~6.67 Hz). Semilla base `NoiseSeed=42`. Solo simulación — el robot físico no está
disponible (desensamblado), esto debe quedar explícito en el paper (§9 del doc del equipo, tabla
de cambios requeridos, fila "Metodología / Sec. 2.4").

---

## 3. Auditoría de valores — qué es útil y qué no para el análisis cuantitativo

| Campo | Veredicto | Razón |
|---|---|---|
| `sim_time_s`, `tresponse`, `tswitch`, `roll_rms`, `pitch_rms`, `mode`, `verdict`, `noise_level_idx`, `illum_direction`, `bb_red/blue/green` | **Usar** | Poblados de forma consistente, con definición clara y trazable al código (`trial_summary.json → final_metrics`). |
| `tr` (`trial_summary.json`) | **Usar como fuente principal de riesgo de vuelco agregado** | Bien poblado en casi todos los trials (a diferencia de `stability_log.csv`, ver fila siguiente). |
| **(a) `lambda_efficiency` / `exp_lambda`** | **Excluir** | Constante en `1.0` en todas las muestras inspeccionadas, sin definición documentada más allá del nombre de campo. No aporta información — no es una métrica ya usada en el paper (es nueva de este dataset), así que excluirla no retira nada existente. |
| **(b) `rmse_ct`** | **Excluir** | Solo tiene datos reales en `familia_c1_terreno_rugoso` (0 en el resto); su definición semántica es NO DISPONIBLE más allá del nombre de columna. Verificado directamente: en `familia_a_apetitivo/test_001` la columna está vacía en el 100% de las filas. |
| **(c) `stability_log.csv` (serie `SM`/`TR`/`triangle_area`/`inradius`)** | **Excluir como fuente para ESTE experimento** | Vacío (solo cabecera) en la mayoría de los 27 trials de c1 y 15 de c2 inspeccionados; solo 7/15 trials de c2 tienen filas de datos reales (1–8 filas). Usar `tr` de `trial_summary.json` en su lugar (ver fila anterior). **Importante — no afecta lo ya publicado:** la Tabla 7 existente del paper (SM/TR/inradius, `results.tex` línea ~258) proviene de **otro experimento** (terreno rugoso/pendiente sin perturbación multisensor combinada) y no se toca. Lo único que se pierde es la posibilidad de reportar SM/TR con muestra completa **para este nuevo experimento de robustez** — se compensa con `tr`, dejando una nota metodológica de que no es directamente comparable a la Tabla 7 (condiciones distintas). |
| **(d) 3 `.zip` anidados en `familia_c1_terreno_rugoso`** (`test_0.zip`, `test2 sin robustness.zip`, `suite_execution_manifest.zip`) | **Excluir, no eliminar** | Su manifiesto interno (36 entradas) no coincide con el manifiesto oficial de nivel superior (63 entradas). Todo lo reportado para c1 en este documento y en el del equipo usa exclusivamente las carpetas `test_NNN_*` de nivel superior. Se recomienda **preguntar al equipo** si son corridas previas/descartadas antes de decidir si se archivan o se borran — no descartar definitivamente sin confirmación, ya que podrían ser una versión alterna válida. |
| Outlier `familia_c2_pendiente` trial 6 (`roll_rms=16.88`, modo final `C` en vez de `H`, `noise_level_idx=0`) | **Mantener, con decisión editorial pendiente** | Dato real, no filtrado — no hay evidencia de error de instrumentación. El equipo de escritura (próxima sesión) debe decidir si se discute como hallazgo genuino o se excluye con justificación explícita en el texto; no debe eliminarse silenciosamente. |

**Respuesta directa a la pregunta "¿esto nos quita métricas que antes teníamos?":** No. `(a)`–`(c)`
son todos campos **nuevos** de este dataset de robustez (ninguno reemplaza una métrica ya publicada
en el paper); excluirlos del análisis cuantitativo no borra nada del texto actual. `(d)` son datos
crudos redundantes/inciertos, no una métrica citada en ningún lado todavía.

---

## 4. Hallazgo de arqueología de código en `PETER_SIMULATION` (nuevo, no estaba en el doc del equipo)

El documento de transferencia del equipo (§6) señala como incertidumbre **crítica** que no podían
determinar si `pruebaDeTerreno` (que fuerza `_illum_severity=0.0`, desactivando la distorsión de
iluminación) estuvo activo durante las 6 suites, porque solo tenían "una fotografía" del código.
Siguiendo la pista dada por el usuario (rama `dieguito` del repo `PETER_SIMULATION`, ya presente
como sibling read-only en `../PETER_SIMULATION`), se cruzó la fecha de cada commit relevante contra
la fecha de generación de cada carpeta `familia_*` (mtime):

| Commit | Fecha | Mensaje | `pruebaDeTerreno` existe? |
|---|---|---|---|
| `04925ed` | 2026-08-27 21:21 | "robustness v2 funcional" | **No** — no existe la variable en absoluto |
| `c6536f5` | 2026-08-30 19:31 | "Cambios mayores..." | **No** — tampoco existe |
| `b37020d` | 2026-08-31 16:36 (**hoy**) | "Fix a los cambios mayores..." | **Sí** — introducida por primera vez, con `pruebaDeTerreno=True` hardcodeado y el override `if self.pruebaDeTerreno: self._illum_severity = 0.0` |

Las 6 carpetas de datos se generaron entre el 28 y el 30 de agosto (17:17–21:47), es decir, **antes**
de `b37020d` (hoy). `familia_c1_terreno_rugoso` (mtime 30-ago 19:23) es 8 minutos anterior a
`c6536f5` (19:31), así que junto con `familia_a_*`/`familia_b_compleja` corresponde a `04925ed`;
`familia_c2_pendiente` (mtime 21:47) es posterior a `c6536f5`, así que probablemente corresponde a
ese commit. **En ninguno de los dos commits que realmente generaron los datos existe el flag
`pruebaDeTerreno`** — la línea `_illum_severity = self.IllumLevels[self.ACTIVE_NOISE_IDX]` se
aplica sin condición alguna en ambos.

**Conclusión — resuelve la incertidumbre crítica del equipo:** la distorsión de iluminación de
cámara **sí estuvo activa** (sin excepción, en las 6 suites) en el código que generó este dataset.
El flag que la desactivaría fue añadido por el equipo **después** de la entrega de datos, como parte
del sistema dinámico que el usuario mencionó que se diseñó a posteriori para mejorar la robustez —
no aplica retroactivamente a estos 112 trials. **La Figura R3 (dropout de cámara,
`familia_a_apetitivo` trial 7) es defendible sin el caveat de "no disponible en los archivos
proporcionados" que pedía el documento del equipo.**

**Segundo hallazgo, no contemplado por el equipo — requiere confirmación antes de redactar:** en
ambos commits (`04925ed` y `c6536f5`), el canal `G` (derivado del LiDAR, que compite dentro del
circuito de arbitraje StN/Gpi/Gpe/StR contra R —apetitivo— y B —aversivo—) se calcula
(`G = self.lidar[4,0]*15` si supera 0.2) pero **inmediatamente se sobreescribe a `G = 0` de forma
incondicional**, en la línea siguiente, sin ningún flag que lo condicione:

```python
if self.lidar[4,0]*15 > 0.2: G = self.lidar[4,0]*15
else: G = 0
G = 0   # <-- sobreescribe siempre, código muerto en ambos commits que generaron los datos
```

Esto significa que **el ruido de LiDAR no llega a la competencia de arbitraje de ganglios basales
(canal `StN[1]`) en ninguna de las 6 suites entregadas** — contradice la afirmación de la Sección 2/5
del documento del equipo ("`G` ... compite con el resto de canales dentro del circuito
StN/Gpi/Gpe/StR"). Sin embargo, verificado también en el código: el ruido de LiDAR **sí** sigue
llegando a la vía de evasión/dirección motriz (`z[5]`–`z[13]`, que consumen directamente
`self.lidar[2,0]`, `self.lidar[3,0]`, `self.lidar[4,1]`), independientemente del canal `G`. Es decir:
robustez de LiDAR demostrada a nivel de evasión reactiva, **no** a nivel de la competencia
Ganglios-Basales R/G/B de tres vías. **Recomendación: confirmar con el equipo de simulación si este
`G=0` fue intencional (p.ej. porque el objetivo de estas 6 suites no era ejercitar la competencia de
tres vías, sino solo la deriva/ruido a nivel sensor-a-locomoción) antes de que el equipo de escritura
afirme en el paper que "el ruido de LiDAR se propaga hasta el arbitraje de ganglios basales" sin
matizar la vía exacta.**

*Referencias de commit (para pinnear en el futuro `README.md` del experimento, §9.3 del README
principal): `04925ed0b5c7cd2de876fac69e90108dc3fcc281` (familia_a_*, familia_b_compleja,
familia_c1_terreno_rugoso), `c6536f59a3a31a57439b60df4017f9d17d981f70` (probable, familia_c2_pendiente
— confirmar con el equipo si es necesario). Commit `b37020d97c7431313d16e985a7b445c38397cdc0`
("Fix...") es POSTERIOR a los datos y NO debe usarse como referencia de proveniencia.*

---

## 5. Reorganización — YA EJECUTADA en esta sesión

```
experiments/R3-04-noise-robustness/
├── README.md                         # nuevo — Goal/Método/Parámetros/Data provenance/Output files
├── config.yaml                       # nuevo — noise_level_idx 0-4, seed 42, niveles por sensor (de §3 del doc del equipo)
├── robustez_transferencia_tecnica.md # movido — documento de transferencia original del equipo, conservado como referencia (COMMITTED, no es data/ regenerable)
├── data/                              # gitignored (experiments/*/data/) — TODO lo crudo entregado por el equipo
│   ├── consolidated_results.csv       # 112 filas — considerado intermedio, no "final" hasta que scripts/ lo limpie (columnas inútiles de §3 siguen presentes)
│   ├── familia_a_apetitivo/
│   ├── familia_a_aversivo/
│   ├── familia_a_obstaculo/
│   ├── familia_b_compleja/
│   ├── familia_c1_terreno_rugoso/     # incluye los 3 .zip anidados sin tocar — ver §3d
│   └── familia_c2_pendiente/
├── output/                            # committed — vacío por ahora (solo .gitkeep); scripts/ todavía no existen
└── scripts/                           # vacío por ahora — agregación/plotting queda para la sesión de escritura, posiblemente reusando experiments/_plotting/
```

`git mv` no aplicaba — la carpeta original (`R3-04_simulation`) no estaba trackeada todavía
(`git status` la marcaba `??`), así que fue un `mv` simple sin historial que preservar.
`PROGRESS.md` — columna `Data source` de R3-04 ya apuntaba al nombre correcto
(`experiments/R3-04-noise-robustness/`), no requirió cambio; su `Status` sigue en `pending`
(no se toca hasta que la prosa real se redacte en la sesión de escritura).

**Pendiente para la sesión de escritura:** escribir `scripts/` que lean `data/`, produzcan el CSV
limpio (sin `lambda_efficiency`/`exp_lambda`/`rmse_ct`, con el campo `perturbations` parseado desde
su repr-de-dict de Python a JSON válido) y las figuras/tablas de §6 en `output/`, luego
`scripts/promote_figure.sh` hacia `assets/`, y solo entonces editar `sections/*.tex`.

---

## 6. Contenido propuesto para el paper (heredado del documento del equipo, sin cambios — ver
`robustez_transferencia_tecnica.md` Secciones 11–12 para el detalle completo)

- **Figura R1** — `Tswitch` vs. `noise_level_idx`, una serie por familia comportamental (apetitivo,
  aversivo, obstáculo, compleja), solo trials `SUCCESS`.
- **Figura R2** — `roll_rms`/`pitch_rms` vs. `noise_level_idx`, familias `c1`/`c2`.
- **Figura R3** — evidencia de dropout de cámara (`familia_a_apetitivo` trial 7, `FAILURE_TIMEOUT`
  vs. reintento `SUCCESS`) — **ya defendible sin caveat, ver hallazgo §4**.
- **Tabla R1** — tasa de fallo por familia y tipo de fallo (conteos literales, ya tabulados en el
  documento del equipo, Sección 10).
- **Tabla R2** — parámetros de perturbación por sensor (reproducibilidad metodológica).
- Cambios de prosa requeridos en `methodology.tex` (§2.3), `results.tex` (§3.1 nueva subsección,
  §3.4 Limitations), y `conclusions.tex` — ver tabla completa en
  `robustez_transferencia_tecnica.md` Sección 12, con la matización adicional de §4 de este
  documento (LiDAR llega a evasión motriz, no a la competencia de tres vías del circuito de
  ganglios basales, en este dataset específico).

---

## Preguntas abiertas para el equipo antes de redactar (no bloquean el resto del plan)

1. Confirmar si el `G=0` hardcodeado (§4) fue intencional para estas 6 suites, o es un descuido que
   invalida parcialmente la afirmación de "robustez de arbitración ante ruido LiDAR" tal como está
   planteada en el documento de transferencia.
2. Confirmar si el commit `c6536f5` es efectivamente el que generó `familia_c2_pendiente` (o si hubo
   un commit intermedio no pusheado en el momento).
3. Confirmar la naturaleza de los 3 `.zip` anidados en `familia_c1_terreno_rugoso` (§3d) — ¿corridas
   descartadas, versión alterna, o datos de prueba del harness?
