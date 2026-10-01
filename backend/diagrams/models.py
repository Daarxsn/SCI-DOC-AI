from enum import Enum

from pydantic import BaseModel, Field


class DiagramDomain(str, Enum):
    GENERAL = "general"
    PHYSICS = "physics"
    BIOLOGY = "biology"


class DiagramLabel(BaseModel):
    label_id: str
    text: str
    confidence: float = Field(ge=0, le=1)
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)


class DiagramObject(BaseModel):
    object_id: str
    object_type: str
    confidence: float = Field(ge=0, le=1)
    attributes: dict[str, str] = Field(default_factory=dict)


class DiagramRelationship(BaseModel):
    source_id: str
    relation: str
    target_id: str
    confidence: float = Field(ge=0, le=1)


class Diagram(BaseModel):
    diagram_id: str
    domain: DiagramDomain
    confidence: float = Field(ge=0, le=1)
    labels: list[DiagramLabel] = Field(default_factory=list)
    objects: list[DiagramObject] = Field(default_factory=list)
    relationships: list[DiagramRelationship] = Field(default_factory=list)
    source_image_path: str | None = None
