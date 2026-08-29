#!/usr/bin/env python3
"""
export_weights_to_c.py -- R2-04-mlp-onboard-compute

Reads the recovered real-implementation MLP checkpoint
(`pesos_red/parametros_modelo.json`, exported from
`pesos_red/pesos_usados_en_implementacion.pth`) and emits a single C header
(`mlp_weights.h`) with:
  - the three Linear layers' weights/biases (row-major float arrays),
  - the StandardScaler mean/scale,
  - N test input vectors (135 floats each) built from real IMU CSV logs, and
  - the expected softmax output for each test vector, computed here in pure
    Python so the firmware's forward() can be checked bit-tolerance-close
    against a known-good reference (see README.md, "Validacion").

Stdlib only -- no torch/joblib needed, because parametros_modelo.json is
already a plain-JSON dump of the state_dict (see pesos_red/parametros_modelo.json).

Architecture (confirmed from the checkpoint itself, matches results.tex 150-80):
    Linear(135, 150) -> LeakyReLU(0.01) -> Linear(150, 80) -> LeakyReLU(0.01)
    -> Linear(80, 2)

Usage:
    python3 export_weights_to_c.py \
        --checkpoint-json ../../../pesos_red/parametros_modelo.json \
        --csv ../real/Test_current_integrated_floor_t01/imu_ina.csv \
        --csv ../real/Test_current_integrated_ramp_t01/imu_ina.csv \
        --num-vectors 5 \
        --out ../output/mlp_weights.h
"""
import argparse
import csv
import json
import math
import os


def leaky_relu(x, slope=0.01):
    return x if x > 0 else slope * x


def linear(x, w, b, in_features, out_features):
    """w is row-major [out_features x in_features] (PyTorch nn.Linear layout)."""
    out = [0.0] * out_features
    for o in range(out_features):
        acc = b[o]
        base = o * in_features
        for i in range(in_features):
            acc += w[base + i] * x[i]
        out[o] = acc
    return out


def softmax(x):
    m = max(x)
    exps = [math.exp(v - m) for v in x]
    s = sum(exps)
    return [v / s for v in exps]


def load_checkpoint(path):
    with open(path) as f:
        d = json.load(f)

    layers = {l["name"]: l for l in d["layers"] if l["type"] == "linear"}
    assert set(layers) == {"net.0", "net.3", "net.6"}, sorted(layers)

    def flat_weight(layer):
        # weight is stored as [out_features][in_features] nested lists (PyTorch layout).
        w = layer["params"]["weight"]
        flat = [v for row in w for v in row]
        return flat

    def bias(layer):
        return list(layer["params"]["bias"])

    ck = {
        "input_size": d["input_size"],
        "num_classes": d["num_classes"],
        "hidden1": layers["net.0"]["out_features"],
        "hidden2": layers["net.3"]["out_features"],
        "W1": flat_weight(layers["net.0"]), "B1": bias(layers["net.0"]),
        "W2": flat_weight(layers["net.3"]), "B2": bias(layers["net.3"]),
        "W3": flat_weight(layers["net.6"]), "B3": bias(layers["net.6"]),
        "scaler_mean": list(d["preprocessing"]["mean"]),
        "scaler_scale": list(d["preprocessing"]["scale"]),
    }
    assert ck["input_size"] == 135, ck["input_size"]
    assert ck["hidden1"] == 150 and ck["hidden2"] == 80, (ck["hidden1"], ck["hidden2"])
    return ck


def forward_reference(x, ck):
    """Pure-Python reference forward pass, mirrors export_weights_to_c's own
    understanding of the checkpoint -- used ONLY to produce EXPECTED_OUTPUT_i
    for the firmware's own runtime self-check, not as an independent oracle."""
    xs = [(x[i] - ck["scaler_mean"][i]) / ck["scaler_scale"][i] for i in range(len(x))]
    h1 = linear(xs, ck["W1"], ck["B1"], ck["input_size"], ck["hidden1"])
    h1 = [leaky_relu(v) for v in h1]
    h2 = linear(h1, ck["W2"], ck["B2"], ck["hidden1"], ck["hidden2"])
    h2 = [leaky_relu(v) for v in h2]
    logits = linear(h2, ck["W3"], ck["B3"], ck["hidden2"], ck["num_classes"])
    return softmax(logits)


# --- Test-vector construction from real IMU CSV logs --------------------
#
# CAVEAT (documented explicitly, see README.md "Limitaciones"): the
# `experiments/real/*/imu_ina.csv` logs were captured for the energy
# experiment (R2-04-mode-energy) and only contain
# time_s,qx,qy,qz,qw,ax,ay,az,gx,gy,gz,current_A,voltage_V,power_W,robot_cmd
# -- there is no logged `direccion` (1-7 obstacle-direction enum consumed by
# mlp_imu.py's MAPA_DIR), and `robot_cmd` is a single teleop keystroke
# character (c/i/j/k/l/u/x/z), not the numeric `modo` feature the live MLP
# pipeline consumes. bit0/bit1/bit2 AND modo are therefore fixed to 0.0 here
# -- only ax, ay, az, gx, gy are real hardware sensor values. This does NOT
# weaken the validation in step 3.3 of the plan: that check only needs the C
# forward() to reproduce whatever fixed input this script feeds it,
# bit-tolerance-close to the Python reference above -- it is not a claim that
# these vectors are the literal bytes seen live in the field.
WINDOW = 15
FEATURES_PER_ROW = 9  # ax, ay, az, gx, gy, bit0, bit1, bit2, modo


