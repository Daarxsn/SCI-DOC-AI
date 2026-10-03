import os

from backend.core.production import check_production_readiness
from backend.jobs.reliability import RetryPolicy
from backend.results.integrity import sha256_bytes, verify_artifact_checksum
from backend.results.models import ResultArtifact


def test_retry_policy_has_bounded_attempts():
    policy = RetryPolicy(max_attempts=3)
    assert policy.allows(0)
    assert policy.allows(2)
    assert not policy.allows(3)


def test_artifact_checksum_is_verified():
    payload = b"pdf-bytes"
    artifact = ResultArtifact(
        tenant_id="tenant-a",
        document_id="doc-1",
        artifact_id="a1",
        format="pdf",
        path="artifact.pdf",
        size_bytes=len(payload),
        checksum=sha256_bytes(payload),
    )
    assert verify_artifact_checksum(artifact, payload)
    assert not verify_artifact_checksum(artifact, b"tampered")


def test_production_readiness_requires_credentials(monkeypatch):
    monkeypatch.delenv("SCI_DOC_API_KEY", raising=False)
    monkeypatch.delenv("SCI_DOC_TENANT_ID", raising=False)
    monkeypatch.setenv("DEBUG", "false")
    readiness = check_production_readiness()
    assert readiness.ready is False
    assert readiness.checks["debug_disabled"] is True
