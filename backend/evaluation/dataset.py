from pathlib import Path
from backend.evaluation.models import DatasetManifest

class DatasetValidator:
    def validate(self, manifest:DatasetManifest, *, root:str|Path|None=None)->list[str]:
        errors=[]; root_path=Path(root) if root else None; seen=set()
        for case in manifest.cases:
            if case.case_id in seen: errors.append(f"{case.case_id}: duplicate case id")
            seen.add(case.case_id)
            for field in ("input_path","reference_path","annotation_path"):
                value=getattr(case,field)
                if value and root_path and not (root_path/value).exists(): errors.append(f"{case.case_id}: missing {field}: {value}")
            if case.split.value=="test" and not case.reference_path: errors.append(f"{case.case_id}: test case requires reference_path")
        if not manifest.cases: errors.append("dataset contains no cases")
        return errors

def coverage_summary(manifest:DatasetManifest)->dict:
    result={"total":len(manifest.cases),"by_domain":{},"by_source_language":{},"by_target_language":{},"by_split":{}}
    for c in manifest.cases:
        for key,value in (("by_domain",c.domain),("by_source_language",c.source_language),("by_target_language",c.target_language or "none"),("by_split",c.split.value)):
            result[key][value]=result[key].get(value,0)+1
    return result
