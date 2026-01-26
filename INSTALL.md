# RUP Protocol v3.0 — Install & Validate

This folder contains:

* `rup-protocol.yaml` — the protocol definition
* `rup-schema.json` — JSON Schema to validate the protocol and agent outputs
* `validate_rup.py` — Python validator
* `validate_rup.js` — Node.js validator
* `validate_rup.sh` — Bash wrapper (uses Node + ajv)
* `examples/` — sample agent outputs

## Option A: Python validator (recommended)

### 1) Create a venv and install deps

```bash
cd ~/path/to/RUP-Protocol
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Validate the protocol

```bash
python validate_rup.py protocol rup-protocol.yaml
```

### 3) Validate examples

```bash
python validate_rup.py output examples/discovery_output.json discovery
python validate_rup.py output examples/plan_output.json plan
python validate_rup.py output examples/execution_output.json execution
python validate_rup.py output examples/verification_output.json verification
```

## Option B: Node validator

### 1) Install deps

```bash
cd ~/path/to/RUP-Protocol
npm install
```

### 2) Validate

```bash
node validate_rup.js protocol rup-protocol.yaml
node validate_rup.js all examples
```

## Option C: Bash wrapper

```bash
cd ~/path/to/RUP-Protocol
chmod +x validate_rup.sh
./validate_rup.sh protocol rup-protocol.yaml
./validate_rup.sh all examples
```

## Notes

* The protocol YAML is validated as YAML → object → JSON Schema. If you convert YAML to JSON manually, ensure YAML anchors and special types are preserved.
* The example output JSON files are *synthetic* and meant to validate schema shape, not to represent real execution.
