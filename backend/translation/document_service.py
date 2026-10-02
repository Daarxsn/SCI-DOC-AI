from backend.schemas.udr import ElementType, UdrDocument
from backend.translation.models import TranslationLanguage, TranslationStatus
from backend.translation.service import TranslationService
from backend.translation.udr_adapter import TranslationUdrAdapter

class DocumentTranslationService:
    TEXT_TYPES = {ElementType.HEADING, ElementType.PARAGRAPH, ElementType.QUESTION, ElementType.SUBQUESTION, ElementType.OPTION, ElementType.CAPTION, ElementType.HEADER, ElementType.FOOTER}

    def __init__(self, translator: TranslationService, adapter=None) -> None:
        self.translator = translator
        self.udr_adapter = adapter or TranslationUdrAdapter()

    def translate_document(self, document: UdrDocument, target_language: TranslationLanguage) -> UdrDocument:
        source_language = TranslationLanguage(document.source.language)
        translated = document.model_copy(deep=True)
        translated.source.language = target_language.value
        for page in translated.pages:
            for element in page.elements:
                if element.type in self.TEXT_TYPES and element.source_text:
                    unit = self.translator.translate(element.source_text, source_language, target_language, document.domain, element_type=element.type.value)
                    self.udr_adapter.apply(element, unit)
                elif element.type in {ElementType.EQUATION, ElementType.IMAGE, ElementType.GRAPH}:
                    element.target_text = element.source_text or element.text
                    element.metadata["translation_status"] = TranslationStatus.SKIPPED.value
                    element.metadata["translation_reason"] = "non_prose_element"
                elif element.type == ElementType.DIAGRAM:
                    self._translate_diagram_labels(element, source_language, target_language, document.domain)
        return translated

    def _translate_diagram_labels(self, element, source_language, target_language, domain):
        translated_labels = []
        for label in element.metadata.get("labels", []):
            source_text = label.get("text")
            if not source_text:
                translated_labels.append(label)
                continue
            unit = self.translator.translate(source_text, source_language, target_language, domain, element_type="diagram_label")
            updated = dict(label)
            updated.update({"source_text": source_text, "text": unit.target_text, "translation_status": unit.status.value, "translation_confidence": unit.confidence, "translation_id": unit.unit_id})
            translated_labels.append(updated)
        element.metadata["labels"] = translated_labels
        element.metadata["translation_status"] = "translated"
