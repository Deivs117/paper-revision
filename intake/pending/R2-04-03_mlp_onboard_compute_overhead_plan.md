# R2-04-03 — Plan: overhead de cómputo embebido del MLP en la ESP32-S3 (onboard deployment)

**Estado: 🔲 PLAN, BLOQUEADO** en el paso 1 (esperando checkpoint 150-80 real) — no ejecutable hoy más
allá de dejar el andamiaje (script de exportación, esqueleto PlatformIO) listo para cuando llegue el
checkpoint.

**Origen:** fila `R2-04` de `PROGRESS.md`, cláusula "embedded computing overhead of the MLP network
for onboard deployment analysis" — distinta de la cláusula de energía por modo (esa ya está cerrada,
ver `intake/processed/R02-01-03_energia_transicion_y_modo_R2-04.md`).

## 1. Alcance — qué pide el revisor realmente, y qué NO hace falta

El enunciado del revisor tiene dos cláusulas separadas: "Supplement (A) long-term average energy
consumption of three locomotion modes **and** (B) embedded computing overhead of the MLP network for
onboard deployment analysis."

- **(A)** ya está cerrado (tabla `tab:mode_steady_state_energy`).
- **(B)** es costo de **cómputo** (latencia/memoria), no de energía — es una métrica distinta. El
  número que ya existe en `results.tex:591` (MLP = 1.64 μs/muestra) fue medido **en host**
  (PyTorch/sklearn en PC), nunca en la ESP32-S3 real, así que no responde honestamente a "onboard
  deployment analysis" — la inferencia real, hoy, corre en el PC (`RED_PETER_CONSOLA.py` /
  `PETER_SIMULATION/.../mlp_imu.py`), la ESP solo hace adquisición IMU + control de actuadores.

**Decisión de alcance (2026-08-29):** este bloque solo mide **latencia de inferencia + huella de
memoria (RAM/Flash) del forward-pass del MLP corriendo dentro de la ESP32-S3**. No se mide corriente
ni energía específica del MLP — no hace falta:
1. La cláusula (B) del revisor es sobre cómputo, no energía.
2. Los sensores de corriente disponibles (WCS1600 100A DC/AC, SCT-013-000 100A/50mA) están fuera de
   rango para esto: el ESP32-S3 consume del orden de decenas/cientos de mA, muy por debajo de la
   resolución útil de un sensor de 100A; además el SCT-013 es un transformador de corriente **AC**,
   inutilizable en un riel DC como la alimentación de la placa. No usar ninguno de los dos aquí.
3. Evita instrumentación adicional (protoboard, resistencia shunt, etc.) — decisión explícita del
   autor de mantener esto simple.

## 2. Bloqueante — checkpoint 150-80 real

**El autor está buscando por fuera el checkpoint/arquitectura real 150-80** que sí coincide con lo ya
publicado en `methodology.tex`/`results.tex` (F1=0.771, ablation study). Confirmado en esta sesión de
planeación (2026-08-29) que **no existe ningún archivo `.pth`/dataset de entrenamiento 150-80 en
ningún repo de `~/Documents/Paper/`** — el único checkpoint real presente es
`pesos_red/modelo_mlp.pth` (arquitectura 200-100, confirmada leyendo los tamaños de tensor del zip
interno del `.pth`, sin necesitar `torch` instalado: `108000B→135×200`, `80000B→200×100`,
`800B→100×2`). Los números 150-80 ya publicados provienen de vectorización de píxeles de un PNG
antiguo (`experiments/_plotting/vectorized/README.md`: "no raw training log survives"), no de un
modelo vivo.

**Este bloque no se puede correr hasta que llegue** (de parte del autor) uno de estos dos:
- Un checkpoint 150-80 real (`.pth` + `escalador.pkl`/normalizador equivalente), o
- Confirmación explícita de que se usa la arquitectura 200-100 real (`pesos_red/modelo_mlp.pth`) y que
  el paper se corrige para coincidir con ella.

**Formato exacto que necesito del checkpoint, sea cual sea la arquitectura final:**
- Archivo de pesos compatible con `torch.load` (state_dict de `nn.Sequential` con capas `Linear`/
  `ReLU` alternadas) o, si no es PyTorch, cualquier formato del que se puedan extraer arrays de pesos
  + biases por capa (no hace falta que sea `.pth` específicamente).
