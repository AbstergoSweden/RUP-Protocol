# RUP Protocol

The **RUP Protocol** is a comprehensive framework designed for AI agents to systematically upgrade repositories toward production readiness. It defines a standardized 4-phase pipeline (Discovery, Planning, Execution, Verification) and provides schemas and validation tools to ensure consistency and quality.

## Key Files

*   `rup-protocol.yaml`: The master protocol definition file. Contains all rules, agent personas, and phase definitions.
*   `rup-schema.json`: The JSON Schema used to validate the protocol file and agent outputs.
*   `validate_rup.py`: Python script for validating the protocol and agent outputs against the schema.
*   `validate_rup.js`: Node.js script for validating the protocol and agent outputs.
*   `examples/`: Contains example outputs for discovery, planning, execution, and verification phases.

## Development & Usage

### Python Environment

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Validate Protocol:**
    ```bash
    python validate_rup.py protocol rup-protocol.yaml
    ```

3.  **Validate Agent Outputs:**
    ```bash
    python validate_rup.py output discovery.json discovery
    python validate_rup.py output plan.json plan
    ```

4.  **Run Tests:**
    ```bash
    pytest
    ```

### Node.js Environment

1.  **Install Dependencies:**
    ```bash
    npm install
    ```

2.  **Validate Protocol:**
    ```bash
    npm run validate:protocol
    # OR
    node validate_rup.js protocol rup-protocol.yaml
    ```

3.  **Run Tests:**
    ```bash
    npm test
    ```

## Agent Workflow

The protocol enforces a strict 4-phase pipeline. Agents should adhere to the specific inputs and outputs defined in `rup-protocol.yaml` for each phase:

1.  **Discovery Phase:** Analyze the repository to identify gaps (Output: `discovery.json`).
2.  **Planning Phase:** Prioritize tasks based on discovery findings (Output: `plan.json`).
3.  **Execution Phase:** Implement changes based on the plan (Output: `changes.patch` or direct file modifications).
4.  **Verification Phase:** Verify changes and generate a report (Output: `report.json`).

## Contribution Guidelines

*   **Commits:** Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat(core): add new validation rule`).
*   **License:** This project is licensed under CC0-1.0 (Public Domain).
