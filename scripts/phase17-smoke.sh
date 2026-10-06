#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
API_KEY="${SCI_DOC_API_KEY:-}"
TMP_FILE="${TMPDIR:-/tmp}/sci-doc-ai-phase17.png"

if [[ -z "$API_KEY" ]]; then
  echo "SCI_DOC_API_KEY is required" >&2
  exit 2
fi

cleanup() { rm -f "$TMP_FILE"; }
trap cleanup EXIT

printf '\x89PNG\r\n\x1a\n' > "$TMP_FILE"
# Minimal valid PNG signature is enough to exercise the upload MIME/extension boundary.
# The current ingestion contract may reject an incomplete image, which is reported as a failure.
if ! python3 - "$TMP_FILE" <<'PY'
import struct, zlib, sys
p=sys.argv[1]
raw=b"\x00\xff\xff\xff"
def chunk(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",1,1,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")
open(p,"wb").write(png)
PY
then
  echo "Failed to create test PNG" >&2
  exit 1
fi

health="$(curl -fsS "$API_BASE_URL/health")"
ready="$(curl -fsS "$API_BASE_URL/ready")"
python3 - "$health" "$ready" <<'PY'
import json,sys
health,ready=map(json.loads,sys.argv[1:3])
assert health["status"]=="ok", health
assert ready["status"]=="ready", ready
PY

upload="$(curl -fsS -X POST -F "file=@$TMP_FILE;type=image/png" "$API_BASE_URL/api/v1/documents/upload")"
document_id="$(python3 - "$upload" <<'PY'
import json,sys
v=json.loads(sys.argv[1])
assert v["status"]=="accepted", v
assert v.get("document_id"), v
print(v["document_id"])
PY
)"

job="$(curl -fsS -X POST "$API_BASE_URL/v1/jobs"   -H "Content-Type: application/json"   -H "X-API-Key: $API_KEY"   -d "{"document_id":"$document_id","target_language":"Hindi","domain":"general","idempotency_key":"phase17-$document_id"}")"

job_id="$(python3 - "$job" <<'PY'
import json,sys
v=json.loads(sys.argv[1])
assert v.get("job_id"), v
assert v["status"]=="queued", v
print(v["job_id"])
PY
)"

results="$(curl -fsS "$API_BASE_URL/v1/documents/$document_id/results" -H "X-API-Key: $API_KEY")"
python3 - "$results" "$document_id" <<'PY'
import json,sys
v=json.loads(sys.argv[1])
doc=sys.argv[2]
assert v["document_id"]==doc, v
assert v["status"]=="available", v
assert isinstance(v["artifacts"],list), v
PY

echo "Phase 17 smoke verification PASSED"
echo "document_id=$document_id"
echo "job_id=$job_id"
