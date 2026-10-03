"""Phase 10 production-release verification."""
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
def main():
    print("=== SCI-DOC AI | PHASE 10 VERIFICATION ===", flush=True)
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_p10_release.py", "-q"], cwd=ROOT)
    if result.returncode:
        print("PHASE 10 VERIFICATION: FAIL", flush=True); return result.returncode
    manifest = json.loads((ROOT / "release-manifest.json").read_text())
    if manifest["version"] != "1.0.0":
        print("PHASE 10 VERIFICATION: FAIL — manifest version mismatch", flush=True); return 1
    print("PHASE 10 VERIFICATION: PASS", flush=True); return 0
if __name__ == "__main__": raise SystemExit(main())