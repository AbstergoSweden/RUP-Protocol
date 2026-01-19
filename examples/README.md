# RUP Protocol Examples

This folder contains example **agent output artifacts** that conform to the `rup-schema.json` definitions.

## Files

* `discovery_output.json`
    * Intended to match `#/$defs/DiscoveryReport`
    * Summarizes repo metadata, detected tooling, gaps, and risk scores

* `plan_output.json`
    * Intended to match `#/$defs/PlanOutput`
    * Contains a prioritized backlog and selected items for the run

* `execution_output.json`
    * Intended to match `#/$defs/ExecutionOutput`
    * Contains file changes, proposed commits, and local verification outcomes

* `verification_output.json`
    * Intended to match `#/$defs/VerificationOutput`
    * Contains verification results, metrics deltas, audit trail, and PR recommendations

## Validate examples

### Python

```bash
cd /Users/super_user/Desktop/RUP-Protocol-v2.1
python validate_rup.py output examples/discovery_output.json discovery
python validate_rup.py output examples/plan_output.json plan
python validate_rup.py output examples/execution_output.json execution
python validate_rup.py output examples/verification_output.json verification
```

### Node

```bash
cd /Users/super_user/Desktop/RUP-Protocol-v2.1
node validate_rup.js all examples
```
