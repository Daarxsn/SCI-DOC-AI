from dataclasses import dataclass

@dataclass(frozen=True)
class AuthPrincipal:
    tenant_id: str
    subject: str
    scopes: frozenset[str] = frozenset()

    def allows(self, scope: str) -> bool:
        return scope in self.scopes or "*" in self.scopes
