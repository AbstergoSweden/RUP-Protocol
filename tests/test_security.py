import os
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
VALIDATOR_SCRIPT = ROOT_DIR / "validate_rup.py"


def test_yaml_alias_limit_blocks_billion_laughs(tmp_path):
    # Create a YAML file with excessive aliases to trigger the limit.
    anchors = ["a0: &a0 lol"]
    for i in range(1, 20):
        anchors.append(f"a{i}: *a0")
    payload = "\n".join(anchors) + "\n"

    path = tmp_path / "alias_bomb.yaml"
    path.write_text(payload, encoding="utf-8")

    env = os.environ.copy()
    env["RUP_MAX_YAML_ALIASES"] = "5"

    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "protocol", str(path)],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT_DIR,
    )

    assert result.returncode == 1
    combined = result.stdout + result.stderr
    assert "YAML aliases exceed limit" in combined
