from dataclasses import dataclass

@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    actor_id: str | None = None

class TenantGuard:
    def require(self, resource_tenant_id: str, context: TenantContext):
        if resource_tenant_id != context.tenant_id:
            raise PermissionError("Tenant boundary violation")
