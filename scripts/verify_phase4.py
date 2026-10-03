"""Lightweight Phase 4 reconstruction verification."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== SCI-DOC AI | PHASE 4 VERIFICATION ===", flush=True)
    import subprocess

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_reconstruction.py", "tests/test_background_reconstruction.py", "tests/test_scientific_reconstruction.py", "-q"],
        cwd=ROOT,
    )
    if result.returncode:
        print("PHASE 4 VERIFICATION: FAIL", flush=True)
        return result.returncode

    print("PHASE 4 VERIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
