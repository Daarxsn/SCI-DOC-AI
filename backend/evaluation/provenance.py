import hashlib
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BenchmarkProvenance:
    dataset_id: str
    dataset_version: str
    provider: str
    model_version: str | None
    configuration: dict[str, Any]
    case_ids: tuple[str, ...]

    def fingerprint(self) -> str:
        payload = {
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "provider": self.provider,
            "model_version": self.model_version,
            "configuration": self.configuration,
            "case_ids": list(self.case_ids),
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def build_provenance(
    *,
    dataset_id: str,
    dataset_version: str,
    provider: str,
    model_version: str | None,
    configuration: dict[str, Any] | None,
    case_ids: list[str],
) -> BenchmarkProvenance:
    return BenchmarkProvenance(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        provider=provider,
        model_version=model_version,
        configuration=configuration or {},
        case_ids=tuple(case_ids),
    )
