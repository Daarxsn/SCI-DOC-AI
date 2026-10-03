from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class AuditEvent:
    action: str
    tenant_id: str
    subject: str
    resource_type: str
    resource_id: str
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class InMemoryAuditLog:
    def __init__(self):
        self.events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event

    def for_tenant(self, tenant_id: str) -> list[AuditEvent]:
        return [event for event in self.events if event.tenant_id == tenant_id]
