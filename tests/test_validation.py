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


def test_validate_all_fails_on_malformed_yaml(tmp_path):
    """Test that the 'all' command returns exit code 1 for malformed YAML."""
    # Create a malformed YAML file
    malformed_file = tmp_path / "bad_protocol.yaml"
    malformed_file.write_text("this: is: not: valid yaml\n  bad indent")
    
    result = subprocess.run(
        ["python", "validate_rup.py", "all", str(tmp_path)],
        capture_output=True,
        text=True,
        cwd=ROOT_DIR
    )
    # Exit code should be 1 because of parse error
    assert result.returncode == 1, f"Expected exit code 1 for malformed YAML, got {result.returncode}"


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

