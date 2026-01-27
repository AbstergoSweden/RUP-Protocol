import subprocess
import pytest
import json
import shutil
import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
VALIDATE_PY = ROOT_DIR / "validators" / "validate_rup.py"
VALIDATE_JS = ROOT_DIR / "validators" / "validate_rup.js"
SCHEMA_PATH = ROOT_DIR / "rup-schema.json"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "parity"

# Check if node validator is available and functional
def _check_node_validator():
    """Check if Node.js validator is available and functional."""
    if not shutil.which("node"):
        return False
    try:
        # Try running the validator with --help or a simple test
        result = subprocess.run(
            ["node", str(VALIDATE_JS), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # If it returns without error or with recognizable output, it's working
        return result.returncode == 0 or "Usage" in result.stdout or "Usage" in result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

NODE_AVAILABLE = _check_node_validator()

def run_python_validator(command, file_path, output_type=None):
    cmd = [sys.executable, str(VALIDATE_PY), command, str(file_path)]
    if output_type:
        cmd.append(output_type)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def run_node_validator(command, file_path, output_type=None):
    cmd = ["node", str(VALIDATE_JS), command, str(file_path)]
    if output_type:
        cmd.append(output_type)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

@pytest.fixture
def valid_discovery_json(tmp_path):
    data = {
        "repo_metadata": {
            "name": "parity-test",
            "primary_language": "python",
            "repo_type": "library",
            "loc": 100,
            "file_count": 5
        },
        "languages": [{"name": "python", "percentage": 100, "lockfile_present": True}],
        "tooling": {},
        "gaps": [],
        "risk_assessment": {
            "overall_risk": "low",
            "technical_debt_score": 0,
            "production_readiness_score": 100
        }
    }
    path = tmp_path / "valid_discovery.json"
    with open(path, "w") as f:
        json.dump(data, f)
    return path

@pytest.fixture
def invalid_discovery_json(tmp_path):
    data = {
        "repo_metadata": {
            # Missing required fields
            "name": "parity-test"
        },
        # Wrong type
        "languages": "python", 
        "gaps": []
    }
    path = tmp_path / "invalid_discovery.json"
    with open(path, "w") as f:
        json.dump(data, f)
    return path

@pytest.mark.skipif(not NODE_AVAILABLE, reason="Node.js not available")
def test_parity_valid_discovery(valid_discovery_json):
    py_code, py_out, py_err = run_python_validator("output", valid_discovery_json, "discovery")
    node_code, node_out, node_err = run_node_validator("output", valid_discovery_json, "discovery")
    
    if py_code != 0 or node_code != 0:
        print(f"Python: code={py_code}, out={py_out}, err={py_err}")
        print(f"Node: code={node_code}, out={node_out}, err={node_err}")

    assert py_code == node_code == 0
    assert "Valid" in py_out
    assert "Valid" in node_out

@pytest.mark.skipif(not NODE_AVAILABLE, reason="Node.js not available")
def test_parity_invalid_discovery(invalid_discovery_json):
    py_code, py_out, _ = run_python_validator("output", invalid_discovery_json, "discovery")
    node_code, node_out, _ = run_node_validator("output", invalid_discovery_json, "discovery")
    
    assert py_code == 1
    assert node_code == 1
    assert "Invalid" in py_out
    assert "Invalid" in node_out

@pytest.mark.skipif(not NODE_AVAILABLE, reason="Node.js not available")
def test_parity_protocol_schema():
    # Use the actual protocol file
    protocol_path = ROOT_DIR / "rup-protocol.yaml"
    
    py_code, _, _ = run_python_validator("protocol", protocol_path)
    node_code, _, _ = run_node_validator("protocol", protocol_path)
    
    # Both should pass or both should fail (hopefully pass)
    assert py_code == node_code

@pytest.fixture
def edge_case_yaml(tmp_path):
    # YAML with anchors, aliases, timestamps, and large integers
    content = """
    repo_metadata:
        name: &repo_name "complex-repo"
        primary_language: "python"
        repo_type: "library"
        loc: 1000000000000000000
        file_count: 42
        last_commit_date: 2023-01-01T12:00:00Z
        license: null
    languages:
        - name: "python"
          percentage: 90.5
          lockfile_present: true
    tooling: {}
    gaps: []
    risk_assessment:
        overall_risk: "low"
        technical_debt_score: 10
        production_readiness_score: 90
    """
    path = tmp_path / "edge_case_discovery.yaml"
    with open(path, "w") as f:
        f.write(content)
    
    # Convert to JSON for the validator (validators accept JSON for output)
    # But wait, validate_rup.py loads JSON for 'output' command.
    # We should probably support YAML for output too?
    # The current validate_rup.py implementation uses load_json for output command.
    # Let's convert this YAML to JSON and see if python/node handle it differently.
    
    # Actually, let's test YAML protocol loading parity instead, as that's where YAML parsing matters.
    # We'll create a minimal valid protocol with anchors.
    
    protocol_content = """
    schema_version: "3.0.0"
    protocol_version: "3.0.0"
    metadata:
        name: &name "Parity Protocol"
        designation: *name
        tagline: "Testing anchors"
        changelog:
            - version: "1.0.0"
              date: "2023-01-01"
              changes: ["Initial"]
    agent_architecture:
        overview: "Simple"
        pipeline: "A -> B"
        agents:
            agent_discovery:
                id: "agent_discovery"
                responsibility: "Discover"
                scope: "Repo"
    priorities:
        P0:
            description: "Top"
    guardrails: {}
    evaluation: {}
    phases:
        - id: "phase_1_discovery"
          name: "Discovery"
    commit_protocol:
        standard: "CC"
        format: "fmt"
        types:
            - type: "feat"
              description: "Feature"
    """
    
    proto_path = tmp_path / "edge_case_protocol.yaml"
    with open(proto_path, "w") as f:
        f.write(protocol_content)
    return proto_path

@pytest.mark.skipif(not NODE_AVAILABLE, reason="Node.js not available")
def test_parity_yaml_anchors(edge_case_yaml):
    py_code, py_out, _ = run_python_validator("protocol", edge_case_yaml)
    node_code, node_out, _ = run_node_validator("protocol", edge_case_yaml)
    
    if py_code != 0 or node_code != 0:
        print(f"Python Out: {py_out}")
        print(f"Node Out: {node_out}")

    assert py_code == node_code == 0



@pytest.mark.skipif(not NODE_AVAILABLE, reason="Node.js not available")
def test_parity_schema_version_mismatch(tmp_path):
    protocol_content = """
    schema_version: "1.0.0"
    protocol_version: "3.0.0"
    metadata:
        name: "Old Protocol"
        changelog: []
    agent_architecture: {}
    priorities: {}
    guardrails: {}
    evaluation: {}
    phases: []
    """
    path = tmp_path / "bad_version_protocol.yaml"
    with open(path, "w") as f:
        f.write(protocol_content)
        
    py_code, py_out, _ = run_python_validator("protocol", path)
    node_code, node_out, _ = run_node_validator("protocol", path)
    
    assert py_code == 1
    assert node_code == 1
    assert "Schema version mismatch" in py_out
    assert "Schema version mismatch" in node_out
