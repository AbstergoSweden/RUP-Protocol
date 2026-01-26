# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 3.0.x   | ✅        |
| 2.1.x   | ⚠️        |
| 2.0.x   | ❌        |
| 1.0.x   | ❌        |

## Reporting a Vulnerability

**Do NOT report vulnerability via public GitHub issues.**

If you discover a security vulnerability in this project, please report it via email to: `2-craze-headmen@icloud.com`.

We will verify the vulnerability and direct you on the next steps.

## Policy

- We aim to acknowledge reports within 48 hours.
- We will provide a timeline for the fix.
- We follow a 90-day coordinated disclosure policy.

## Input Hardening

- YAML parsing uses a safe loader with alias limits to prevent “billion laughs” attacks.
- File size limits are enforced when loading YAML/JSON (`RUP_MAX_FILE_BYTES`, default 5MB).
- Alias limits are enforced during YAML parse (`RUP_MAX_YAML_ALIASES`, default 50).
- Validators do not execute code; they only parse YAML/JSON and validate against the schema.
