from pathlib import Path

from backend.pilot.acceptance import PilotAcceptanceCriteria, PilotCaseEvidence, PilotReport
from backend.pilot.intake import PilotIntakeCase, PilotIntakeValidator


def evidence(case_id, failed=False, review=False, export=True, metrics=None):
    return PilotCaseEvidence(
        case_id=case_id,
        processing_seconds=2.0,
        failed=failed,
        review_required=review,
        export_allowed=export,
        metrics=metrics or {},
    )


def test_pilot_report_passes_when_acceptance_criteria_are_met():
    report = PilotReport(
        pilot_id="pilot-1",
        tenant_id="tenant-a",
        dataset_id="client-set",
        dataset_version="1.0",
        model_versions={"ocr": "v1", "translation": "v1"},
        cases=[evidence("c1"), evidence("c2")],
        criteria=PilotAcceptanceCriteria(max_failure_rate=0.10, min_export_rate=0.90),
    )
    assert report.passed is True
    assert report.failure_rate == 0.0
    assert report.export_rate == 1.0


def test_pilot_report_fails_when_export_rate_is_below_threshold():
    report = PilotReport(
        pilot_id="pilot-2",
        tenant_id="tenant-a",
        dataset_id="client-set",
        dataset_version="1.0",
        model_versions={},
        cases=[evidence("c1", export=True), evidence("c2", export=False)],
        criteria=PilotAcceptanceCriteria(min_export_rate=0.90),
    )
    assert report.passed is False


def test_intake_rejects_invalid_pilot_configuration(tmp_path):
    source = tmp_path / "sample.pdf"
    source.write_bytes(b"%PDF-fixture")
    case = PilotIntakeCase(
        case_id="c1",
        source_path=str(source),
        source_language="fr",
        target_language="en",
        domain="chemistry",
    )
    errors = PilotIntakeValidator().validate(case)
    assert "pilot source language must be English" in errors
    assert "pilot target language must be Hindi or Marathi" in errors
    assert "pilot domain must be mathematics, physics, or biology" in errors


def test_intake_accepts_supported_source(tmp_path):
    source = tmp_path / "sample.pdf"
    source.write_bytes(b"%PDF-fixture")
    case = PilotIntakeCase(
        case_id="c1",
        source_path=str(source),
        source_language="en",
        target_language="hi",
        domain="physics",
    )
    assert PilotIntakeValidator().validate(case) == []
    assert len(case.source_sha256()) == 64
