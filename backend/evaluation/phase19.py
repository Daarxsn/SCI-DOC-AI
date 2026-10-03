from pathlib import Path
import hashlib
import json
from backend.core.config import Settings
from backend.core.model_registry import assert_runtime_dependencies
from backend.evaluation.benchmark import BenchmarkRunner
from backend.evaluation.phase13 import load_manifest, validate_cases
from backend.pipeline.end_to_end import ScientificDocumentPipeline

def sha256_file(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def texts(document, field):
    return ' '.join(value for page in document.pages for element in page.elements if (value:=getattr(element,field,None)))

def execute_benchmark_result(manifest_path, root, output_dir, config: Settings):
    manifest=load_manifest(manifest_path)
    if len(manifest['cases']) != 1: raise RuntimeError('Phase 19 requires exactly one benchmark case')
    checks=validate_cases(manifest,root)
    if not checks[0]['ready']: raise RuntimeError('Phase 19 blocked: source asset/checksum is not ready')
    case=manifest['cases'][0]; root_path=Path(root)
    ref=root_path/case['reference_path']; ann=root_path/case['annotation_path']
    if not ref.is_file() or not ann.is_file(): raise RuntimeError('Phase 19 blocked: reference or annotation is missing')
    reference=json.loads(ref.read_text(encoding='utf-8'))
    if reference.get('metadata',{}).get('ground_truth_status')!='VERIFIED': raise RuntimeError('Phase 19 blocked: reference ground truth is not VERIFIED')
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True); output_pdf=out/(case['case_id']+'.pdf')
    assert_runtime_dependencies(config)
    result=ScientificDocumentPipeline(config=config).run(root_path/case['input_path'],source_language=case.get('source_language','en'),target_language=case.get('target_language','hi'),domain=case.get('domain','general'),document_type=case.get('document_type','question_paper'),output_path=output_pdf)
    runner=BenchmarkRunner(); metrics=[runner.text_metric('ocr_cer_score',[texts(result.document,'source_text')],[reference['ocr_text']]),runner.text_metric('translation_token_f1',[texts(result.document,'target_text')],[reference['translation_text']])]
    artifact=result.reconstruction_artifact
    report=runner.report(manifest.get('benchmark_id',manifest['dataset_id']+'-'+manifest['version']),case['domain']+':'+case['source_language']+'->'+case['target_language'],metrics,metadata={'case_id':case['case_id'],'stage_status':result.stage_status,'validation_passed':result.validation.passed,'validation_issues':len(result.validation.issues),'model_configuration':result.model_configuration,'source_sha256':sha256_file(root_path/case['input_path']),'reference_sha256':sha256_file(ref),'annotation_sha256':sha256_file(ann),'reconstruction_artifact':artifact.model_dump() if artifact else None})
    payload={'phase':19,'execution_status':'EXECUTED','benchmark':report.model_dump(),'accuracy_claim':True}
    (out/'benchmark-result.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
    return payload
