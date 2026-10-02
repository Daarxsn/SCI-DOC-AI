from backend.translation.memory import MemoryEntry, TranslationMemory
from backend.translation.service import TranslationService
from backend.translation.terminology import TerminologyEntry, TerminologyRegistry
from backend.translation.models import TranslationLanguage
from backend.translation.rule_based_adapter import RuleBasedTranslationAdapter


def test_translation_memory_is_domain_and_language_scoped():
    memory = TranslationMemory()
    entry = MemoryEntry(
        source_text="cell",
        target_text="कोशिका",
        source_language="en",
        target_language="hi",
        domain="biology",
    )
    memory.add(entry)

    assert memory.lookup("cell", "en", "hi", "biology").target_text == "कोशिका"
    assert memory.lookup("cell", "en", "mr", "biology") is None
    assert memory.lookup("cell", "en", "hi", "physics") is None


def test_terminology_is_reused_before_translation():
    registry = TerminologyRegistry()
    registry.add(TerminologyEntry(
        source_term="cell",
        target_term="कोशिका",
        source_language="en",
        target_language="hi",
        domain="biology",
    ))

    service = TranslationService(
        RuleBasedTranslationAdapter(),
        terminology=registry,
    )
    result = service.translate(
        "The cell is visible.",
        TranslationLanguage.EN,
        TranslationLanguage.HI,
        "biology",
    )

    assert "__SCI_TERM_" not in result.target_text
    assert "कोशिका" in result.target_text
