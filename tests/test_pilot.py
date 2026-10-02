from uuid import uuid4

from backend.pilot.providers import ManifestExportProvider, PassthroughTranslationProvider, StaticModelRegistry
from backend.pilot.service import PilotService
from backend.schemas.udr import DocumentSource, UdrDocument
from backend.validation.unified import UnifiedValidationService


def make_document():
    return UdrDocument(
        document_id=uuid4(),
        document_type="question_paper",
        source=DocumentSource(language="en", mime_type="application/pdf"),
        domain="physics",
        pages=[],
    )


def test_pilot_run_tracks_models_and_stages():
    service = PilotService(
        PassthroughTranslationProvider(),
        UnifiedValidationService(),
        ManifestExportProvider(),
        StaticModelRegistry({"ocr":"1.0","translation":"1.0"}),
    )
    run, _, report = service.start("tenant-a", make_document(), "hi", "physics")
    assert run.document_id
    assert run.metadata["model_versions"]["ocr"] == "1.0"
    assert run.progress in {70, 100}


def test_pilot_is_tenant_scoped():
    service = PilotService(
        PassthroughTranslationProvider(),
        UnifiedValidationService(),
        ManifestExportProvider(),
        StaticModelRegistry({}),
    )
    run, _, _ = service.start("tenant-a", make_document(), "hi", "physics")
    assert service.get(run.run_id, "tenant-a") is not None
    assert service.get(run.run_id, "tenant-b") is None
