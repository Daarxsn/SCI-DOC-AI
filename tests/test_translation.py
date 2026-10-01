from backend.schemas.udr import ElementType
from backend.translation.models import TranslationLanguage, TranslationStatus
from backend.translation.rule_based_adapter import RuleBasedAdapter
from backend.translation.service import TranslationService
from backend.translation.terminology import TerminologyEntry, TerminologyRegistry


def service() -> TranslationService:
    registry = TerminologyRegistry(
        [
            TerminologyEntry(
                term_id="term-cell",
                source_term="cell",
                target_term="कोशिका",
                language="hi",
                domain="biology",
            )
        ]
    )

    return TranslationService(RuleBasedAdapter(), registry)


def test_equation_is_not_sent_to_generic_translation():
    result = service().translate(
        source_text="F = ma",
        source_language=TranslationLanguage.ENGLISH,
        target_language=TranslationLanguage.HINDI,
        element_type=ElementType.EQUATION,
        domain="physics",
    )

    assert result.status == TranslationStatus.REVIEW
    assert result.target_text == "F = ma"


def test_terminology_registry_applies_controlled_term():
    result = service().translate(
        source_text="cell",
        source_language=TranslationLanguage.ENGLISH,
        target_language=TranslationLanguage.HINDI,
        element_type=ElementType.PARAGRAPH,
        domain="biology",
    )

    assert result.target_text == "कोशिका"
    assert "term-cell" in result.terminology_ids
