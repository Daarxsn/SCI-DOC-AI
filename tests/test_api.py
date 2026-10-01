from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_creates_initial_udr():
    response = client.post(
        "/api/v1/documents/analyze",
        json={
            "document_type": "question_paper",
            "source_language": "en",
            "mime_type": "application/pdf",
            "domain": "mathematics",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["stage"] == "m0_udr"
    assert body["udr"]["source"]["language"] == "en"
    assert body["udr"]["domain"] == "mathematics"


def test_analyze_rejects_unsupported_mime_type():
    response = client.post(
        "/api/v1/documents/analyze",
        json={
            "mime_type": "text/plain",
        },
    )

    assert response.status_code == 415
