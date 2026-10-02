from dataclasses import dataclass, field

from backend.validation.scientific import ScientificIssue


@dataclass
class ScientificValidationReport:
    document_id: str
    issues: list[ScientificIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(issue.severity in {"critical", "error"} for issue in self.issues)

    @property
    def requires_review(self) -> bool:
        return any(issue.severity in {"critical", "error", "warning"} for issue in self.issues)

    @property
    def export_allowed(self) -> bool:
        return self.passed and not self.requires_review

    def by_severity(self, severity: str) -> list[ScientificIssue]:
        return [issue for issue in self.issues if issue.severity == severity]
