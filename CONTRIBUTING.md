# Contributing to RUP Protocol

Thank you for your interest in contributing to RUP Protocol!

## Development Setup

1. Fork and clone the repository.
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:

   ```bash
   npm install
   ```

## Workflow

1. Create a branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes.
3. Run the validation scripts:

   ```bash
   # Validate the protocol definition
   python validate_rup.py protocol rup-protocol.yaml
   ```

4. Run tests:

   ```bash
   pytest
   npm test
   ```

5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):

   ```bash
   git commit -m "feat(scope): description"
   ```

## Pull Requests

- Ensure all tests and validations pass.
- Update the changelog if necessary.
- Link to any relevant issues.

## License

By contributing, you agree that your contributions will be licensed under the [CC0-1.0](./LICENSE).
