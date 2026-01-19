import subprocess
import pytest
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
PROTOCOL_FILE = ROOT_DIR / "rup-protocol-v2.1.yaml"
VALIDATOR_SCRIPT = ROOT_DIR / "validate_rup.py"

def test_protocol_file_exists():
    """Verify that the protocol YAML file exists."""
    assert PROTOCOL_FILE.exists(), f"Protocol file not found at {PROTOCOL_FILE}"

def test_validator_script_exists():
    """Verify that the validator script exists."""
    assert VALIDATOR_SCRIPT.exists(), f"Validator script not found at {VALIDATOR_SCRIPT}"

def test_validate_protocol_execution():
    """Run the validation script against the protocol file."""
    result = subprocess.run(
        ["python3", str(VALIDATOR_SCRIPT), "protocol", str(PROTOCOL_FILE)],
        capture_output=True,
        text=True
    )
    
    # Check for success exit code
    assert result.returncode == 0, f"Validation failed: {result.stderr}"
    
    # Check for success message
    assert "Valid" in result.stdout or "Valid" in result.stderr


def test_validate_examples_discovery():
    """Run the validation script against the discovery example."""
    example_file = ROOT_DIR / "examples" / "discovery_output.json"
    if not example_file.exists():
        pytest.skip("Discovery example not found")
        
    result = subprocess.run(
        ["python3", str(VALIDATOR_SCRIPT), "output", str(example_file), "discovery"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Discovery example validation failed: {result.stderr}"

