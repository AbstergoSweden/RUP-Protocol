# TODO (RUP Protocol Repo)

## Done (v3.0 migration)

- [x] Add canonical `rup-protocol.yaml` (v3.0.0) and pin legacy snapshots in `legacy/`
- [x] Update `rup-schema.json` for v3.0.0 (definitions/adversarial_defense/error_modes.strategy + optional agent `meta`)
- [x] Update validators (`validate_rup.py`, `validate_rup.js`, `validate_rup.sh`) for v3.0.0 + dynamic schema-version enforcement
- [x] Update docs + workflows + tests to reference `rup-protocol.yaml`
- [x] Keep tests green; avoid local sandbox failures for link checking
- [x] Rename project branding to "RUP Protocol" (docs + protocol banner + schema title)

## Next

- [ ] Builder polish: replace the placeholder `rup-protocol-src.yaml` stub with real modular includes (or remove `build_rup.py` if out of scope)
- [ ] Add `legacy/README.md` documenting what is pinned and when it should be updated
- [ ] Consider adding a small `make validate` / `make test` convenience layer (optional)

