from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class TranslationGovernanceRecord:
    action: str
    actor: str
    timestamp: str
    source_language: str
    target_language: str
    domain: str
    source_text: str
    target_text: str | None
    reason: str | None = None

class TranslationGovernanceLog:
    def __init__(self):
        self._records = []

    def record(self, action, actor, *, source_language, target_language, domain, source_text, target_text, reason=None):
        record = TranslationGovernanceRecord(
            action=action,
            actor=actor,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            source_text=source_text,
            target_text=target_text,
            reason=reason,
        )
        self._records.append(record)
        return record

    def records(self):
        return list(self._records)
