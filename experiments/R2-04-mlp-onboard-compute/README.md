# R2-04-mlp-onboard-compute — embedded compute overhead of the terrain-classifier MLP

Produces the "onboard deployment" half of reviewer requirement `R2-04` (the energy half is
`experiments/R2-04-mode-energy/`, already closed). See
`intake/pending/R2-04-03_mlp_onboard_compute_overhead_plan.md` for the full history/decision log
of this block, including the checkpoint-provenance blocker that was open until 2026-08-29.

## Goal

Measure, on the actual ESP32-S3 target (not host PyTorch/sklearn), the terrain-classifier MLP's:
- per-sample inference latency (μs, mean ± SD, N=1000), and
- RAM/Flash footprint at build time.

Feeds a new sentence in `results.tex` (computational-cost-analysis paragraph, currently only
reports the host-measured 1.64 μs/sample) and, per row `R2-04`, `PROGRESS.md`.

## Method

1. `scripts/export_weights_to_c.py` reads `pesos_red/parametros_modelo.json` (a plain-JSON dump
   of `pesos_red/pesos_usados_en_implementacion.pth`'s `state_dict` + `StandardScaler`) and emits
   `firmware/include/mlp_weights.h`: the three `Linear` layers' weights/biases, the scaler's
   `mean`/`scale`, and 5 test-input vectors + their expected softmax output (computed in the same
   script, pure Python, no torch/numpy needed).
2. `firmware/` is a standalone PlatformIO project (same `board`/`framework` as
   `PETER_SIMULATION/Repository/Peter_arduino/`, deliberately not TFLite Micro — see plan doc
   §3.2 for why). `src/main.cpp` implements the forward pass by hand (2× GEMV+LeakyReLU, GEMV,
   softmax), runs the 5 self-check vectors, then benchmarks N=1000 repeated forward() calls with
   `micros()`.

## Architecture (confirmed from the checkpoint, matches `results.tex`'s published 150-80)

`Linear(135,150) -> LeakyReLU(0.01) -> Linear(150,80) -> LeakyReLU(0.01) -> Linear(80,2)`.

**Correction applied to the paper as part of this block:** `results.tex:551` said "ReLU"; the
recovered real-implementation checkpoint (`pesos_red/parametros_modelo.json`) uses
`LeakyReLU(negative_slope=0.01)` on both hidden layers. No `mlp_imu.py`/`RED_PETER_CONSOLA.py`
copy found anywhere under `PETER_SIMULATION/` defines this architecture (they all hardcode
200-100/ReLU) — the recovered `.pth` is trusted as the real-implementation source of truth per
author decision (2026-08-29), and `results.tex` was corrected to say LeakyReLU, wrapped in
`\revblue{}`.

## Parameters / seed

See `config.yaml`. No RNG is involved (forward pass on fixed test vectors + a deterministic
timing loop) — reruns should reproduce the same self-check output; wall-clock latency numbers
will vary slightly run to run (real hardware timing), that's what the SD over N=1000 captures.

## Data provenance

- Checkpoint: `pesos_red/pesos_usados_en_implementacion.pth` / `pesos_red/parametros_modelo.json`
  — recovered from the real implementation by the author (2026-08-29), outside any repo under
  `~/Documents/Paper/` (not present in `PETER_SIMULATION` at any commit checked during this
  block's planning).
- Test-vector accelerometer/gyro values: real hardware logs,
  `experiments/real/Test_current_integrated_floor_t01/imu_ina.csv` and
  `..._ramp_t01/imu_ina.csv` (already committed for `R2-04-mode-energy`).
- **Limitation (documented, does not affect the latency/footprint measurement):** those CSVs
  don't log the `direccion` (1-7 enum) or numeric `modo` features the live pipeline
  (`mlp_imu.py`) also feeds the MLP — only `robot_cmd`, a teleop keystroke character, which isn't
  the same value. `export_weights_to_c.py` therefore fixes `bit0/bit1/bit2/modo = 0.0` for all
  test vectors; `ax,ay,az,gx,gy` are real sensor values. This is fine for what these vectors are
  used for (confirm the C forward pass numerically reproduces a fixed reference input,
  bit-tolerance-close) — it is not a claim that these are literal production inputs.
- **This experiment's `data/` step (actually running the firmware) requires a physical
  ESP32-S3.** This session has no `pio`/PlatformIO toolchain and no board attached, so `pio run
  -t upload -t monitor` must be run by the author on real hardware. Everything up to that point
  was run and validated here: `mlp_weights.h` generation, and the exact `forward()`/`linear()`/
  `softmax()` logic used in `firmware/src/main.cpp` was additionally compiled standalone with
  `gcc -O2` (host, outside `firmware/`, not committed) against the generated header and produced
  output matching `EXPECTED_OUTPUT_i` exactly for all 5 test vectors — the only thing not yet
  confirmed is that the Arduino/ESP32-S3 toolchain compiles the same file without surprises and
  what real `micros()` timing looks like on-device.

## How to regenerate

```
cd experiments/R2-04-mlp-onboard-compute
python3 scripts/export_weights_to_c.py \
    --checkpoint-json ../../pesos_red/parametros_modelo.json \
    --csv ../real/Test_current_integrated_floor_t01/imu_ina.csv \
    --csv ../real/Test_current_integrated_ramp_t01/imu_ina.csv \
    --num-vectors 5 \
    --out output/mlp_weights.h
cd firmware
pio run -t upload -t monitor
```
Read the self-check section first (must say "Self-check: OK, all vectors within 1e-3" — if not,
the latency number below it is not trustworthy, see plan doc §3.3 for how to debug). Then copy
the full console output (self-check + latency line + PlatformIO's own "RAM:"/"Flash:" build
report) into `output/onboard_compute_results.txt`.

## Output files

| File in `output/` | Promoted to (`assets/...`) | Used in |
|---|---|---|
| `onboard_compute_results.txt` | n/a (numbers only, no figure) | `results.tex:592`, computational-cost-analysis paragraph |
| `mlp_weights.h` | n/a (build input, not a paper asset) | `firmware/` build only, via `platformio.ini`'s `-I../output` |

**Status as of 2026-08-29: CLOSED — real ESP32-S3 number is in `results.tex`.**

First hardware run was on the wrong chip: the board the author had on hand was identified by the
OS as an **ESP32-C3**, not the ESP32-S3 the physical robot's firmware actually targets (confirmed
in `PETER_SIMULATION/Repository/Peter_arduino/platformio.ini`). Getting it running took two real
fixes, both kept in the firmware for every subsequent run:
1. `BIAS1/2/3` instead of `B1/B2/B3` in the generated header — Arduino's `binary.h` `#define`s
   `B0`..`B11111111` as binary-literal macros, so `B1`/`B2`/`B3` silently expanded to `1`/`2`/`3`.
2. `-D ARDUINO_USB_MODE=1 -D ARDUINO_USB_CDC_ON_BOOT=1` build flags — without them, Arduino's
   `Serial` on an ESP32-C3/S3 (native USB, no separate UART bridge chip) binds to the physical
   UART0 pins instead of the USB-Serial-JTAG peripheral the USB cable is actually plugged into,
   so `Serial.println()` output silently goes nowhere reachable. (These are already the flags
   `Peter_arduino/platformio.ini` uses for the same reason — matches the established convention.)

Result on that ESP32-C3 (NOT used in the paper): self-check passed, RAM 5.9%/Flash 29.4%, mean
latency **49.892 ms** (SD 2.166 μs, N=1000) — ~30,000x slower than host, because the C3 has no
hardware FPU (RISC-V, software float emulation) unlike the S3. Real number, wrong chip — kept on
file in `output/onboard_compute_results.txt` for traceability only.

**A real ESP32-S3 was then connected (same day).** Two more real issues, both now permanently
fixed in `platformio.ini`'s `esp32-s3-devkitc-1` env:
3. First upload attempt failed transiently (`esptool`: `write failed: [Errno 19] No such device`
   mid-handshake) — a bare retry of the identical command succeeded; not seen again.
4. Genuine bootloop after that first successful flash (`assert failed: do_core_init` /
   `Detected size(4096k) smaller than the size in the binary image header(8192k)`) —
   PlatformIO's `esp32-s3-devkitc-1` board definition defaults to the 8MB "N8" flash variant, but
   the physical board has 4MB. Fixed with the same `board_build.flash_size=4MB` /
   `board_upload.flash_size=4MB` / `board_build.flash_mode=dio` /
   `board_build.flash_frequency=80m` / `board_build.partitions=default.csv` overrides
   `Peter_arduino/platformio.ini` already uses for this exact reason.

**Final result (ESP32-S3, this is what's in the paper):** self-check passed exactly — all 5
vectors match the Python reference within 1e-3 on the real target chip. Mean on-device latency
**8.814 ms** (SD 2.672 μs, N=1000), RAM 24,140 B (7.4% of 320 KB), Flash 397,829 B (30.4% of the
board's 4 MB partition, almost entirely the model weights). Still ~5,000x slower than the host
figure despite the hardware FPU — plausible given the firmware's naive scalar (non-vectorized)
matmul and `static const` weight arrays living in flash rather than RAM; noted alongside the
number in `results.tex`, see `output/onboard_compute_results.txt` for the full account. Written
into `results.tex:592` as a new `\revblue{}` sentence following the existing host-latency
sentence — see `patches/r2-04-mlp-onboard-compute.tex` for the exact wording diff.
