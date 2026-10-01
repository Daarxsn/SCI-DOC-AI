from enum import Enum

from pydantic import BaseModel, Field


class MathRepresentation(str, Enum):
    LATEX = "latex"
    MATHML = "mathml"
    RAW = "raw"


class MathSymbol(BaseModel):
    symbol: str
    normalized: str | None = None
    confidence: float = Field(ge=0, le=1)


class Equation(BaseModel):
    equation_id: str
    raw_text: str
    latex: str | None = None
    mathml: str | None = None
    representation: MathRepresentation = MathRepresentation.RAW
    confidence: float = Field(ge=0, le=1)
    symbols: list[MathSymbol] = Field(default_factory=list)
    validation_errors: list[str] = Field(default_factory=list)
