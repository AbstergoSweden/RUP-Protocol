# Validators

This directory hosts the canonical validator implementations and their utilities.

## Contents

- `validate_rup.py` — Primary Python validator (recommended for most validation workflows).
- `validate_rup.js` — Parallel Node.js validator for cross-language consistency checks.
- `validate_rup.sh` — Bash wrapper that delegates to the Node.js validator.

## Usage Examples

```bash
# Python
python validate_rup.py protocol rup-protocol.yaml

# Node.js
node validate_rup.js protocol rup-protocol.yaml

# Bash wrapper
./validate_rup.sh protocol rup-protocol.yaml
```
