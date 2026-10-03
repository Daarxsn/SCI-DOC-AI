"""Phase 9 production-hardening verification."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== SCI-DOC AI | PHASE 9 VERIFICATION ===", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_p9_production.py", "-q"],
        cwd=ROOT,
    )
    if result.returncode:
        print("PHASE 9 VERIFICATION: FAIL", flush=True)
        return result.returncode
    print("PHASE 9 VERIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
