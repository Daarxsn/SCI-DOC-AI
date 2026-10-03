from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field
class JobStatus(str,Enum):
    QUEUED="queued"; PROCESSING="processing"; REVIEW="review"; VALIDATING="validating"; COMPLETED="completed"; FAILED="failed"
class Job(BaseModel):
    job_id:str; tenant_id:str; document_id:str; status:JobStatus=JobStatus.QUEUED
    progress:int=Field(default=0,ge=0,le=100); stage:str="queued"; error:str|None=None
    created_at:str=Field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    updated_at:str=Field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    metadata:dict=Field(default_factory=dict)
class JobCreateRequest(BaseModel):
    document_id:str
    target_language:str
    domain:str
    idempotency_key:str|None=None
class JobStatusResponse(BaseModel):
    job_id:str; status:JobStatus; progress:int; stage:str; error:str|None=None
