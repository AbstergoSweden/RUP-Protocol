# Contributing

Thanks for considering a contribution! This project follows the RUP protocol principles: correctness first, security always, and clear documentation.

## Getting Started
- Fork the repo and create a feature branch.
- Install dependencies:
  - Python: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - Node: `npm ci`
- Run tests before pushing: `pytest` and `npm test`.

## Pull Requests
- Use Conventional Commits in PR titles (`type(scope): subject`).
- Link related issues (e.g., `Closes #123`).
- Add tests for new behavior and update docs when needed.
- Ensure `npm test` and `pytest` pass.

## Code of Conduct
- Be respectful, inclusive, and constructive.