- El normalizador usado antes de la red (`escalador.pkl` de `sklearn.StandardScaler`, o equivalente) —
  necesito `mean_`/`scale_` (o `min_`/`max_` si es MinMax) para poder reproducir el mismo
  preprocesamiento en C.
- Confirmar `input_size` (135 si sigue siendo ventana de 15×9) y `num_classes` (2: plano/inclinado).

## 3. Plan de implementación (una vez llegue el checkpoint)

### 3.1 Script de exportación de pesos → C (en `paper-revision/experiments/R2-04-mlp-onboard-compute/scripts/`)

`export_weights_to_c.py` (Python, host, usa `torch`+`joblib`, mismas dependencias que ya usa
`pesos_red/RED_PETER_CONSOLA.py`):
- Carga el `state_dict` del checkpoint final y el normalizador.
- Para cada capa `Linear`, escribe sus pesos y bias como arrays `float` planos (row-major) en un
  header C, ej. `mlp_weights.h`:
  ```c
  #define INPUT_SIZE 135
  #define HIDDEN1_SIZE <200 o 150, según checkpoint final>
  #define HIDDEN2_SIZE <100 o 80>
  #define NUM_CLASSES 2
  static const float W1[INPUT_SIZE * HIDDEN1_SIZE] = { ... };
  static const float B1[HIDDEN1_SIZE] = { ... };
  static const float W2[HIDDEN1_SIZE * HIDDEN2_SIZE] = { ... };
  static const float B2[HIDDEN2_SIZE] = { ... };
  static const float W3[HIDDEN2_SIZE * NUM_CLASSES] = { ... };
  static const float B3[NUM_CLASSES] = { ... };
  static const float SCALER_MEAN[INPUT_SIZE] = { ... };
  static const float SCALER_SCALE[INPUT_SIZE] = { ... };
  ```
- **Vectores de prueba embebidos:** el mismo script toma 3-5 ventanas reales de 135 valores (de
  `experiments/real/Test_current_integrated_floor_t01/imu_ina.csv` y `..._ramp_t01/imu_ina.csv`,
  aplicando la misma ventana deslizante de 15 muestras × 9 features que usa
  `test_mlp()`/`red_python_lidar_cam_imu_sg.py` — 5 canales IMU crudos + 3 bits de dirección + modo,
  descartando `gz`) y las escribe también como arrays C (`TEST_INPUT_0[135]`, etc.), junto con la
  salida esperada del modelo en Python para esos mismos vectores (`EXPECTED_OUTPUT_0[2]`, softmax) —
  esto es lo que permite validar en el paso 3.3 que la implementación en C reproduce el mismo
  resultado que PyTorch, sin necesitar replicar el preprocesamiento de ventana dentro del firmware
  (el benchmark de cómputo no necesita leer sensores en vivo).
- No se commitea el checkpoint `.pth` crudo dentro de `experiments/` si es grande/binario innecesario
  para el pipeline — solo el header `.h` generado (texto, revisable, pequeño) va a
  `experiments/R2-04-mlp-onboard-compute/output/mlp_weights.h`.

### 3.2 Firmware standalone (PlatformIO + Arduino framework, ESP32-S3)

Carpeta nueva `experiments/R2-04-mlp-onboard-compute/firmware/` (proyecto PlatformIO independiente,
**no** modifica `PETER_SIMULATION/Repository/Peter_arduino/` — sin gait, sin kinematics, sin
PCA9685/servos, sin IMU en vivo — solo el forward-pass):

`platformio.ini`:
```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200
build_flags = -O2
```
(mismo `board`/`framework` que `PETER_SIMULATION/Repository/Peter_arduino/platformio.ini`, para no
introducir un segundo toolchain — decisión ya tomada.)

