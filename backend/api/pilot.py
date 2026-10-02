from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.api.security import require_api_key
from backend.pilot.models import PilotRun
from backend.pilot.service import PilotService
from backend.pilot.providers import (
    ManifestExportProvider,
    PassthroughTranslationProvider,
    StaticModelRegistry,
)
from backend.validation.unified import UnifiedValidationService

router = APIRouter(prefix="/v1/pilot", tags=["pilot"])

class PilotStartRequest(BaseModel):
    tenant_id: str
    document_id: str
    target_language: str
    domain: str

# The API contract is ready for wiring to the persisted UDR/document store.
# A real deployment should resolve document_id to the stored UDR before start.
model_registry = StaticModelRegistry({"ocr":"baseline","translation":"adapter","validation":"m5","reconstruction":"adapter"})
pilot_service = PilotService(PassthroughTranslationProvider(), UnifiedValidationService(), ManifestExportProvider(), model_registry)

@router.get("/{run_id}", response_model=PilotRun)
def get_run(run_id: str, tenant_id: str, x_api_key: str | None = Header(default=None)):
    try:
        require_api_key(x_api_key)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    run = pilot_service.get(run_id, tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Pilot run not found")
    return run
