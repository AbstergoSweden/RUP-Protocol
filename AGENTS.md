# RUP Protocol v2.1 — Agent Development Guide

## Project Overview

**RUP (Repository Upgrade Protocol) v2.1.0** is a production-grade repository automation framework designed for AI agents. It provides a systematic 4-phase pipeline for upgrading repositories toward production readiness:

1. **Discovery** - Analyze repository structure, identify gaps and risks
2. **Planning** - Prioritize work items (P0-P3) and create execution plan
3. **Execution** - Implement fixes, add tests, update documentation
4. **Verification** - Validate changes, generate reports, prepare PRs

### Key Capabilities

- **14 Language Support**: Python, Node.js, Go, Rust, Java, Ruby, PHP, C#, Swift, Kotlin, Scala, Elixir, C/C++
- **Multi-Platform CI**: GitHub Actions, GitLab CI, CircleCI, Azure DevOps
- **Comprehensive Governance**: CODEOWNERS, branch protection, issue/PR templates, ADRs
- **Security-First**: SBOM generation, secret scanning, license compliance
- **Rollback-Safe**: All changes include verification and rollback procedures

## Technology Stack

### Core Technologies

- **Schema Definition**: JSON Schema Draft 2020-12 (`rup-schema.json`)
- **Protocol Definition**: YAML with anchors and special types (`rup-protocol-v2.1.yaml`)
- **Validation Framework**: Multi-language implementation (Python, Node.js, Bash)

### Python Environment

- **Dependencies**: `jsonschema>=4.21.0`, `PyYAML>=6.0.1`
- **Primary Validator**: `validate_rup.py` (recommended)
- **Python Version**: 3.11+ (from CI configuration)

### Node.js Environment

- **Dependencies**: `ajv@^8.17.1`, `ajv-formats@^3.0.1`, `js-yaml@^4.1.0`, `glob@^10.4.5`
- **Parallel Validator**: `validate_rup.js`
- **Package Manager**: npm

## Code Organization

### Root Directory Structure

```text
RUP-Protocol/
├── rup-protocol-v2.1.yaml    # Main protocol definition (AI agent reference)
├── rup-schema.json           # JSON Schema (single source of truth)
├── validate_rup.py           # Python validator (primary implementation)
├── validate_rup.js           # Node.js validator (parallel implementation)
├── validate_rup.sh           # Bash wrapper (delegates to Node.js)
├── package.json              # npm dependencies and scripts
├── requirements.txt          # Python dependencies
├── examples/                 # Sample agent output files
│   ├── discovery_output.json
│   ├── plan_output.json
│   ├── execution_output.json
│   └── verification_output.json
├── README.md                 # Human-readable overview
├── INSTALL.md               # Installation instructions
├── WARP.md                  # WARP.dev specific guidance
├── LICENSE                  # CC0-1.0 (Public Domain)
└── .gitignore
```

### Examples Directory

The `examples/` directory contains synthetic but schema-compliant sample outputs for each agent type:

- **discovery_output.json**: Repository analysis, tooling detection, risk assessment
- **plan_output.json**: Prioritized backlog, selected items, time estimates
- **execution_output.json**: File changes, commit proposals, verification results
- **verification_output.json**: Test results, metrics deltas, PR recommendations

⚠️ **Important**: These examples are for schema validation only and do not represent real execution results.

## Build & Test Commands

### Python Validator (Recommended)

```bash
# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Validate protocol definition
python validate_rup.py protocol rup-protocol-v2.1.yaml

# Validate specific agent output
python validate_rup.py output examples/discovery_output.json discovery
python validate_rup.py output examples/plan_output.json plan
python validate_rup.py output examples/execution_output.json execution
python validate_rup.py output examples/verification_output.json verification

# Validate all files in directory
python validate_rup.py all ./examples

# Verbose mode (show all errors)
python validate_rup.py protocol rup-protocol-v2.1.yaml --verbose
```

### Node.js Validator

