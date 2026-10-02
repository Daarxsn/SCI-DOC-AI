from dataclasses import dataclass

from backend.schemas.udr import ElementType, UdrDocument


@dataclass(frozen=True)
class ScientificIssue:
    severity: str
    code: str
    element_id: str | None
    message: str


class ScientificValidator:
    """Cross-domain validation rules for translated scientific documents."""

    def validate(self, document: UdrDocument) -> list[ScientificIssue]:
        issues: list[ScientificIssue] = []
        issues.extend(self._validate_languages(document))
        issues.extend(self._validate_questions(document))
        issues.extend(self._validate_equations(document))
        issues.extend(self._validate_diagrams(document))
        issues.extend(self._validate_translation(document))
        return issues

    def _validate_languages(self, document):
        issues = []
        if document.source.language not in {"en", "hi", "mr"}:
            issues.append(ScientificIssue("error", "unsupported_source_language", None, "Document source language is outside the supported language set."))
        return issues

    def _validate_questions(self, document):
        issues = []
        seen: set[str] = set()

        for page in document.pages:
            for element in page.elements:
                if element.type not in {ElementType.QUESTION, ElementType.SUBQUESTION}:
                    continue

                number = element.metadata.get("question_number")
                if number is not None:
                    key = str(number)
                    if key in seen:
                        issues.append(ScientificIssue("critical", "duplicate_question_number", element.id, f"Question number {key} occurs more than once."))
                    seen.add(key)

                if not element.source_text:
                    issues.append(ScientificIssue("error", "missing_question_source", element.id, "Question has no source text."))

        return issues

    def _validate_equations(self, document):
        issues = []

        for page in document.pages:
            for element in page.elements:
                if element.type != ElementType.EQUATION:
                    continue

                latex = element.metadata.get("latex")
                mathml = element.metadata.get("mathml")
                raw = element.source_text or element.text

                if not latex and not mathml and not raw:
                    issues.append(ScientificIssue("critical", "equation_content_missing", element.id, "Equation has no source representation."))
                    continue

                if latex:
                    if latex.count("{") != latex.count("}"):
                        issues.append(ScientificIssue("critical", "unbalanced_latex", element.id, "Equation LaTeX has unbalanced braces."))
                    if latex.count("(") != latex.count(")"):
                        issues.append(ScientificIssue("error", "unbalanced_equation", element.id, "Equation has unbalanced parentheses."))

        return issues

    def _validate_diagrams(self, document):
        issues = []

        for page in document.pages:
            for element in page.elements:
                if element.type not in {ElementType.DIAGRAM, ElementType.GRAPH}:
                    continue

                labels = element.metadata.get("labels", [])
                objects = element.metadata.get("objects", [])

                if not labels and not objects:
                    issues.append(ScientificIssue("warning", "empty_diagram_structure", element.id, "Diagram contains no structured labels or objects."))

                for label in labels:
                    if not label.get("text"):
                        issues.append(ScientificIssue("warning", "empty_diagram_label", element.id, "Diagram contains a label without text."))

        return issues

    def _validate_translation(self, document):
        issues = []

        for page in document.pages:
            for element in page.elements:
                status = element.metadata.get("translation_status")
                confidence = element.metadata.get("translation_confidence", element.confidence)

                if status == "review":
                    issues.append(ScientificIssue("warning", "translation_requires_review", element.id, "Translation was routed to human review."))

                if isinstance(confidence, (int, float)) and confidence < 0.5:
                    issues.append(ScientificIssue("warning", "very_low_translation_confidence", element.id, "Translation confidence is below 0.5."))

        return issues
