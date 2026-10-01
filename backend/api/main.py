from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.core.config import settings
from backend.services.document_service import DocumentService


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Multimodal scientific document intelligence platform.",
)

document_service = DocumentService()


class AnalyzeRequest(BaseModel):
    document_type: str = "question_paper"
    source_language: str = "en"
    mime_type: str
    domain: str = "general"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/v1/documents/analyze")
def analyze_document(request: AnalyzeRequest) -> dict:
    try:
        udr = document_service.create_initial_udr(
            document_type=request.document_type,
            source_language=request.source_language,
            mime_type=request.mime_type,
            domain=request.domain,
        )
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc

    return {
        "status": "accepted",
        "stage": "m0_udr",
        "udr": udr.model_dump(mode="json"),
    }
