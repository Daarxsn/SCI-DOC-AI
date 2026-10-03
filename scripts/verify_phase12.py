from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
required = [
    "backend/core/model_registry.py", "backend/core/ml_runtime.py", "backend/api/main.py",
    "Dockerfile.ml", "docker-compose.ml.yml", "requirements-p1.txt",
    "docs/PHASE12_ML_RUNTIME.md", "tests/test_p12_ml_runtime.py",
]
for relative in required:
    if not (ROOT / relative).is_file():
        raise SystemExit(f"missing Phase 12 file: {relative}")
registry = (ROOT / "backend/core/model_registry.py").read_text(encoding="utf-8")
for marker in ("configured_models", "runtime_status", "assert_runtime_dependencies"):
    if marker not in registry:
        raise SystemExit(f"missing model registry contract: {marker}")
compose = (ROOT / "docker-compose.ml.yml").read_text(encoding="utf-8")
for marker in ("api-ml:", "MODEL_CACHE_DIR", "model_cache"):
    if marker not in compose:
        raise SystemExit(f"missing ML compose marker: {marker}")
print("Phase 12 structural verification: PASS")
