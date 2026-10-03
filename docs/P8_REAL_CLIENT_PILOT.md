# P8 — Real Client Pilot

Phase 8 defines the operational contract for a controlled real-client pilot.

## Intake

Every pilot case records:

- case ID;
- source document path;
- SHA-256 source fingerprint;
- source language;
- target language;
- scientific domain;
- expected output format;
- client metadata.

Initial pilot scope is English → Hindi/Marathi for Mathematics, Physics and Biology.

## Evidence

Each case records:

- processing time;
- failure state/reason;
- whether human review was required;
- whether export was allowed;
- artifact IDs;
- measured metrics when available.

## Acceptance

A pilot report evaluates explicit acceptance criteria:

- maximum failure rate;
- maximum review rate;
- minimum export rate;
- optional processing-time limit;
- optional OCR/translation/reconstruction thresholds.

The report passes only when every configured criterion is satisfied.

## Important measurement rule

Fixture tests verify the pilot machinery only. They are **not client performance results**.

A real pilot must use an agreed fixed document set and record model versions, dataset version, source checksums, processing times, validation outcomes, reviewer corrections and measured quality metrics.

## Pilot exit package

The pilot should produce:

1. fixed input manifest;
2. model/configuration manifest;
3. per-document processing record;
4. validation/review records;
5. output artifacts;
6. benchmark report;
7. failure taxonomy;
8. optimization backlog.

No production accuracy claim should be made until those real measurements exist.
