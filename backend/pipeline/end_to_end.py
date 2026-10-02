from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from backend.core.config import Settings, settings
from backend.ocr.factory import create_ocr_adapter
from backend.pipeline.ocr_to_udr import OcrToUdrPipeline
from backend.pipeline.scientific_enrichment import ScientificEnrichment
from backend.preprocessing.service import PreprocessingService
from backend.translation.models import TranslationLanguage
from backend.translation.service import TranslationService
from backend.translation.document_service import DocumentTranslationService
from backend.translation.factory import create_translation_adapter
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
    stage_status: dict[str, str]


class ScientificDocumentPipeline:
    """Real document pipeline: source file -> pages -> OCR -> UDR -> AI -> validation -> PDF."""

    def __init__(self, config: Settings = settings, review_queue=None):
        self.config = config
        self.review_queue = review_queue or TranslationReviewQueue()

    def run(
        self,
        source_path: str | Path,
        *,
        document_type: str = "question_paper",
        source_language: str = "en",
        target_language: str = "hi",
        mime_type: str | None = None,
        domain: str = "general",
        output_path: str | Path | None = None,
    ) -> EndToEndResult:
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Input document does not exist: {source}")

        resolved_mime = mime_type or self._mime_type(source)
        stages = {
            "input": "passed",
            "preprocessing": "pending",
            "ocr": "pending",
            "udr": "pending",
            "scientific_enrichment": "pending",
            "translation": "pending",
            "validation": "pending",
            "reconstruction": "skipped",
        }

        with TemporaryDirectory(prefix="sci-doc-p3-") as work_dir:
            page_dir = Path(work_dir) / "pages"
            artifacts = PreprocessingService().process(
                source_path=source,
                mime_type=resolved_mime,
                output_dir=page_dir,
            )
            if not artifacts:
                raise ValueError("Preprocessing produced no pages")
            stages["preprocessing"] = "passed"

            image_paths = [Path(a.processed_path) for a in artifacts]
            document = OcrToUdrPipeline(
                ocr_adapter=create_ocr_adapter(self.config),
            ).process_pages(
                image_paths=image_paths,
                document_type=document_type,
                source_language=source_language,
                mime_type=resolved_mime,
                domain=domain,
            )
            stages["ocr"] = "passed"
            stages["udr"] = "passed"

            document = ScientificEnrichment(
                equation_provider=self.config.equation_provider,
                diagram_provider=self.config.diagram_provider,
                diagram_model=self.config.diagram_model,
                device=self.config.ml_device,
            ).apply(document, image_paths)
            stages["scientific_enrichment"] = "passed"

            translator = TranslationService(
                create_translation_adapter(self.config),
                terminology=TerminologyRegistry(),
            )
            translated = DocumentTranslationService(
                translator,
                review_queue=self.review_queue,
            ).translate_document(
                document, TranslationLanguage(target_language)
            )
            stages["translation"] = "passed"

            validation = UnifiedValidationService().validate(translated)
            stages["validation"] = "passed"

            rendered = None
            if output_path and validation.export_allowed:
                rendered = ReconstructionService().render_pdf(
                    translated, output_path
                )
                stages["reconstruction"] = "passed"

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
                "device": self.config.ml_device,
            },
            stage_status=stages,
        )

    @staticmethod
    def _mime_type(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return "application/pdf"
        if suffix in {".jpg", ".jpeg"}:
            return "image/jpeg"
        if suffix == ".png":
            return "image/png"
        raise ValueError(f"Unsupported input type: {suffix or 'unknown'}")
