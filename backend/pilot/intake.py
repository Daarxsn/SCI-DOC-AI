import hashlib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PilotIntakeCase:
    case_id: str
    source_path: str
    source_language: str
    target_language: str
    domain: str
    expected_format: str = "pdf"
    metadata: dict = field(default_factory=dict)

    def source_exists(self) -> bool:
        return Path(self.source_path).exists()

    def source_sha256(self) -> str:
        digest = hashlib.sha256()
        with open(self.source_path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


class PilotIntakeValidator:
    SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

    def validate(self, case: PilotIntakeCase) -> list[str]:
        errors = []
        path = Path(case.source_path)
        if not path.exists():
            errors.append("source document does not exist")
        elif path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            errors.append(f"unsupported source extension: {path.suffix}")
        if case.source_language != "en":
            errors.append("pilot source language must be English")
        if case.target_language not in {"hi", "mr"}:
            errors.append("pilot target language must be Hindi or Marathi")
        if case.domain not in {"mathematics", "physics", "biology"}:
            errors.append("pilot domain must be mathematics, physics, or biology")
        return errors
