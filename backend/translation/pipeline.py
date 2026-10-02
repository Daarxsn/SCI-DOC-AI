from dataclasses import dataclass
from backend.schemas.udr import UdrDocument
from backend.translation.document_service import DocumentTranslationService
from backend.translation.models import TranslationLanguage


@dataclass
class DocumentTranslationResult:
    document: UdrDocument
    review_required: bool
    review_count: int


class TranslationPipeline:
    def __init__(self, document_service: DocumentTranslationService, review_queue=None):
        self.document_service = document_service
        self.review_queue = review_queue or document_service.review_queue

    def translate(self, document: UdrDocument, target_language: TranslationLanguage) -> DocumentTranslationResult:
        translated = self.document_service.translate_document(document, target_language)
        pending = self.review_queue.pending() if self.review_queue is not None else []
        return DocumentTranslationResult(translated, bool(pending), len(pending))
