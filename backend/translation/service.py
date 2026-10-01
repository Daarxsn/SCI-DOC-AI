from uuid import uuid4

from backend.translation.adapter import TranslationAdapter
from backend.translation.models import (
    TranslationLanguage,
    TranslationStatus,
    TranslationUnit,
)
from backend.translation.policies import TranslationAction, TranslationPolicy
from backend.translation.terminology import TerminologyRegistry


class TranslationService:
    def __init__(
        self,
        adapter: TranslationAdapter,
        terminology: TerminologyRegistry | None = None,
        policy: TranslationPolicy | None = None,
    ) -> None:
        self.adapter = adapter
        self.terminology = terminology or TerminologyRegistry()
        self.policy = policy or TranslationPolicy()

    def translate(
        self,
        *,
        source_text: str,
        source_language: TranslationLanguage,
        target_language: TranslationLanguage,
        element_type,
        domain: str,
        context: str | None = None,
    ) -> TranslationUnit:
        unit = TranslationUnit(
            unit_id=f"tr-{uuid4().hex[:12]}",
            source_text=source_text,
            source_language=source_language,
            target_language=target_language,
        )

        action = self.policy.action_for(element_type)

        if action == TranslationAction.PRESERVE:
            unit.target_text = source_text
            unit.status = TranslationStatus.SKIPPED
            unit.confidence = 1.0
            return unit

        if action == TranslationAction.SPECIALIZED:
            unit.target_text = source_text
            unit.status = TranslationStatus.REVIEW
            unit.confidence = 0.0
            unit.metadata["reason"] = "specialized_scientific_element"
            return unit

        translated, confidence = self.adapter.translate(
            source_text,
            source_language=source_language,
            target_language=target_language,
            context=context,
        )

        translated, terminology_ids = self.terminology.apply(
            translated,
            language=target_language.value,
            domain=domain,
        )

        unit.target_text = translated
        unit.confidence = confidence
        unit.terminology_ids = terminology_ids
        unit.status = (
            TranslationStatus.REVIEW
            if confidence < 0.6
            else TranslationStatus.TRANSLATED
        )

        return unit
