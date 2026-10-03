# Phase 27 — Real Dataset Acquisition

Phase 27 establishes the controlled intake gate for real scientific source documents.

## Scope

- English source documents.
- Initial domains: Mathematics, Physics, Biology.
- Target languages: Hindi and Marathi.
- Accepted source formats: PDF, PNG, JPG, JPEG.
- Intake size: 1–20 documents/cases per batch.
- SHA-256 is recorded for every source.
- Document rights/provenance must be declared as verified, owned, licensed, public-domain, or permission-granted.

## Intake contract

Each case must provide:

- case_id
- source_path
- domain
- source_language
- target_language
- rights_status

The intake validator checks the file exists, is non-empty, uses a supported format, belongs to a supported domain/language pair, and has an acceptable rights status.

## Example metadata

    {
      "dataset_id": "sci-doc-real-intake",
      "version": "1.0.0",
      "cases": [
        {
          "case_id": "mathematics-hi-001",
          "source_path": "source/mathematics-hi-001.png",
          "domain": "mathematics",
          "source_language": "en",
          "target_language": "hi",
          "rights_status": "owned"
        }
      ]
    }

Run:

    python scripts/run_phase27_intake.py --metadata intake-metadata.json --root . --output phase27-intake.json

## Important evidence rule

CI uses a tiny synthetic file only to test the intake mechanics. It is NOT a scientific document and must never be treated as a benchmark result.

Phase 27 does not claim scientific accuracy. A real scientific document must be supplied and verified before Phase 28 ground-truth annotation begins.
