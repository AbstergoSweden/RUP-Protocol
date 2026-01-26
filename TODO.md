# TODO (RUP Protocol Repo)

## Done (v3.0 migration)

- [x] Add canonical `rup-protocol.yaml` (v3.0.0) and pin legacy snapshots in `legacy/`
- [x] Update `rup-schema.json` for v3.0.0 (definitions/adversarial_defense/error_modes.strategy + optional agent `meta`)
- [x] Update validators (`validate_rup.py`, `validate_rup.js`, `validate_rup.sh`) for v3.0.0 + dynamic schema-version enforcement
- [x] Update docs + workflows + tests to reference `rup-protocol.yaml`
- [x] Keep tests green; avoid local sandbox failures for link checking
- [x] Rename project branding to "RUP Protocol" (docs + protocol banner + schema title)

## Next

- [ ] Evaluate whether to add a dedicated formatter for Markdown/YAML (optional)

## Done (repo refinements)

- [x] Remove experimental builder artifacts and keep `rup-protocol.yaml` canonical
- [x] Add a scheduled link-check workflow for environments with outbound network
- [x] Add lightweight linting for Python (ruff) and JavaScript (node --check)
- [x] Add Markdown/YAML linting and wire into CI
- [x] Add YAML alias/file-size hardening in validators + security tests
- [x] Add `legacy/README.md` documenting what is pinned and when it should be updated
- [x] Add a small `make validate` / `make test` convenience layer
