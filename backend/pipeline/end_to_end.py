from dataclasses import dataclass
from pathlib import Path

from backend.core.config import Settings, settings
from backend.ocr.factory import create_ocr_adapter
from backend.pipeline.ocr_to_udr import OcrToUdrPipeline
from backend.preprocessing.image_processor import ImagePreprocessor
from backend.translation.factory import create_translation_adapter
from backend.translation.models import TranslationLanguage
from backend.translation.service import TranslationService
from backend.translation.document_service import DocumentTranslationService
from backend.translation.terminology import TerminologyRegistry
from backend.translation.review import TranslationReviewQueue
from backend.validation.unified import UnifiedValidationService
from backend.reconstruction.service import ReconstructionService


@dataclass
class EndToEndResult:
    document: object
    validation: object
    review_queue: TranslationReviewQueue
    output_path: str | None
    model_configuration: dict


class ScientificDocumentPipeline:
    """P1 real-model orchestration from page images through reconstructed PDF."""

    def __init__(self, config: Settings = settings, review_queue=None):
        self.config = config
        self.review_queue = review_queue or TranslationReviewQueue()

    def run(
        self,
        image_paths: list[str | Path],
        *,
        document_type: str = "question_paper",
        source_language: str = "en",
        target_language: str = "hi",
        mime_type: str = "image/png",
        domain: str = "general",
        output_path: str | Path | None = None,
    ) -> EndToEndResult:
        ocr = create_ocr_adapter(self.config)
        ingestion = OcrToUdrPipeline(ocr_adapter=ocr, preprocessor=ImagePreprocessor())
        document = ingestion.process_pages(
            image_paths=image_paths,
            document_type=document_type,
            source_language=source_language,
            mime_type=mime_type,
            domain=domain,
        )

        terminology = TerminologyRegistry()
        translator = TranslationService(
            create_translation_adapter(self.config),
            terminology=terminology,
        )
        translated = DocumentTranslationService(
            translator, review_queue=self.review_queue
        ).translate_document(document, TranslationLanguage(target_language))

        validation = UnifiedValidationService().validate(translated)
        rendered = None
        if output_path and validation.export_allowed:
            rendered = ReconstructionService().render_pdf(translated, output_path)

        return EndToEndResult(
            document=translated,
            validation=validation,
            review_queue=self.review_queue,
            output_path=str(rendered) if rendered else None,
            model_configuration={
                "ocr_provider": self.config.ocr_provider,
                "translation_provider": self.config.translation_provider,
                "translation_model": self.config.translation_model,
                "equation_provider": self.config.equation_provider,
                "diagram_provider": self.config.diagram_provider,
            },
        )
