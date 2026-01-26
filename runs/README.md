# Self-Targeted Runs

This folder contains RUP Protocol outputs produced by running the protocol
against this repository.

## Latest

- `self-2026-01-26/` — discovery/plan/execution/verification outputs

## Validation

```bash
./.venv/bin/python validate_rup.py output runs/self-2026-01-26/discovery.json discovery
./.venv/bin/python validate_rup.py output runs/self-2026-01-26/plan.json plan
./.venv/bin/python validate_rup.py output runs/self-2026-01-26/execution.json execution
./.venv/bin/python validate_rup.py output runs/self-2026-01-26/verification.json verification
```

