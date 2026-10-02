import hashlib
import hmac
import os

class ApiKeyAuthenticator:
    def __init__(self, expected_key=None):
        self.expected_key = expected_key or os.getenv("SCI_DOC_API_KEY")
    def authenticate(self, supplied_key):
        if not self.expected_key or not supplied_key:
            return False
        return hmac.compare_digest(
            hashlib.sha256(supplied_key.encode()).digest(),
            hashlib.sha256(self.expected_key.encode()).digest(),
        )

def require_api_key(supplied_key, authenticator=None):
    if not (authenticator or ApiKeyAuthenticator()).authenticate(supplied_key):
        raise PermissionError("Invalid or missing API key")