`src/main.cpp`:
- Incluye `mlp_weights.h` generado en 3.1.
- Implementa `forward(const float* input, float* output)`: 2× GEMV+ReLU (capas ocultas) + GEMV final +
  softmax — sin ninguna librería externa (TFLite Micro no hace falta para una red de este tamaño,
  ~47K parámetros; matmul manual es más simple y evita la cadena de conversión PyTorch→ONNX→TF→TFLite,
  que es frágil y no siempre reproduce bit-a-bit la salida original — decisión ya tomada).
- `setup()`: normaliza cada `TEST_INPUT_i` con `SCALER_MEAN`/`SCALER_SCALE`, corre `forward()` una vez
  por vector de prueba y lo imprime por Serial junto al `EXPECTED_OUTPUT_i` — paso de validación
  (3.3).
- Luego mide latencia: repite `forward()` sobre el mismo input **N=1000 veces** (usar `micros()` antes/
  después, tomar media y SD sobre las 1000 corridas) y reporta por Serial:
  - Latencia media ± SD por inferencia (μs).
  - (Nota: RAM/Flash usados **no** se miden en runtime — se leen directo del reporte que PlatformIO
    imprime automáticamente al final de `pio run`, sección "RAM:"/"Flash:" — no requiere código
    adicional.)

### 3.3 Validación de correctitud (antes de confiar en el número de latencia)

Comparar, para cada uno de los 3-5 vectores de prueba, la salida de `forward()` en C contra
`EXPECTED_OUTPUT_i` (calculado en Python con el mismo checkpoint) — deben coincidir dentro de una
tolerancia razonable (ej. 1e-3, dado que ambos usan `float32`). Si no coinciden, el error está casi
seguro en el orden de los pesos exportados (row-major vs. column-major) o en el preprocesamiento del
normalizador — depurar ahí antes de confiar en cualquier medición de tiempo.

### 3.4 Cómo correr (una vez el firmware compila y valida)

```
cd experiments/R2-04-mlp-onboard-compute
python3 scripts/export_weights_to_c.py --checkpoint <ruta al .pth final> --scaler <ruta al escalador> \
    --out firmware/include/mlp_weights.h
cd firmware
pio run -t upload -t monitor
```
Registrar la salida de consola (latencia media±SD, y el reporte RAM/Flash del build) en
`experiments/R2-04-mlp-onboard-compute/output/onboard_compute_results.txt` (texto plano, N=1000
declarado).

## 4. Qué cambia en el paper

- `results.tex:591` (párrafo del computational-cost analysis): añadir una frase con la latencia
  **on-device real** medida en la ESP32-S3 (μs, N=1000, ± SD), aclarando explícitamente que el número
  de 1.64 μs existente es de referencia en host y que este nuevo número es la medición en el
  microcontrolador objetivo — responde directamente a "onboard deployment analysis" sin quitar el
  dato host ya existente (los dos son válidos y complementarios: uno es referencia de clasificador
  entre algoritmos, el otro es el número real de despliegue).
- Añadir footprint de memoria (RAM/Flash en bytes) del modelo en la ESP32-S3 — dato nuevo, no existe
  ninguna versión previa de esto en el paper.
- Todo el texto nuevo/modificado envuelto en `\revblue{}`, como el resto de la ronda.
- Si el checkpoint final resulta ser 200-100 (no 150-80), la corrección de arquitectura en
  `methodology.tex:357`/`results.tex:551,580,591` es un cambio previo obligatorio antes de este —
  **no** se reporta la latencia embebida de una red cuya arquitectura declarada en el paper no
  coincide con lo que realmente se corrió.

## 5. Trazabilidad — pendiente de completar cuando se cierre

- `experiments/R2-04-mlp-onboard-compute/` — carpeta a crear con `scripts/`, `firmware/`, `output/`
  (seguir `experiments/_TEMPLATE/README.md`).
- `PROGRESS.md`: fila `R2-04` — actualizar su nota para reflejar que la cláusula "MLP compute
  overhead" pasa de "already present (host)" a "medido on-device en ESP32-S3" una vez el firmware
  corra y produzca el número real; no se abre una fila nueva `N-xx`/`C-xx`, sigue siendo el mismo
  requerimiento de revisor `R2-04`.
- `git mv` este documento a `intake/processed/` solo cuando el punto 2 (checkpoint real) se resuelva y
  el firmware haya producido y validado un número real.
