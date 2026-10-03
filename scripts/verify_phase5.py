"""Phase 5 human-review verification."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== SCI-DOC AI | PHASE 5 VERIFICATION ===", flush=True)
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_review.py",
            "tests/test_translation_review.py",
            "tests/test_review_workflow.py",
            "-q",
        ],
        cwd=ROOT,
    )
    if result.returncode:
        print("PHASE 5 VERIFICATION: FAIL", flush=True)
        return result.returncode
    print("PHASE 5 VERIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
