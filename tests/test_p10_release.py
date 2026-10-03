import json
from pathlib import Path
from backend.core.version import __version__, RELEASE_CHANNEL, RELEASE_NAME
ROOT = Path(__file__).resolve().parents[1]

def test_release_version_is_1_0_0():
    assert __version__ == "1.0.0"
    assert RELEASE_NAME == "SCI-DOC AI v1.0.0"
    assert RELEASE_CHANNEL == "production-candidate"

def test_release_manifest_is_complete():
    manifest = json.loads((ROOT / "release-manifest.json").read_text())
    assert manifest["version"] == __version__
    assert manifest["api_version"] == "v1"
    assert set(manifest["target_languages"]) == {"hi", "mr"}
    assert set(manifest["domains"]) == {"mathematics", "physics", "biology"}
    assert all(manifest["verification"].values())
    assert manifest["limitations"]

def test_release_artifacts_exist():
    for path in ["Dockerfile", "docker-compose.yml", ".env.example", "docs/P9_PRODUCTION_HARDENING.md", "docs/P8_REAL_CLIENT_PILOT.md"]:
        assert (ROOT / path).exists(), path