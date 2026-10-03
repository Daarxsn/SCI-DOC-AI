import hashlib
import json
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
DOMAINS = {"mathematics", "physics", "biology"}
TARGET_LANGUAGES = {"hi", "mr"}
RIGHTS_STATUSES = {"verified", "owned", "licensed", "public_domain", "permission_granted"}

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def validate_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    required = {"case_id", "source_path", "domain", "source_language", "target_language", "rights_status"}
    missing = sorted(required - set(case))
    if missing:
        raise ValueError(f"missing required fields: {missing}")
    source = root / case["source_path"]
    if not source.is_file():
        raise ValueError(f"source file does not exist: {case['source_path']}")
    if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"unsupported source format: {source.suffix}")
    if source.stat().st_size == 0:
        raise ValueError(f"source file is empty: {case['source_path']}")
    if case["domain"] not in DOMAINS:
        raise ValueError(f"unsupported domain: {case['domain']}")
    if case["source_language"] != "en":
        raise ValueError("Phase 27 requires English source documents")
    if case["target_language"] not in TARGET_LANGUAGES:
        raise ValueError(f"unsupported target language: {case['target_language']}")
    if case["rights_status"] not in RIGHTS_STATUSES:
        raise ValueError(f"unverified document rights status: {case['rights_status']}")
    return {
        "case_id": case["case_id"],
        "source_path": case["source_path"],
        "source_format": source.suffix.lower().lstrip("."),
        "domain": case["domain"],
        "source_language": case["source_language"],
        "target_language": case["target_language"],
        "rights_status": case["rights_status"],
        "source_size_bytes": source.stat().st_size,
        "source_sha256": sha256_file(source),
        "scientific_document_status": case.get("scientific_document_status", "UNVERIFIED"),
    }

def build_intake_manifest(metadata_path: str | Path, root: str | Path, output_path: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    cases = metadata.get("cases", [])
    if not 1 <= len(cases) <= 20:
        raise ValueError("Phase 27 accepts 1 to 20 intake cases")
    seen = set()
    normalized = []
    for case in cases:
        case_id = case.get("case_id")
        if case_id in seen:
            raise ValueError(f"duplicate case_id: {case_id}")
        seen.add(case_id)
        normalized.append(validate_case(case, root_path))
    domains = sorted({case["domain"] for case in normalized})
    targets = sorted({case["target_language"] for case in normalized})
    manifest = {
        "schema_version": "1.0",
        "phase": 27,
        "dataset_id": metadata.get("dataset_id", "sci-doc-real-intake"),
        "version": metadata.get("version", "1.0.0"),
        "status": "INTAKE_VALIDATED",
        "scientific_accuracy_claim": False,
        "case_count": len(normalized),
        "domains": domains,
        "target_languages": targets,
        "cases": normalized,
    }
    Path(output_path).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest
