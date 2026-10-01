from pydantic import BaseModel, Field


class OcrWord(BaseModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)


class OcrBlock(BaseModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)
    words: list[OcrWord] = Field(default_factory=list)
    reading_order: int = Field(ge=0)


class OcrPageResult(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    blocks: list[OcrBlock] = Field(default_factory=list)
    engine: str
    engine_version: str | None = None
