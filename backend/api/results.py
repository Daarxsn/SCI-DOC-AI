from fastapi import APIRouter, Header, HTTPException
from backend.api.security import authenticate_api_key
from backend.results.models import ResultResponse
from backend.results.storage import InMemoryArtifactStore

router = APIRouter(prefix="/v1/documents", tags=["results"])
artifact_store = InMemoryArtifactStore()

@router.get("/{document_id}/results", response_model=ResultResponse)
def get_results(document_id: str, x_api_key: str | None = Header(default=None)):
    try:
        principal = authenticate_api_key(x_api_key)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    if not principal.allows("documents:read"):
        raise HTTPException(status_code=403, detail="Insufficient scope")
    return ResultResponse(
        document_id=document_id,
        status="available",
        artifacts=artifact_store.list(document_id, principal.tenant_id),
    )
