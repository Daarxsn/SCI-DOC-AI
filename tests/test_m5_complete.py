from uuid import uuid4
from backend.schemas.udr import BoundingBox, DocumentSource, ElementType, UdrDocument, UdrElement, UdrPage
from backend.validation.unified import UnifiedValidationService

def document():
    return UdrDocument(document_id=uuid4(),document_type="question_paper",source=DocumentSource(language="hi",mime_type="application/pdf"),domain="physics",pages=[UdrPage(page_number=1,width=500,height=700,elements=[
        UdrElement(id="eq",type=ElementType.EQUATION,bbox=BoundingBox(x=10,y=10,width=100,height=30),source_text="F = ma",target_text="F = ma",metadata={"source_latex":"F = ma","target_latex":"F = ma"}),
        UdrElement(id="q",type=ElementType.QUESTION,bbox=BoundingBox(x=10,y=60,width=200,height=40),source_text="What is force?",target_text="बल क्या है?",metadata={"translation_status":"translated","translation_confidence":0.95}),
        UdrElement(id="d",type=ElementType.DIAGRAM,bbox=BoundingBox(x=10,y=120,width=200,height=150),metadata={"objects":[{"id":"o1"}],"labels":[{"id":"l1","text":"बल"}],"relationships":[{"source":"o1","target":"l1"}]}),
    ])])

def test_complete_m5_pipeline_allows_clean_document():
    report=UnifiedValidationService().validate(document())
    assert report.checked_elements==3
    assert report.export_allowed

def test_m5_blocks_invalid_diagram_relationship():
    doc=document(); doc.pages[0].elements[2].metadata["relationships"]=[{"source":"missing","target":"l1"}]
    report=UnifiedValidationService().validate(doc)
    assert any(i.code=="missing_relationship_source" for i in report.issues)
    assert report.export_allowed is False

def test_m5_detects_equation_representation_change():
    doc=document(); doc.pages[0].elements[0].metadata["target_latex"]="F = mv"
    report=UnifiedValidationService().validate(doc)
    assert any(i.code=="math_representation_changed" for i in report.issues)
    assert report.export_allowed is False
