import re
from dataclasses import dataclass
from backend.schemas.udr import ElementType, UdrDocument

@dataclass(frozen=True)
class MathIssue:
    severity: str
    code: str
    element_id: str
    message: str

class MathematicalEquivalenceValidator:
    _space = re.compile(r"\s+")
    def normalize(self, expression: str) -> str:
        value = (expression or "").replace("{", "(").replace("}", ")")
        value = value.replace(r"\,", "").replace("×", "*").replace("÷", "/")
        return self._space.sub("", value).lower()
    def equivalent(self, source: str, target: str) -> bool:
        return bool(source and target) and self.normalize(source) == self.normalize(target)
    def validate(self, document: UdrDocument):
        issues = []
        for page in document.pages:
            for element in page.elements:
                if element.type != ElementType.EQUATION:
                    continue
                source = element.metadata.get("source_latex") or element.source_text or element.metadata.get("latex") or element.text
                target = element.metadata.get("target_latex") or element.target_text
                if target and not self.equivalent(str(source), str(target)):
                    issues.append(MathIssue("warning", "math_representation_changed", element.id, "Source and target equation representations are not textually equivalent after conservative normalization."))
        return issues
