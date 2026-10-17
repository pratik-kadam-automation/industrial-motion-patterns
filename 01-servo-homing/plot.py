"""Regenerates repeatability.svg. Requires matplotlib (pip install matplotlib)."""
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import simulate as s

random.seed(1)
a, *_ = s.run(s.home_single_pass)
b, *_ = s.run(s.home_four_step)
fig, ax = plt.subplots(figsize=(8, 4.5), facecolor="#0f172a")
ax.set_facecolor("#0f172a")
ax.hist(a, bins=60, alpha=.8, color="#f87171", label="Single fast pass")
ax.hist(b, bins=60, alpha=.9, color="#34d399", label="4-step (fast / back-off / creep)")
ax.set_xlabel("Zero-position error (mm)", color="#cbd5e1")
ax.set_ylabel("Count (1000 homing cycles)", color="#cbd5e1")
ax.set_title("Repeatability of the home position", color="white")
ax.tick_params(colors="#94a3b8")
for sp in ax.spines.values():
    sp.set_color("#334155")
ax.legend(facecolor="#1e293b", labelcolor="white", edgecolor="#334155")
fig.savefig("repeatability.svg", format="svg", bbox_inches="tight", facecolor=fig.get_facecolor())
