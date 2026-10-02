from enum import Enum
from pydantic import BaseModel, Field, field_validator

SUPPORTED_LANGUAGES = {"en", "hi", "mr"}
SUPPORTED_DOMAINS = {"mathematics", "physics", "biology", "general"}

class EvaluationTask(str, Enum):
    OCR="ocr"; LAYOUT="layout"; TRANSLATION="translation"; MATHEMATICS="mathematics"; DIAGRAM="diagram"; RECONSTRUCTION="reconstruction"; END_TO_END="end_to_end"
class DatasetSplit(str, Enum):
    TRAIN="train"; VALIDATION="validation"; TEST="test"
class AnnotationType(str, Enum):
    DOCUMENT="document"; TEXT="text"; EQUATION="equation"; DIAGRAM="diagram"; TABLE="table"; LAYOUT="layout"

class MetricResult(BaseModel):
    name:str; value:float=Field(ge=0,le=1); threshold:float=Field(ge=0,le=1); passed:bool; sample_count:int=Field(ge=0); details:dict=Field(default_factory=dict)

class Annotation(BaseModel):
    annotation_id:str; annotation_type:AnnotationType; page_number:int=Field(ge=1); element_id:str|None=None; source_text:str|None=None; target_text:str|None=None; bbox:dict[str,float]|None=None; structured:dict=Field(default_factory=dict)

class BenchmarkCase(BaseModel):
    case_id:str; domain:str; source_language:str; target_language:str|None=None; split:DatasetSplit=DatasetSplit.TEST; input_path:str; reference_path:str|None=None; annotation_path:str|None=None; checksum_sha256:str|None=None; metadata:dict=Field(default_factory=dict)
    @field_validator("source_language")
    @classmethod
    def source_lang(cls,v):
        if v not in SUPPORTED_LANGUAGES: raise ValueError(f"Unsupported source language: {v}")
        return v
    @field_validator("target_language")
    @classmethod
    def target_lang(cls,v):
        if v is not None and v not in SUPPORTED_LANGUAGES: raise ValueError(f"Unsupported target language: {v}")
        return v
    @field_validator("domain")
    @classmethod
    def domain(cls,v):
        if v not in SUPPORTED_DOMAINS: raise ValueError(f"Unsupported domain: {v}")
        return v

class DatasetManifest(BaseModel):
    dataset_id:str; version:str; description:str; cases:list[BenchmarkCase]=Field(default_factory=list); annotation_schema_version:str="1.0"; metadata:dict=Field(default_factory=dict)

class BenchmarkReport(BaseModel):
    benchmark_id:str; task:EvaluationTask; metrics:list[MetricResult]=Field(default_factory=list); overall_score:float=Field(ge=0,le=1); passed:bool; metadata:dict=Field(default_factory=dict)
