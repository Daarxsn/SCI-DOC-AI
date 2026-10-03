"""Phase 8 real-client-pilot verification."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== SCI-DOC AI | PHASE 8 VERIFICATION ===", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_pilot.py", "tests/test_pilot_acceptance.py", "-q"],
        cwd=ROOT,
    )
    if result.returncode:
        print("PHASE 8 VERIFICATION: FAIL", flush=True)
        return result.returncode
    print("PHASE 8 VERIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
