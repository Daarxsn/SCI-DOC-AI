from enum import Enum

from pydantic import BaseModel, Field


class ImageMode(str, Enum):
    RGB = "RGB"
    GRAYSCALE = "L"


class PageArtifact(BaseModel):
    page_number: int = Field(ge=1)
    source_path: str
    processed_path: str
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    rotation_degrees: int = 0
    image_mode: ImageMode
    dpi: int = Field(gt=0)
    preprocessing_steps: list[str] = Field(default_factory=list)
