"""
Servo homing repeatability simulator.

Compares two ways of finding the home position of a linear axis:
  A) single fast approach to the home sensor
  B) fast search -> back off -> slow creep -> zero reset

No hardware, no vendor libraries. The numbers below are illustrative defaults;
change them to match your own axis and run again.
"""
import random
import statistics as st

# ---- Axis model (illustrative values) ------------------------------------
V_FAST = 200.0        # mm/s   fast search speed
V_CREEP = 5.0         # mm/s   creep speed
DECEL = 5000.0        # mm/s^2 nominal deceleration after sensor trips
DECEL_VAR = 0.05      # +/-5 % run-to-run deceleration variation (load, friction)
LATENCY_MEAN = 0.005  # s      sensor + scan-time delay before motion reacts
LATENCY_SD = 0.002    # s      jitter in that delay
BACKOFF_MM = 10.0     # mm     retreat past the sensor edge
TRAVEL_MM = 300.0     # mm     distance from start to sensor


def stop_error(speed):
    """Distance travelled past the sensor edge before the axis stops (mm)."""
    latency = max(0.0, random.gauss(LATENCY_MEAN, LATENCY_SD))
    a = DECEL * (1 + random.uniform(-DECEL_VAR, DECEL_VAR))
    return speed * latency + speed ** 2 / (2 * a)


def home_single_pass():
    t = TRAVEL_MM / V_FAST
    return stop_error(V_FAST), t


def home_four_step():
    t = TRAVEL_MM / V_FAST            # 1. fast search
    t += BACKOFF_MM / V_FAST          # 2. back off past the edge
    t += BACKOFF_MM / V_CREEP         # 3. slow creep to the edge
    return stop_error(V_CREEP), t     # 4. latch zero at the creep stop point


def run(fn, n=1000):
    errs, times = zip(*(fn() for _ in range(n)))
    mean = st.mean(errs)
    spread = max(errs) - min(errs)
    return [e - mean for e in errs], st.stdev(errs), spread, st.mean(times)


if __name__ == "__main__":
    random.seed(1)
    for name, fn in (("Single fast pass", home_single_pass),
                     ("4-step (fast/back-off/creep)", home_four_step)):
        _, sd, spread, t = run(fn)
        print(f"{name:30s} std dev {sd:7.4f} mm | spread {spread:7.4f} mm | homing time {t:5.2f} s")
