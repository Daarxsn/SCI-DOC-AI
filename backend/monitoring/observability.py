import json
import time
from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True)
class TelemetryEvent:
    event_type: str
    service: str
    correlation_id: str
    tenant_id: str | None
    status: str
    duration_ms: float | None = None
    metadata: dict[str, Any] | None = None

def serialize_event(event: TelemetryEvent) -> str:
    payload = asdict(event)
    payload["metadata"] = payload["metadata"] or {}
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)

class Timer:
    def __init__(self) -> None:
        self._started = time.perf_counter()

    def elapsed_ms(self) -> float:
        return round((time.perf_counter() - self._started) * 1000, 3)
