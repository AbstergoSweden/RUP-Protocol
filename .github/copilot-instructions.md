# Copilot instructions

## Build, test, lint, validate
- Setup:
  - Python: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - Node: `npm ci` (or `npm install`)
- Validation (protocol/schema):
  - Python: `python validators/validate_rup.py protocol rup-protocol.yaml`
  - Python (examples): `python validators/validate_rup.py all ./examples`
  - Node: `npm run validate:protocol` or `node validators/validate_rup.js protocol rup-protocol.yaml`
  - Node (examples): `npm run validate:examples`
  - Bash wrapper: `./tools/scripts/validate_rup.sh protocol rup-protocol.yaml`
- Tests:
  - Python: `pytest`
  - Node: `npm test`
  - Single pytest test: `pytest tests/test_validation.py::test_validate_protocol_execution`
  - Single jest test: `npm test -- validation.test.js -t "should validate the protocol file successfully"`
- Lint:
  - Python: `ruff check .`
  - Docs (Markdown/YAML): `./.venv/bin/python tools/lint_docs.py`
  - Node: `npm run lint`
- Makefile shortcuts: `make validate`, `make test`, `make lint` (expects `.venv` at `./.venv/bin/python`).

## High-level architecture
- **Schema-first**: `rup-schema.json` is the canonical source of truth; `rup-protocol.yaml` is validated against it.
- **Validators**: `validators/validate_rup.py` is the primary implementation; `validators/validate_rup.js` is the parallel Node.js validator; `tools/scripts/validate_rup.sh` wraps the Node validator.
- **Examples**: `examples/` contains schema-compliant outputs (discovery/plan/execution/verification) used by validation and parity tests.
- **Tests**: `tests/` includes pytest suites plus Jest tests to ensure parity and safety checks (e.g., YAML alias limits).

## Key conventions
- Keep **schema, protocol, validators, and examples in sync** when changing schema definitions or protocol structure.
- When updating `rup-protocol.yaml`, **bump versions and changelog** (`protocol_version`, `last_updated`, `metadata.changelog`).
- Validators share a **common CLI contract** (`protocol`, `output`, `all`) and output types (`discovery`, `plan`, `execution`, `verification`); keep both implementations aligned.
- Use **Conventional Commits** (`type(scope): subject`) for PRs and commit messages.
