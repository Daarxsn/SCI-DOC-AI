from uuid import uuid4

from backend.pilot.models import PilotRun, PilotStage
from backend.pilot.providers import (
    ExportProvider,
    ModelRegistry,
    TranslationProvider,
)


class PilotService:
    def __init__(self, translation: TranslationProvider, validator, exporter: ExportProvider, models: ModelRegistry):
        self.translation = translation
        self.validator = validator
        self.exporter = exporter
        self.models = models
        self.runs = {}

    def start(self, tenant_id, document, target_language, domain):
        run = PilotRun(
            run_id=str(uuid4()),
            tenant_id=tenant_id,
            document_id=str(document.document_id),
            target_language=target_language,
            domain=domain,
            metadata={"model_versions": self.models.versions()},
        )
        self.runs[run.run_id] = run

        try:
            run.stage = PilotStage.TRANSLATION
            run.progress = 35
            translated = self.translation.translate(document, target_language)

            run.stage = PilotStage.VALIDATION
            run.progress = 60
            report = self.validator.validate(translated)
            run.review_required = report.requires_review
            run.export_allowed = report.export_allowed

            if report.requires_review:
                run.stage = PilotStage.REVIEW
                run.progress = 70
                return run, translated, report

            run.stage = PilotStage.RECONSTRUCTION
            run.progress = 85

            if not report.export_allowed:
                run.stage = PilotStage.FAILED
                run.error = "Validation blocked export"
                return run, translated, report

            artifacts = self.exporter.export(translated)
            run.artifact_ids = [x["artifact_id"] for x in artifacts]
            run.stage = PilotStage.COMPLETED
            run.progress = 100
            return run, translated, report

        except Exception as exc:
            run.stage = PilotStage.FAILED
            run.error = str(exc)
            return run, document, None

    def get(self, run_id, tenant_id):
        run = self.runs.get(run_id)
        if not run or run.tenant_id != tenant_id:
            return None
        return run
