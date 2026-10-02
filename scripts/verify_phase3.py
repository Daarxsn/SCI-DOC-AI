"""Phase 3 lightweight verification.

Validates the real-document orchestration without requiring heavyweight ML models.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# When executed from the scripts directory, make the repository root
# explicit so backend.* imports are reliable.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== SCI-DOC AI | PHASE 3 VERIFICATION ===", flush=True)

    print("[1/3] Checking E2E pipeline module...", flush=True)
    from backend.pipeline.end_to_end import ScientificDocumentPipeline

    assert hasattr(ScientificDocumentPipeline, "run")
    assert hasattr(ScientificDocumentPipeline, "_mime_type")
    print("      PASS — document-input pipeline available", flush=True)

    print("[2/3] Checking supported document types...", flush=True)
    assert ScientificDocumentPipeline._mime_type(Path("a.pdf")) == "application/pdf"
    assert ScientificDocumentPipeline._mime_type(Path("a.png")) == "image/png"
    assert ScientificDocumentPipeline._mime_type(Path("a.jpg")) == "image/jpeg"
    print("      PASS — PDF/JPG/PNG supported", flush=True)

    print("[3/3] Running P3 orchestration tests...", flush=True)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_p3_pipeline.py",
            "tests/test_p1_end_to_end.py",
            "-q",
        ],
        cwd=ROOT,
    )
    if result.returncode:
        print("      FAIL — P3 tests failed", flush=True)
        return result.returncode

    print("      PASS — E2E orchestration tests", flush=True)
    print()
    print("PHASE 3 VERIFICATION: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
