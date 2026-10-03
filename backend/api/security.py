import hashlib
import hmac
import os
from backend.security.principal import AuthPrincipal

class ApiKeyAuthenticator:
    def __init__(self, expected_key=None, tenant_id=None, subject="api-client", scopes=None):
        self.expected_key = expected_key or os.getenv("SCI_DOC_API_KEY")
        self.tenant_id = tenant_id or os.getenv("SCI_DOC_TENANT_ID")
        self.subject = subject
        self.scopes = frozenset(scopes or {"documents:read","documents:write","jobs:read","jobs:write"})

    def authenticate(self, supplied_key) -> AuthPrincipal | None:
        if not self.expected_key or not supplied_key or not self.tenant_id:
            return None
        if not hmac.compare_digest(hashlib.sha256(supplied_key.encode()).digest(), hashlib.sha256(self.expected_key.encode()).digest()):
            return None
        return AuthPrincipal(self.tenant_id, self.subject, self.scopes)

def authenticate_api_key(supplied_key, authenticator=None) -> AuthPrincipal:
    principal=(authenticator or ApiKeyAuthenticator()).authenticate(supplied_key)
    if principal is None:
        raise PermissionError("Invalid or missing API key")
    return principal

def require_api_key(supplied_key, authenticator=None):
    authenticate_api_key(supplied_key, authenticator)
