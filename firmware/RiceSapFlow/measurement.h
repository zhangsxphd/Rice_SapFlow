#pragma once
#include <stdint.h>
#include <math.h>

// Independent of Arduino so pulse safety and measurement transitions can be tested.
class Measurement {
public:
  enum Phase { IDLE, HEATING, OBSERVING, FAULT };
  static constexpr uint32_t MAX_PULSE_MS = 3000;
  static constexpr uint32_t COOLDOWN_MS = 120000;
  static constexpr uint32_t OBSERVE_MS = 90000;
  static constexpr uint32_t MAX_SAMPLE_AGE_MS = 350;
  static constexpr float MAX_TEMP_C = 40.0f;
  static constexpr float MAX_RISE_C = 2.0f;
  Phase phase = IDLE;
  bool armed = false;
  bool heat = false;
  bool valid = false;
  bool everPulsed = false;
  uint32_t lastSampleMs = 0, pulseStartMs = 0, pulseLengthMs = 0;
  uint32_t armMs = 0, observedMs = 0;
  float up = NAN, down = NAN, baseUp = NAN, baseDown = NAN;
  const char *fault = "";

  bool sample(uint32_t now, float u, float d) {
    if (!isfinite(u) || !isfinite(d) || u < -10 || d < -10 || u > MAX_TEMP_C || d > MAX_TEMP_C) {
      trip("temperature_out_of_range"); return false;
    }
    up = u; down = d; valid = true; lastSampleMs = now;
    if (phase == HEATING || phase == OBSERVING) {
      if (u - baseUp > MAX_RISE_C || d - baseDown > MAX_RISE_C) {
        trip("temperature_rise_limit"); return false;
      }
    } else if (phase == IDLE) {
      baselineU[index] = u; baselineD[index] = d;
      index = (index + 1) % 30;
      if (count < 30) ++count;
    }
    return true;
  }
  bool arm(uint32_t now) {
    if (phase != IDLE || !fresh(now) || count < 20 || !stable()) return false;
    armed = true; armMs = now; return true;
  }
  bool start(uint32_t now, uint32_t duration) {
    if (!armed || phase != IDLE || !fresh(now) || count < 20 || !stable() ||
        uint32_t(now - armMs) > 60000 ||
        duration < 100 || duration > MAX_PULSE_MS ||
        (everPulsed && uint32_t(now - pulseStartMs) < COOLDOWN_MS)) return false;
    baseUp = mean(baselineU); baseDown = mean(baselineD);
    armed = false; heat = true; phase = HEATING; everPulsed = true;
    pulseStartMs = now; pulseLengthMs = duration; return true;
  }
  void tick(uint32_t now) {
    if (armed && uint32_t(now - armMs) > 60000) armed = false;
    if ((phase == HEATING || phase == OBSERVING) && !fresh(now)) {
      trip("sensor_stale"); return;
    }
    if (phase == HEATING && uint32_t(now - pulseStartMs) >= pulseLengthMs) {
      heat = false; phase = OBSERVING; observedMs = now;
    }
    if (phase == OBSERVING && uint32_t(now - pulseStartMs) >= OBSERVE_MS) {
      heat = false; phase = IDLE; count = 0; index = 0;
    }
  }
  void cancel() {
    heat = false; armed = false;
    if (phase != FAULT) phase = IDLE;
    count = 0; index = 0;
  }
  void trip(const char *reason) {
    heat = false; armed = false; valid = false; phase = FAULT; fault = reason;
    count = 0; index = 0;
  }
  bool reset() {
    if (heat) return false;
    phase = IDLE; fault = ""; armed = false; valid = false; count = 0; index = 0;
    return true;
  }
  bool fresh(uint32_t now) const {
    return valid && uint32_t(now - lastSampleMs) <= MAX_SAMPLE_AGE_MS;
  }
  float riseUp() const { return up - baseUp; }
  float riseDown() const { return down - baseDown; }
  float ratio() const {
    if (!valid || (phase != HEATING && phase != OBSERVING) ||
        riseUp() < 0.05f || riseDown() < 0.05f) return NAN;
    return riseDown() / riseUp();
  }
  const char *phaseName() const {
    switch (phase) {
      case HEATING: return "heating";
      case OBSERVING: return "observing";
      case FAULT: return "fault";
      default: return "idle";
    }
  }
private:
  float baselineU[30] = {}, baselineD[30] = {};
  unsigned count = 0, index = 0;
  float mean(const float *a) const {
    float s = 0; for (unsigned i = 0; i < count; ++i) s += a[i];
    return count ? s / count : NAN;
  }
  bool stable() const {
    float umin = baselineU[0], umax = umin, dmin = baselineD[0], dmax = dmin;
    for (unsigned i = 1; i < count; ++i) {
      if (baselineU[i] < umin) umin = baselineU[i];
      if (baselineU[i] > umax) umax = baselineU[i];
      if (baselineD[i] < dmin) dmin = baselineD[i];
      if (baselineD[i] > dmax) dmax = baselineD[i];
    }
    return umax - umin <= 0.15f && dmax - dmin <= 0.15f;
  }
};
