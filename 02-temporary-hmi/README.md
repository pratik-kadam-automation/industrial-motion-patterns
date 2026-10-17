# 02 - Temporary HMI in Node-RED

**Situation:** the machine's HMI is damaged mid-project. All manual controls are gone: Auto/Manual selection, individual outputs, reset. Mechanical trials cannot wait weeks for a replacement.

**Idea:** anything already on the panel that can talk to the PLC is a resource. A protocol gateway is not only for sending data to the cloud; it is a programmable bridge into the PLC. Put a small dashboard on a touchscreen laptop connected to the machine network and run the machine from that.

## What is in `flow.json`

A Node-RED dashboard with:
- **Manual mode** switch (Auto/Manual)
- **Four output switches**
- **Reset** button
- **Status read back from the PLC**: mode, four output LEDs, last action

It ships with a **simulated PLC** so it runs with no hardware. Swap that one function node for your real read/write nodes.

## Run it

1. Install Node-RED and the dashboard package: `npm install node-red-dashboard` in your Node-RED folder.
2. Import `flow.json` (menu, Import, paste) and deploy.
3. Open `http://localhost:1880/ui`.

Tested: the flow loads in Node-RED 3.x with node-red-dashboard 3.6.x, and the interlock logic was unit-tested (outputs ignored in AUTO, accepted in MANUAL, cleared on switching to AUTO or reset).

## Design rules worth copying

1. **Outputs only work in MANUAL.** The command builder rejects output commands in AUTO and says why.
2. **LEDs show the PLC's state, not the button's state.** The panel polls the PLC every second. If a command was ignored, the LED stays off even though the switch was flipped.
3. **Reset returns to a safe state:** outputs off, mode AUTO.
4. **Every action is echoed** in a "Last action" line, so the operator sees what the panel did.

## Connecting a real PLC

Replace the `Simulated PLC` node with your own write and read nodes. Keep the contract:

- Input: `{op:'writeCoil', addr, value}`, `{op:'reset'}`, or a `poll` message
- Output 1: mode text; outputs 2-5: output states (booleans)

Which node you use depends on the PLC protocol (Modbus TCP, a vendor protocol such as MC/SLMP, OPC UA, and so on). Address 0 = manual-mode bit, 1-4 = outputs. Map them to your real device addresses.

## Safety

This is a **temporary convenience panel**, not a safety function. The hardwired E-stop and any safety circuits must stay in place and independent of this dashboard. Do not rely on a laptop UI to stop a machine.
