// R2-04-mlp-onboard-compute -- standalone forward-pass benchmark on ESP32-S3.
//
// Measures ONLY the MLP forward pass (no gait/kinematics/servo/IMU-in-the-loop
// code -- those live in PETER_SIMULATION/Repository/Peter_arduino/, untouched).
// Two things happen, in order:
//   1. Correctness self-check: run forward() on each embedded TEST_INPUT_i and
//      print it next to EXPECTED_OUTPUT_i (computed in Python at export time)
//      -- confirm they match within tolerance BEFORE trusting the latency
//      number below (see experiments/R2-04-mlp-onboard-compute/README.md).
//   2. Latency benchmark: repeat forward() N=1000 times on TEST_INPUT_0,
//      report mean +/- SD in microseconds over Serial.
//
// RAM/Flash footprint is NOT measured here -- read it from the "RAM:"/
// "Flash:" lines PlatformIO prints automatically at the end of `pio run`.

#include <Arduino.h>
#include <math.h>
#include "mlp_weights.h"

static float hidden1[HIDDEN1_SIZE];
static float hidden2[HIDDEN2_SIZE];
static float logits[NUM_CLASSES];
static float scaled[INPUT_SIZE];
static float output[NUM_CLASSES];

static inline float leaky_relu(float x) {
    return x > 0.0f ? x : LEAKY_RELU_SLOPE * x;
}

// out[o] = b[o] + sum_i w[o*in + i] * x[i]   (row-major, matches PyTorch nn.Linear)
static void linear(const float* x, const float* w, const float* b,
                    int in_features, int out_features, float* out) {
    for (int o = 0; o < out_features; o++) {
        float acc = b[o];
        const float* wrow = w + (size_t)o * in_features;
        for (int i = 0; i < in_features; i++) {
            acc += wrow[i] * x[i];
        }
        out[o] = acc;
    }
}

static void softmax(const float* x, int n, float* out) {
    float m = x[0];
    for (int i = 1; i < n; i++) if (x[i] > m) m = x[i];
    float sum = 0.0f;
    for (int i = 0; i < n; i++) {
        out[i] = expf(x[i] - m);
        sum += out[i];
    }
    for (int i = 0; i < n; i++) out[i] /= sum;
}

// Full forward pass: scaler -> Linear+LeakyReLU x2 -> Linear -> softmax.
static void forward(const float* input, float* out) {
    for (int i = 0; i < INPUT_SIZE; i++) {
        scaled[i] = (input[i] - SCALER_MEAN[i]) / SCALER_SCALE[i];
    }
    linear(scaled, W1, B1, INPUT_SIZE, HIDDEN1_SIZE, hidden1);
    for (int i = 0; i < HIDDEN1_SIZE; i++) hidden1[i] = leaky_relu(hidden1[i]);

    linear(hidden1, W2, B2, HIDDEN1_SIZE, HIDDEN2_SIZE, hidden2);
    for (int i = 0; i < HIDDEN2_SIZE; i++) hidden2[i] = leaky_relu(hidden2[i]);

    linear(hidden2, W3, B3, HIDDEN2_SIZE, NUM_CLASSES, logits);
    softmax(logits, NUM_CLASSES, out);
}

void setup() {
    Serial.begin(115200);
    delay(2000);
    Serial.println("=== R2-04 MLP onboard compute: correctness self-check ===");

    bool all_ok = true;
    for (int v = 0; v < NUM_TEST_VECTORS; v++) {
        forward(TEST_INPUTS[v], output);
        Serial.printf("TEST_INPUT_%d -> C=[", v);
        for (int c = 0; c < NUM_CLASSES; c++) Serial.printf("%.6f%s", output[c], c + 1 < NUM_CLASSES ? ", " : "");
        Serial.printf("]  expected(Python)=[");
        for (int c = 0; c < NUM_CLASSES; c++) Serial.printf("%.6f%s", EXPECTED_OUTPUTS[v][c], c + 1 < NUM_CLASSES ? ", " : "");
        Serial.println("]");

        for (int c = 0; c < NUM_CLASSES; c++) {
            if (fabsf(output[c] - EXPECTED_OUTPUTS[v][c]) > 1e-3f) {
                all_ok = false;
                Serial.printf("  MISMATCH on class %d (tol=1e-3) -- do NOT trust the latency number below\n", c);
            }
        }
    }
    Serial.println(all_ok ? "Self-check: OK, all vectors within 1e-3" : "Self-check: FAILED");

    Serial.println("=== Latency benchmark: N=1000 forward() calls on TEST_INPUT_0 ===");
    const int N = 1000;
    static float latencies_us[N];
    for (int i = 0; i < N; i++) {
        uint32_t t0 = micros();
        forward(TEST_INPUTS[0], output);
        uint32_t t1 = micros();
        latencies_us[i] = (float)(t1 - t0);
    }
    double sum = 0.0;
    for (int i = 0; i < N; i++) sum += latencies_us[i];
    double mean = sum / N;
    double var = 0.0;
    for (int i = 0; i < N; i++) var += (latencies_us[i] - mean) * (latencies_us[i] - mean);
    double sd = sqrt(var / N);

    Serial.printf("Latency: mean=%.3f us, sd=%.3f us, N=%d\n", mean, sd, N);
    Serial.println("=== Done. Copy this console output into output/onboard_compute_results.txt ===");
}

void loop() {
    // Nothing -- setup() prints everything once and the board idles.
    delay(10000);
}