```bash
# Install dependencies
npm install

# Validate protocol definition
npm run validate:protocol
node validate_rup.js protocol rup-protocol-v2.1.yaml

# Validate all examples
npm run validate:examples
node validate_rup.js all ./examples

# Generate sample output
npm run sample:discovery
```

### Bash Wrapper

```bash
# Make executable
chmod +x validate_rup.sh

# Validate protocol
./validate_rup.sh protocol rup-protocol-v2.1.yaml

# Validate directory
./validate_rup.sh all examples
```

## Architecture Details

### Schema-First Design Pattern

The project follows a **schema-first development** approach where `rup-schema.json` is the single source of truth:

1. **Schema Defines Structure**: All protocol definitions and agent outputs must conform to the JSON Schema
2. **Strict Validation**: `additionalProperties: false` ensures no extraneous fields
3. **Reference Resolution**: Uses `$ref` and `$defs` for modular schema composition
4. **Format Validation**: Enforces ISO 8601 dates, semantic versions, email formats

### Validator Implementation Pattern

Both Python and Node.js validators follow identical CLI interfaces:

```text
validate_rup.py|js [command] [file/directory] [type]

Commands:
  protocol <file>              - Validate protocol YAML against schema
  output <file> <type>         - Validate agent output JSON
  all <directory>              - Validate all files in directory
```

Types (for output command):
  discovery, plan, execution, verification

### Key Schema Definitions

Located in `rup-schema.json` under `$defs`:

- **DiscoveryReport**: Repository metadata, detected tooling, gap analysis, risk scores
- **PlanOutput**: Prioritized items (P0-P3), time allocation, selected work
- **ExecutionOutput**: File changes, commit messages, verification results
- **VerificationOutput**: Test metrics, security scan results, PR recommendations

**Priority Levels**:

- **P0**: Correctness + CI green + Security (60-70% time)
- **P1**: Documentation + Developer Experience (20-30% time)
- **P2**: Structural improvements + Advanced CI (5-10% time)
- **P3**: Polish + Performance + Advanced features (0-5% time)

## Code Style Guidelines

### Python (`validate_rup.py`)

- **Type Hints**: All functions use explicit type annotations (`Dict[str, Any]`, `List[Optional[...]]`)
- **Error Handling**: Try/except for import errors with helpful messages
- **CLI Design**: `argparse` with subcommands, colorized output
- **Path Handling**: `pathlib.Path` for cross-platform compatibility
- **Colors**: ANSI color class with terminal detection (`sys.stdout.isatty()`)

### Node.js (`validate_rup.js`)

- **CommonJS Modules**: `require()` syntax, no ES modules
- **Error Handling**: Try/catch for module imports, process.exit(1) on failure
- **CLI Design**: Manual argv parsing (no external CLI library)
- **Sync Operations**: Uses synchronous file operations for simplicity
- **Colors**: Similar ANSI color patterns as Python version

### JSON Schema (`rup-schema.json`)

- **Draft 2020-12**: Uses latest JSON Schema standard
- **Strict Validation**: `additionalProperties: false` on all objects
- **Semantic Versioning**: Pattern `^\d+\.\d+\.\d+$` for version strings
- **Required Fields**: Explicit `required` arrays for all objects
- **Description Fields**: Every property includes detailed descriptions

## Testing Strategy

### Schema Validation Testing

The primary testing mechanism is **self-validation**:

1. **Protocol Validation**: Ensure `rup-protocol-v2.1.yaml` conforms to schema
2. **Example Validation**: All example outputs validate against their respective `$defs`
3. **Cross-Validator Consistency**: Python and Node.js validators produce identical results

### Running Validation Tests

```bash
# Full validation suite (Python)
python validate_rup.py protocol rup-protocol-v2.1.yaml && \
python validate_rup.py output examples/discovery_output.json discovery && \
python validate_rup.py output examples/plan_output.json plan && \
python validate_rup.py output examples/execution_output.json execution && \
python validate_rup.py output examples/verification_output.json verification && \
echo "✅ All validation tests passed"

# Full validation suite (Node.js)
npm run validate:protocol && \
npm run validate:examples && \
echo "✅ All validation tests passed"
```

### Adding New Examples

