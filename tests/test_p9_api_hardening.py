from fastapi.testclient import TestClient

from backend.api import results
from backend.api.main import app
from backend.api.security import ApiKeyAuthenticator
from backend.results.models import ResultArtifact


def test_result_access_uses_authenticated_tenant(monkeypatch):
    results.artifact_store = results.InMemoryArtifactStore()
    results.artifact_store.put(
        ResultArtifact(
            tenant_id="tenant-a",
            document_id="doc-1",
            artifact_id="a1",
            format="pdf",
            path="artifact.pdf",
            size_bytes=1,
        )
    )
    results.artifact_store.put(
        ResultArtifact(
            tenant_id="tenant-b",
            document_id="doc-1",
            artifact_id="b1",
            format="pdf",
            path="artifact-b.pdf",
            size_bytes=1,
        )
    )
    monkeypatch.setattr(
        "backend.api.results.authenticate_api_key",
        lambda key: ApiKeyAuthenticator(
            expected_key="secret", tenant_id="tenant-a"
        ).authenticate(key),
    )
    response = TestClient(app).get(
        "/v1/documents/doc-1/results",
        headers={"X-API-Key": "secret"},
    )
    assert response.status_code == 200
    assert [item["artifact_id"] for item in response.json()["artifacts"]] == ["a1"]


def test_readiness_reports_missing_production_configuration(monkeypatch):
    monkeypatch.delenv("SCI_DOC_API_KEY", raising=False)
    monkeypatch.delenv("SCI_DOC_TENANT_ID", raising=False)
    monkeypatch.setenv("DEBUG", "false")
    response = TestClient(app).get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["debug_disabled"] is True
