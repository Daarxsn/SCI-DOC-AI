from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_staging_compose_defines_required_services():
    compose = (ROOT / "docker-compose.staging.yml").read_text(encoding="utf-8")
    for service in ("api:", "postgres:", "redis:", "minio:"):
        assert service in compose


def test_staging_compose_requires_auth_and_secret_inputs():
    compose = (ROOT / "docker-compose.staging.yml").read_text(encoding="utf-8")
    for marker in (
        "SCI_DOC_API_KEY:",
        "SCI_DOC_TENANT_ID:",
        "POSTGRES_PASSWORD:",
        "MINIO_ROOT_USER:",
        "MINIO_ROOT_PASSWORD:",
    ):
        assert marker in compose


def test_staging_has_dependency_health_gates():
    compose = (ROOT / "docker-compose.staging.yml").read_text(encoding="utf-8")
    assert "depends_on:" in compose
    assert compose.count("healthcheck:") >= 4


def test_staging_documentation_states_in_memory_boundary():
    docs = (ROOT / "docs/PHASE11_STAGING_DEPLOYMENT.md").read_text(encoding="utf-8")
    assert "in-memory adapters" in docs
    assert "Phase 12" in docs
