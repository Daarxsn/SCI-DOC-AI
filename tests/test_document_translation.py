from uuid import uuid4
from backend.schemas.udr import DocumentSource, ElementType, UdrDocument, UdrElement, UdrPage
from backend.translation.document_service import DocumentTranslationService
from backend.translation.models import TranslationLanguage
from backend.translation.rule_based_adapter import RuleBasedAdapter
from backend.translation.service import TranslationService
from backend.translation.terminology import TerminologyEntry, TerminologyRegistry

def test_document_translation_preserves_scientific_elements():
    document = UdrDocument(document_id=uuid4(), document_type="question_paper", source=DocumentSource(language="en", mime_type="application/pdf"), domain="biology", pages=[UdrPage(page_number=1, width=800, height=1000, elements=[
        UdrElement(id="q1", type=ElementType.QUESTION, source_text="The cell is visible."),
        UdrElement(id="eq1", type=ElementType.EQUATION, source_text="x = 2"),
        UdrElement(id="d1", type=ElementType.DIAGRAM, metadata={"labels": [{"text": "cell"}]}),
    ])])
    terminology = TerminologyRegistry()
    terminology.add(TerminologyEntry(source_term="cell", target_term="कोशिका", source_language="en", target_language="hi", domain="biology"))
    service = DocumentTranslationService(TranslationService(RuleBasedAdapter(), terminology=terminology))
    result = service.translate_document(document, TranslationLanguage.HINDI)
    assert "कोशिका" in result.pages[0].elements[0].target_text
    assert result.pages[0].elements[1].target_text == "x = 2"
    assert result.pages[0].elements[2].metadata["labels"][0]["text"] == "कोशिका"
