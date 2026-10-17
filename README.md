# industrial-motion-patterns
![simulate-homing](https://github.com/pratik-kadam-automation/industrial-motion-patterns/actions/workflows/simulate.yml/badge.svg)
Small, hardware-free examples of motion-control and operator-panel patterns from real machine-building work. Each pattern comes with something you can **run** to see the effect, not just a write-up.

| Pattern | What it shows | Run it |
|---|---|---|
| [01-servo-homing](01-servo-homing/) | Why "just home the axis" takes 4 steps, with a simulator that measures the difference | `python simulate.py` |
| [02-temporary-hmi](02-temporary-hmi/) | A stand-in operator panel built in Node-RED when the real HMI is unavailable | Import `flow.json` into Node-RED |

## Principles

- **Vendor-neutral.** No PLC, drive or HMI brand is assumed. Map the examples onto your own hardware.
- **Honest numbers.** Simulation results come from an illustrative model, not from a specific machine. Change the constants and rerun.
- **The machine protects itself.** Limit and fault handling lives in PLC logic, not in a drive setting or a UI.

## Disclaimer

Educational examples. Not safety-rated and not a substitute for a proper safety function (hardwired E-stop, safety PLC, risk assessment). Test on your own equipment and use at your own risk.

## License

MIT, see [LICENSE](LICENSE).
