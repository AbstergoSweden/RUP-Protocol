# RUP Protocol

Current version: v3.0.0

> **Production-Grade Repository Automation Framework for AI Agents**

[![Schema Version](https://img.shields.io/badge/schema-v3.0.0-blue)](./rup-schema.json)
[![License](https://img.shields.io/badge/license-CC0--1.0-green)](./LICENSE)
[![Languages](https://img.shields.io/badge/languages-14-orange)](./rup-protocol.yaml)
[![CI](https://github.com/AbstergoSweden/RUP-Protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/AbstergoSweden/RUP-Protocol/actions/workflows/ci.yml)

## Overview

RUP Protocol is a comprehensive framework for AI agents to systematically upgrade repositories toward production readiness. It provides:

- **4-Phase Pipeline**: Discovery → Planning → Execution → Verification
- **4 Specialized Agents**: Each with explicit I/O contracts and tools
- **14 Language Support**: Python, Node, Go, Rust, Java, Ruby, PHP, C#, Swift, Kotlin, Scala, Elixir, C++
- **Multi-Platform CI**: GitHub Actions, GitLab CI, CircleCI, Azure DevOps
- **Comprehensive Governance**: CODEOWNERS, branch protection, issue/PR templates, ADRs

<img width="1024" height="1024" alt="ashley" src="https://github.com/user-attachments/assets/eba28e5c-7fe9-4b01-b75c-d90af88ec18d" />

## Quick Start

### 1. For AI Agents

```yaml
# Import the protocol
protocol: rup-v3.0.0

# Run minimum viable upgrade
phases:
  - discovery: 5 min
  - fix_one_bug: 15 min
  - update_readme: 10 min
  - add_ci: 10 min
  - verify: 5 min
  - report: 5 min

total_time: ~50 minutes
```

### 2. For Humans (as a Checklist)

1. **Discovery** - Analyze repo, identify gaps
2. **Planning** - Prioritize P0/P1/P2/P3 items
3. **Execution** - Implement fixes, add tests, update docs
4. **Verification** - Run tests, lint, security scans
5. **Report** - Document changes, provide rollback steps

### 3. Validate Your Protocol

```bash
# Install dependencies
pip install jsonschema pyyaml

# Validate protocol
python validators/validate_rup.py protocol rup-protocol.yaml

# Validate agent outputs
python validators/validate_rup.py output discovery.json discovery
python validators/validate_rup.py output plan.json plan

# Validate all files in a directory
python validators/validate_rup.py all ./examples
```

## File Structure

```
RUP-Protocol/
├── README.md                         # This file
├── AGENTS.md                         # Agent development guide
├── rup-protocol.yaml                 # Canonical protocol definition
├── rup-schema.json                   # JSON Schema (single source of truth)
├── security/
│   ├── SECURITY.md                   # Reporting and policy
│   └── reports/                      # Historical/archived security reports
├── governance/
│   ├── CONTRIBUTING.md               # Contribution guidelines
│   ├── CODEOWNERS                    # Ownership matrix
│   └── templates/                    # Issue/PR templates (bug/feature)
├── tools/                            # Maintenance utilities (e.g., lint_docs.py)
│   └── scripts/
│       └── validate_rup.sh           # Wrapper for Node validator script (calls validators/validate_rup.js)
├── validators/
│   ├── validate_rup.py               # Python validator (primary implementation)
│   ├── validate_rup.js               # Node.js validator (parallel implementation)
│   └── README.md                     # Validator usage summary
├── examples/                         # Sample agent output files
│   ├── discovery_output.json
│   ├── plan_output.json
│   ├── execution_output.json
│   ├── verification_output.json
│   ├── rup_mock_walkthrough.md
│   └── mock_scenario_summary.json
├── runs/                             # Self-targeted run outputs (validated JSON)
│   └── README.md
├── legacy/                           # Pinned legacy protocol snapshots
│   ├── rup-protocol-v3.0.yaml
│   └── rup-protocol-v2.1.yaml
├── TODO.md                           # Repository TODOs / roadmap
├── tests/                            # Node and Python test projects
├── package.json                      # npm dependencies and scripts
├── requirements.txt                  # Python dependencies
└── LICENSE                           # CC0-1.0 (Public Domain)
```

## Legacy Versions

- `legacy/rup-protocol-v3.0.yaml` (v3.0.0 snapshot)
- `legacy/rup-protocol-v2.1.yaml` (v2.1.0 snapshot)

## Protocol Highlights

### Priority Levels

| Priority | Description | Time Allocation |
| ---------- | ----------- | --------------- |
| **P0** | Correctness + CI green + Security | 60-70% |
| **P1** | Documentation + Developer Experience | 20-30% |
| **P2** | Structural improvements + Advanced CI | 5-10% |
| **P3** | Polish + Performance + Advanced features | 0-5% |

### Agent Architecture

```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  DISCOVERY  │ ──▶ │  PLANNING   │ ──▶ │  EXECUTION  │ ──▶ │ VERIFICATION │
│    Agent    │     │    Agent    │     │    Agent    │     │    Agent     │
└─────────────┘     └─────────────┘     └─────────────┘     └──────────────┘
      │                   │                   │                    │
      ▼                   ▼                   ▼                    ▼
discovery.json       plan.json         changes.patch        report.json
```

### Supported Languages

| Language | Package Manager | Test Framework | Linter |
| ---------- | --------------- | -------------- | ------ |
| Python | pip, poetry | pytest | ruff, black |
| Node.js | npm, yarn | jest, mocha | eslint, prettier |
| Go | go mod | go test | gofmt, golangci-lint |
| Rust | cargo | cargo test | clippy, rustfmt |
| Java | maven, gradle | junit | checkstyle |
| Ruby | bundler | rspec | rubocop |
| PHP | composer | phpunit | phpcs, phpstan |
| C# | nuget | xunit | dotnet format |
| Swift | SPM | XCTest | swiftlint |
| Kotlin | gradle | JUnit | ktlint |
| Scala | sbt | ScalaTest | scalafmt |
| Elixir | mix | ExUnit | credo |
| C/C++ | cmake | ctest | clang-tidy |

### Repo Size Scaling

| Size | Files | LOC | What to Include |
| ------ | ----- | --- | --------------- |
| Tiny | < 10 | < 1K | README, LICENSE, basic CI |
| Small | 10-100 | 1K-10K | + CONTRIBUTING, SECURITY, pre-commit |
| Medium | 100-1K | 10K-100K | + CODEOWNERS, templates, branch protection |
| Large | > 1K | > 100K | + ADRs, chaos engineering, full observability |

## Key Features

### ✅ Guardrails & Safety

- Never add secrets to code
- Never introduce breaking changes without documentation
- Maximum 20 files changed per run
- Always have rollback procedure

### ✅ Evaluation Metrics

- Test coverage: +5% minimum
- Lint violations: 0 new
- Security findings: 0 new critical/high
- Build time: <10% increase

### ✅ Commit Protocol

Follows [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <subject>

[body]

[footer]
```

Types: `fix`, `feat`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### ✅ Error Handling

- Fail safe, not fast
- Prefer partial success over total failure
- Generate manual verification scripts when tools unavailable
- Always document assumptions

## Validation

Note: `rup-protocol.yaml` includes embedded input/output schemas that are JSON-Schema-like (and may include OpenAPI-style `nullable`). The authoritative validator is `rup-schema.json`.

### Python

```python
from validate_rup import load_schema, validate_protocol, load_yaml

schema = load_schema()
protocol = load_yaml("rup-protocol.yaml")
valid, errors = validate_protocol(protocol, schema)

if valid:
    print("✅ Protocol is valid")
else:
    for error in errors:
        print(f"❌ {error.message}")
```

## Linting

### Python (ruff)

```bash
ruff check .
```

### Markdown / YAML

```bash
./.venv/bin/python tools/lint_docs.py
```

### JavaScript (syntax check)

```bash
npm run lint
```

## Security

- YAML alias expansion is capped to prevent “billion laughs” attacks.
- Input file size limits are enforced for YAML/JSON.
- Configure via env vars: `RUP_MAX_YAML_ALIASES` and `RUP_MAX_FILE_BYTES`.
- See `SECURITY.md` for reporting and policy.

## Continuous Integration

- GitHub Actions CI runs Python (pytest) and Node (jest) suites on pushes and pull requests.
- CodeQL scans run weekly and on PRs for JavaScript and Python.
- Supply chain workflows audit npm and pip dependencies weekly and on PRs.

### Node.js

```javascript
const Ajv = require('ajv');
const yaml = require('js-yaml');
const fs = require('fs');

const schema = JSON.parse(fs.readFileSync('rup-schema.json'));
const protocol = yaml.load(fs.readFileSync('rup-protocol.yaml'));

const ajv = new Ajv({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

if (validate(protocol)) {
    console.log('✅ Protocol is valid');
} else {
    validate.errors.forEach(e => console.log(`❌ ${e.message}`));
}
```

### Bash (wrapper)

```bash
./tools/scripts/validate_rup.sh protocol rup-protocol.yaml
```

## CI/CD Integration

### GitHub Actions

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
      - run: python validators/validate_rup.py protocol rup-protocol.yaml
```

## Changelog

### v3.0.0 (2026-01-22)

- Refactored protocol with YAML anchors for token efficiency
- Added adversarial defense guardrails against prompt injection
- Added recursive self-healing error loops in execution agent
- Added explicit dependency verification to reduce hallucinations
- Unified tool contract definitions

### v2.1.0 (2026-01-18)

- Added monorepo support
- Added containerization section
- Added 6 additional languages
- Added CODEOWNERS, issue/PR templates
- Added ADR support
- Added mutation testing guidance
- Added chaos engineering
- Added incident response playbooks
- Added technical debt tracking
- Added quick-start guide

### v2.0.0 (2026-01-18)

- Split into 4 specialized agents
- Added evaluation metrics
- Enhanced security with SBOM
- Added tool contracts with I/O schemas
- Introduced conventional commits
- Added rollback guidance

### v1.0.0 (2024-12-01)

- Initial release

## Dependency Updates

Python dependencies are pinned in `requirements.txt`. To update them:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -U jsonschema PyYAML pytest requests ruff
pip freeze | grep -E '^(jsonschema|PyYAML|pytest|requests|ruff)==' > requirements.txt
```

Node dependencies are locked via `package-lock.json` and updated with `npm install` + `npm audit`.

## Contributing

See [governance/CONTRIBUTING.md](governance/CONTRIBUTING.md) for guidelines.

## License

[CC0-1.0](LICENSE) - Public Domain

## Credits

Developed by **Faye Hakansdotter**

Built with ❤️ for AI-assisted development
