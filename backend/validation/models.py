from enum import Enum

from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationIssue(BaseModel):
    code: str
    severity: ValidationSeverity
    message: str
    element_id: str | None = None
    details: dict[str, str] = {}


class ValidationReport(BaseModel):
    passed: bool
    issues: list[ValidationIssue] = []
    checked_elements: int = Field(ge=0)
    critical_issues: int = Field(ge=0)
    warning_count: int = Field(ge=0)