When adding new schema `$defs`:

1. Create example JSON file in `examples/` directory
2. Update `INSTALL.md` with validation command
3. Add to test suite in both Python and Node.js
4. Ensure file matches schema exactly (use validator to verify)

## Deployment & CI/CD

### GitHub Actions Integration

```yaml
name: Validate RUP Protocol
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install jsonschema pyyaml
      - run: python validate_rup.py protocol rup-protocol-v2.1.yaml
```

### Validation in Production

**Exit Codes**:

- `0` - Validation successful
- `1` - Validation failed (invalid schema, file not found, etc.)

**Error Handling**:

- Fail-safe approach with detailed error messages
- Maximum 10 errors displayed by default (--verbose for all)
- Error stack traces include JSON path and validation context

## Security Considerations

### Safe by Design

- **No Code Execution**: Validators only parse YAML/JSON, no code execution
- **Schema Validation**: Prevents malicious data through strict schema enforcement
- **Path Safety**: Uses `pathlib` and path joining to prevent directory traversal
- **No Network Calls**: Validators work offline, no external dependencies

### Secrets Handling

- Never add secrets to example files
- Example outputs use synthetic data only
- Schema does not define secret fields

### Input Validation

- File existence checks before parsing
- UTF-8 encoding enforced
- JSON Schema Draft 2020-12 validator (battle-tested)

## Development Workflow

### Making Schema Changes

1. **Edit Schema**: Modify `rup-schema.json` (add new $defs, properties, etc.)
2. **Update Validators**: Ensure Python and Node.js validators handle changes
3. **Add Examples**: Create sample outputs for new schema definitions
4. **Test Validation**: Run full validation suite
5. **Update Documentation**: Reflect changes in AGENTS.md and README.md

### Protocol Updates

1. **Edit Protocol**: Modify `rup-protocol-v2.1.yaml`
2. **Bump Version**: Update `protocol_version` and `last_updated`
3. **Add Changelog**: Document changes in `metadata.changelog`
4. **Validate**: Ensure protocol conforms to schema
5. **Test Examples**: All examples must still validate

### Validator Modifications

**Python Validator**:

- Update `type_map` dictionary when adding new output types
- Modify error formatting functions for better context
- Enhance RefResolver configuration for complex schemas

**Node.js Validator**:

- Update `typeMap` object to match Python version
- Sync glob patterns with Python validator behavior
- Maintain identical exit codes and error messages

## Troubleshooting

### Common Validation Errors

**Schema Validation Failure**:

```text
❌ Validation failed: 2 errors
❌ phases[0].name: 'discover' is not one of ['discovery', 'planning', 'execution', 'verification']
❌ priorities.p0.description: 'Too short' is too short (minimum 20 characters)
```

**Fix**: Check enum values and string length constraints in schema

**Ref Resolution Error**:

```text
❌ Unresolvable JSON pointer: '$defs/NonExistentType'
```

**Fix**: Ensure $ref points to valid $def in schema

**YAML Parsing Error**:

```text
Error: Invalid YAML syntax: mapping values are not allowed here
```

**Fix**: Validate YAML syntax using online validator or Python yaml module

### Debug Mode

```bash
# Python verbose mode
python validate_rup.py protocol rup-protocol-v2.1.yaml --verbose

# Node debug output
node validate_rup.js protocol rup-protocol-v2.1.yaml 2>&1 | tee debug.log
```

## Additional Resources

- **README.md**: Human-readable overview and quick-start guide
- **INSTALL.md**: Detailed installation and validation instructions
- **WARP.md**: WARP.dev specific guidance and workflows
- **rup-protocol-v2.1.yaml**: Complete protocol reference (3000+ lines)
- **rup-schema.json**: JSON Schema reference (1800+ lines)

## License & Maintenance

**License**: CC0-1.0 (Public Domain) - See LICENSE file
**Maintainer**: Faye Ryan-Häkansdotter
**Version**: 2.1.0 (2026-01-18)

This is a reference implementation designed for AI agent consumption. Modifications should maintain backward compatibility and update all three validators synchronously.
