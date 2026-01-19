# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

RUP-Protocol is a production-grade repository automation framework for AI agents. It defines a 4-phase pipeline (Discovery → Planning → Execution → Verification) with JSON Schema validation for protocol definitions and agent outputs across 14 supported languages.

The repo contains:
- **rup-protocol-v2.1.yaml**: Main protocol definition (production reference)
- **rup-schema.json**: JSON Schema (Draft 2020-12) for validating protocol and agent outputs
- **Validators**: Python, Node.js, and Bash implementations
- **Examples**: Sample agent output artifacts matching the schema

## Development Workflow

### Common Commands

**Python Validation** (recommended)
```bash
# Setup environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Validate protocol definition
python validate_rup.py protocol rup-protocol-v2.1.yaml

# Validate agent outputs (discovery|plan|execution|verification)
python validate_rup.py output examples/discovery_output.json discovery
python validate_rup.py output examples/plan_output.json plan
python validate_rup.py output examples/execution_output.json execution
python validate_rup.py output examples/verification_output.json verification

# Validate all files in directory
python validate_rup.py all ./examples
```

**Node.js Validation**
```bash
npm install
npm run validate:protocol
npm run validate:examples
```

**Bash Wrapper**
```bash
chmod +x validate_rup.sh
./validate_rup.sh protocol rup-protocol-v2.1.yaml
./validate_rup.sh all examples
```

## Code Architecture

### Validation System

The codebase implements a **multi-language schema validation framework**:

1. **Schema Definition** (`rup-schema.json`)
   - JSON Schema Draft 2020-12 format
   - Defines required sections: metadata, agent_architecture, priorities, guardrails, evaluation, phases
   - Contains $defs for output types: DiscoveryReport, PlanOutput, ExecutionOutput, VerificationOutput
   - Strict validation with `additionalProperties: false` to catch typos

2. **Python Validator** (`validate_rup.py`)
   - Entry point: CLI with argparse (protocol | output | all commands)
   - Uses jsonschema.Draft202012Validator + RefResolver for $ref handling
   - Loads YAML → converts to dict → validates against schema
   - Colorized terminal output with error context (path, validator, expected value)
   - Limits error display to first 10 by default (--verbose for all)

3. **Node.js Validator** (`validate_rup.js`)
   - Parallel implementation using ajv + ajv-formats
   - Uses glob for directory scanning with pattern matching
   - Same CLI interface, similar error reporting
   - Supports streaming large YAML/JSON files

4. **Bash Wrapper** (`validate_rup.sh`)
   - Delegates to Node.js validator (requires npm dependencies)
   - Provides cross-platform compatibility layer

### Key Design Patterns

- **Schema-First Development**: Protocol and outputs validated against single source of truth
- **Modular Validators**: Separate CLIs for protocol vs. agent output validation
- **Type Mapping**: Output types map to schema $defs (discovery → DiscoveryReport, etc.)
- **Reference Resolution**: RefResolver handles nested $ref in schema definitions
- **CLI Uniformity**: Consistent argument parsing across all three validator implementations

### Data Flow

```
rup-protocol-v2.1.yaml → Load YAML → Validate against schema → Report errors with context
examples/*.json → Load JSON → Map type → Extract $def → Validate → Report with path
```

## Important Patterns & Rules

1. **Schema Integrity**
   - Never modify schema $defs structure without updating validators
   - Keep `additionalProperties: false` on all object definitions
   - Use semantic versioning for schema_version and protocol_version
   - All dates must be ISO 8601 format (validated by format: "date")

2. **YAML Protocol**
   - Supports YAML anchors and special types (preserve during YAML→JSON conversion)
   - Version strings must match pattern: `^\d+\.\d+\.\d+$`
   - Metadata.changelog requires at least one entry
   - Each phase should include name, description, and tools

3. **Validator Output**
   - Use standard exit codes: 0 (valid), 1 (invalid)
   - Always report absolute_path for nested validation errors
   - For errors >10, show summary line with count
   - Preserve original file paths in error messages

4. **Testing Validation**
   - Use `examples/` directory for sample outputs
   - Run `python validate_rup.py all examples` to validate all samples
   - Add new example outputs when adding schema $defs
   - Examples are synthetic but must conform strictly to schema

## File Structure Reference

```
RUP-Protocol/
├── rup-protocol-v2.1.yaml    # Protocol definition (read by agents, validated by schema)
├── rup-schema.json           # Single source of truth for validation
├── validate_rup.py           # Python validator (primary implementation)
├── validate_rup.js           # Node.js validator (parallel implementation)
├── validate_rup.sh           # Bash wrapper (uses Node.js)
├── package.json              # npm dependencies (ajv, js-yaml, glob)
├── requirements.txt          # Python dependencies (jsonschema, pyyaml)
├── examples/
│   ├── discovery_output.json      # Sample DiscoveryReport output
│   ├── plan_output.json           # Sample PlanOutput output
│   ├── execution_output.json      # Sample ExecutionOutput output
│   ├── verification_output.json   # Sample VerificationOutput output
│   └── README.md                  # Example artifact documentation
├── README.md                 # Project overview & quick start
├── INSTALL.md                # Installation & validation usage
└── LICENSE                   # CC0-1.0 (Public Domain)
```

## Schema $defs Reference

Key output types defined in schema (validators extract these):
- **DiscoveryReport**: Repo metadata, detected tooling, gaps, risk scores
- **PlanOutput**: Prioritized backlog (P0-P3), selected items for run
- **ExecutionOutput**: File changes, proposed commits, local verification results
- **VerificationOutput**: Verification results, metrics deltas, audit trail, PR recommendations

When adding new output types:
1. Add $def in rup-schema.json
2. Update type_map in validators (Python: line 114-118, Node: line 170-175)
3. Add example file in examples/ directory
4. Update INSTALL.md with validation command

## Dependencies

**Python** (requirements.txt):
- jsonschema >=4.21.0 — JSON Schema validation
- PyYAML >=6.0.1 — YAML parsing

**Node** (package.json):
- ajv ^8.17.1 — JSON Schema validator
- ajv-formats ^3.0.1 — Custom format validators (date, email, etc.)
- js-yaml ^4.1.0 — YAML parsing
- glob ^10.4.5 — File pattern matching

## License & Contribution

Licensed CC0-1.0 (Public Domain). No external contributors yet; designed as a reference protocol for AI agent implementations. Modifications should maintain schema compatibility and update all three validators synchronously.