def rows_from_csv(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ax, ay, az = float(row["ax"]), float(row["ay"]), float(row["az"])
            gx, gy = float(row["gx"]), float(row["gy"])
            rows.append([ax, ay, az, gx, gy, 0.0, 0.0, 0.0, 0.0])
    return rows


def build_test_vectors(csv_paths, num_vectors):
    all_rows = []
    for p in csv_paths:
        all_rows.extend(rows_from_csv(p))
    vectors = []
    stride = max(1, (len(all_rows) - WINDOW) // max(1, num_vectors))
    start = 0
    while len(vectors) < num_vectors and start + WINDOW <= len(all_rows):
        window = all_rows[start:start + WINDOW]
        flat = [v for row in window for v in row]
        vectors.append(flat)
        start += stride
    return vectors


# --- C header emission ----------------------------------------------------

def c_float_literal(v):
    s = f"{v:.9g}"
    # A bare "0" or "-1" has no '.'/'e' -- "0f"/"-1f" is not a valid C float
    # literal (gcc: "invalid suffix 'f' on integer constant"). Force a decimal
    # point so it always lexes as a float, e.g. "0" -> "0.0", "-1" -> "-1.0".
    if "." not in s and "e" not in s and "E" not in s:
        s += ".0"
    return s + "f"


def c_array(name, values, per_line=10):
    lines = [f"static const float {name}[{len(values)}] = {{"]
    for i in range(0, len(values), per_line):
        chunk = values[i:i + per_line]
        lines.append("    " + ", ".join(c_float_literal(v) for v in chunk) + ",")
    lines.append("};")
    return "\n".join(lines)


def write_header(path, ck, test_vectors, expected_outputs):
    with open(path, "w") as f:
        f.write("// AUTO-GENERATED by export_weights_to_c.py -- do not edit by hand.\n")
        f.write("// Source: pesos_red/parametros_modelo.json (pesos_usados_en_implementacion.pth)\n")
        f.write("// Architecture: Linear(135,150) -> LeakyReLU(0.01) -> Linear(150,80)\n")
        f.write("//               -> LeakyReLU(0.01) -> Linear(80,2)\n")
        f.write("#pragma once\n\n")
        f.write(f"#define INPUT_SIZE {ck['input_size']}\n")
        f.write(f"#define HIDDEN1_SIZE {ck['hidden1']}\n")
        f.write(f"#define HIDDEN2_SIZE {ck['hidden2']}\n")
        f.write(f"#define NUM_CLASSES {ck['num_classes']}\n")
        f.write("#define LEAKY_RELU_SLOPE 0.01f\n")
        f.write(f"#define NUM_TEST_VECTORS {len(test_vectors)}\n\n")

        # NOTE: bias arrays are named BIAS1/2/3, not B1/B2/B3 -- the Arduino core
        # (binary.h) #defines B0..B11111111 as binary-literal macros (e.g. B1 -> 1),
        # so "B1"/"B2"/"B3" silently expand to integers and break compilation.
        f.write(c_array("W1", ck["W1"]) + "\n\n")
        f.write(c_array("BIAS1", ck["B1"]) + "\n\n")
        f.write(c_array("W2", ck["W2"]) + "\n\n")
        f.write(c_array("BIAS2", ck["B2"]) + "\n\n")
        f.write(c_array("W3", ck["W3"]) + "\n\n")
        f.write(c_array("BIAS3", ck["B3"]) + "\n\n")
        f.write(c_array("SCALER_MEAN", ck["scaler_mean"]) + "\n\n")
        f.write(c_array("SCALER_SCALE", ck["scaler_scale"]) + "\n\n")

        for i, (vec, out) in enumerate(zip(test_vectors, expected_outputs)):
            f.write(c_array(f"TEST_INPUT_{i}", vec) + "\n\n")
            f.write(c_array(f"EXPECTED_OUTPUT_{i}", out, per_line=2) + "\n\n")

        f.write("static const float* const TEST_INPUTS[NUM_TEST_VECTORS] = {\n")
        f.write(",\n".join(f"    TEST_INPUT_{i}" for i in range(len(test_vectors))))
        f.write("\n};\n\n")
        f.write("static const float* const EXPECTED_OUTPUTS[NUM_TEST_VECTORS] = {\n")
        f.write(",\n".join(f"    EXPECTED_OUTPUT_{i}" for i in range(len(test_vectors))))
        f.write("\n};\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint-json", required=True,
                     help="Path to pesos_red/parametros_modelo.json")
    ap.add_argument("--csv", action="append", required=True,
                     help="Real IMU CSV to source test-vector windows from (repeatable)")
    ap.add_argument("--num-vectors", type=int, default=5)
    ap.add_argument("--out", required=True, help="Output path for mlp_weights.h")
    args = ap.parse_args()

    ck = load_checkpoint(args.checkpoint_json)
    test_vectors = build_test_vectors(args.csv, args.num_vectors)
    if not test_vectors:
        raise SystemExit("No se pudieron construir vectores de prueba (CSV muy corto?)")
    expected = [forward_reference(v, ck) for v in test_vectors]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    write_header(args.out, ck, test_vectors, expected)

    print(f"OK: {args.out}")
    print(f"  arquitectura: {ck['input_size']} -> {ck['hidden1']} -> {ck['hidden2']} -> {ck['num_classes']}")
    print(f"  vectores de prueba: {len(test_vectors)}")
    for i, out in enumerate(expected):
        print(f"  EXPECTED_OUTPUT_{i} (softmax) = {out}")


if __name__ == "__main__":
    main()
