from pydantic import BaseModel, Field


class ResultArtifact(BaseModel):
    document_id: str
    artifact_id: str
    format: str
    path: str
    size_bytes: int = Field(ge=0)
    checksum: str | None = None


class ResultResponse(BaseModel):
    document_id: str
    status: str
    artifacts: list[ResultArtifact] = Field(default_factory=list)
