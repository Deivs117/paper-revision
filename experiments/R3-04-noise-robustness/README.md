# R3-04 — Robustez sensorial de la arbitración de marcha (IMU drift / LiDAR noise / illumination)

**Reviewer ask:** *"No noise interference robustness experiments are designed for the whole
perception-decision pipeline. The paper does not test the system's gait arbitration performance
under IMU drift, LiDAR distance noise, and camera illumination distortion..."* (R3-04).

**Estado de este directorio:** reorganizado y auditado (2026-08-31) a partir de la entrega cruda del
equipo de simulación. **Aún no se generaron las figuras/tablas finales** (`output/` solo tiene los
datos de origen, sin procesar) ni se escribió la prosa del paper — eso es trabajo de la siguiente
sesión. El análisis completo de qué se puede y no se puede afirmar con estos datos vive en
`intake/pending/R3-04_audit_and_plan.md` (léase antes de generar cualquier figura o escribir
prosa) y en `robustez_transferencia_tecnica.md` (documento de transferencia original del equipo,
conservado aquí como fuente).

## Goal

Producir la Figura R1 (Tswitch vs. nivel de perturbación, 4 familias comportamentales), Figura R2
(roll/pitch RMS vs. nivel de perturbación, terreno rugoso + pendiente), Figura R3 (evidencia de
dropout de cámara → fallo de tarea), Tabla R1 (tasa de fallo por familia) y Tabla R2 (parámetros de
perturbación por sensor) para la fila `R3-04` de `PROGRESS.md`. También sustenta la revisión de
`sections/methodology.tex` §2.3 y `sections/results.tex` §3.1/§3.4 (ver el detalle de cambios
requeridos en `robustez_transferencia_tecnica.md` Sección 12).

## Método

Un único parámetro ROS (`noise_level_idx`, 0–4) escala **simultáneamente** tres mecanismos de
perturbación sobre el pipeline de percepción del nodo `NetworkPublisher` (`red_neuronal.py`):

1. **Deriva de IMU** — random-walk acumulativo sobre ax/ay/az/roll/pitch (`_update_imu_drift`), no
   ruido de media cero. El ruido blanco gaussiano de IMU heredado de versiones previas está
   deshabilitado en esta corrida (`_sigma_imu_noise = 0.0`, ver `config.yaml`).
2. **Ruido de rango del LiDAR** — gaussiano proporcional al rango medido (mismo modelo que
   versiones anteriores), indexado por su propio array `LidarNoiseLevels`.
3. **Distorsión de iluminación de cámara** — sesgo sistemático de área + dropout probabilístico +
   jitter de posición del bounding box (`_apply_illumination_distortion`); actúa sobre las
   características ya extraídas del detector de blobs, no sobre píxeles de imagen.

**No existe una condición que aísle un solo sensor** — cada nivel > 0 es ya una condición
multisensor combinada; ver "Data provenance" para el hallazgo (verificado en el código fuente) sobre
qué canales de arbitración reciben efectivamente cada perturbación.

Se ejecutaron 6 suites de simulación (Gazebo/ROS 2, mismo entorno que el resto del paper),
reutilizando escenarios comportamentales y de terreno ya existentes: apetitivo, aversivo, evasión de
obstáculo, escenario complejo, terreno rugoso, pendiente. Cada suite: 5 niveles × 3 réplicas
`SUCCESS` retenidas (con reintentos ante fallo cuando fue necesario). Solo simulación — el robot
físico no está disponible actualmente (desensamblado).

## Parámetros / seed

Ver `config.yaml`. La corrida **no es reproducible bit-a-bit** solo con `scripts/` + `config.yaml`
(a diferencia de otros experimentos de este repo) — requirió una ejecución real del simulador
Gazebo/ROS 2 por el equipo de simulación; ver "Data provenance" para el paso manual exacto que
produjo `data/`.

## Data provenance

- **Fuente:** ejecución real de las 6 suites en Gazebo/ROS 2 por el equipo de simulación,
  entregada como `familia_*/` (manifiestos + `trial_summary.json`/`unified_metrics.csv`/
  `metrics_raw.csv` por trial) el 2026-08-28 a 2026-08-30, más `consolidated_results.csv`
  (112 filas, entregado el 2026-08-31) y el documento de transferencia
  `robustez_transferencia_tecnica.md`.
- **Commit de `PETER_SIMULATION` pinneado** (verificado por auditoría cruzando fechas de commit
  contra fechas de generación de cada carpeta — ver `intake/pending/R3-04_audit_and_plan.md` §4
  para el detalle completo):
  - `familia_a_apetitivo`, `familia_a_aversivo`, `familia_a_obstaculo`, `familia_b_compleja`,
    `familia_c1_terreno_rugoso` → commit `04925ed0b5c7cd2de876fac69e90108dc3fcc281`
    ("robustness v2 funcional", rama `dieguito`, 2026-08-27 21:21).
  - `familia_c2_pendiente` → probablemente commit `c6536f59a3a31a57439b60df4017f9d17d981f70`
    ("Cambios mayores...", rama `dieguito`, 2026-08-30 19:31) — **sin confirmar con el equipo**,
    inferido solo por timestamp (mtime de la carpeta es posterior al commit).
  - **No usar** el commit `b37020d97c7431313d16e985a7b445c38397cdc0` ("Fix...", 2026-08-31) como
    referencia de proveniencia: es posterior a la entrega de todos estos datos y cambia
    comportamiento relevante (introduce el flag `pruebaDeTerreno`, ausente en los dos commits de
    arriba).
- **Hallazgos verificados directamente contra el código fuente de esos dos commits** (no inferidos
  del documento del equipo, que no tenía acceso al historial de commits):
  - La distorsión de iluminación de cámara **estuvo activa sin excepción** en las 6 suites (el
    flag que la desactivaría condicionalmente no existía todavía en ninguno de los dos commits
    pinneados arriba).
  - El canal `G` (LiDAR → competencia de arbitraje StN/Gpi/Gpe/StR) está hardcodeado a `G = 0`
    justo después de calcularse, en ambos commits — el ruido de LiDAR no llega a esa competencia
    de tres vías en este dataset. Sí llega, en cambio, a la vía de evasión/dirección motriz
    (`z[5]`–`z[13]`, que consumen `self.lidar[2..4]` directamente). Ver
    `intake/pending/R3-04_audit_and_plan.md` §4 antes de redactar cualquier afirmación sobre "el
    ruido de LiDAR se propaga hasta la arbitración de ganglios basales".
- Métricas de estabilidad por muestra (`stability_log.csv`, columnas SM/TR/inradius) están casi
  vacías (solo 7/15 trials de `familia_c2_pendiente` tienen filas de datos reales) — usar en su
  lugar el campo `tr` de `trial_summary.json`, bien poblado. Ver auditoría completa de campos
  útiles/inútiles en `intake/pending/R3-04_audit_and_plan.md` §3.

## How to regenerate

No regenerable desde cero con un solo comando (ver arriba). Para reprocesar los datos ya
entregados una vez que existan scripts en `scripts/`:

```
cd experiments/R3-04-noise-robustness
python3 scripts/<pendiente>.py   # agregación + figuras — no implementado todavía en esta sesión
```

## Output files

| File in `output/` | Promoted to (`assets/...`) | Used in |
|---|---|---|
| *(pendiente — no generado en esta sesión de auditoría/planificación)* | — | Fig. R1/R2/R3, Tabla R1/R2 — ver `intake/pending/R3-04_audit_and_plan.md` §6 |
