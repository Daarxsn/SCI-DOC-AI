from backend.translation.models import TranslationUnit
from backend.schemas.udr import UdrElement


class TranslationUdrAdapter:
    def apply(self, element: UdrElement, unit: TranslationUnit) -> UdrElement:
        element.target_text = unit.target_text
        element.metadata.update(
            {
                "translation_id": unit.unit_id,
                "translation_status": unit.status.value,
                "translation_confidence": unit.confidence,
                "terminology_ids": unit.terminology_ids,
            }
        )

        if unit.confidence is not None:
            element.confidence = min(element.confidence or 0, unit.confidence)

        return element
