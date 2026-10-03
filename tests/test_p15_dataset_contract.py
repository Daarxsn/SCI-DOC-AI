import json
from pathlib import Path
def test_phase15_manifest_has_full_domain_language_matrix():
 data=json.loads(Path("datasets/golden/phase15-manifest.example.json").read_text()); pairs={(c["domain"],c["target_language"]) for c in data["cases"]}
 assert pairs=={(d,t) for d in ("mathematics","physics","biology") for t in ("hi","mr")}
def test_phase15_annotation_schema_is_structured():
 schema=json.loads(Path("datasets/golden/phase15-annotation.schema.json").read_text())
 assert "pages" in schema["required"]
 element=schema["properties"]["pages"]["items"]["properties"]["elements"]["items"]
 assert "annotation_type" in element["required"]
