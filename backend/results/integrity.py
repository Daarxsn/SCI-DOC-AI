import hashlib
from backend.results.models import ResultArtifact


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_artifact_checksum(artifact: ResultArtifact, payload: bytes) -> bool:
    if not artifact.checksum:
        return False
    return artifact.checksum == sha256_bytes(payload)
