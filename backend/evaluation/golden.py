from dataclasses import dataclass, field


@dataclass
class GoldenCase:
    case_id: str
    domain: str
    source_language: str
    target_language: str | None
    input_path: str
    reference_path: str | None
    annotations: dict = field(default_factory=dict)


class GoldenDataset:
    def __init__(self):
        self._cases: dict[str, GoldenCase] = {}

    def add(self, case: GoldenCase):
        if case.case_id in self._cases:
            raise ValueError(f"Duplicate golden case: {case.case_id}")
        self._cases[case.case_id] = case

    def get(self, case_id: str):
        return self._cases.get(case_id)

    def list(self, domain: str | None = None):
        cases = list(self._cases.values())
        return [c for c in cases if domain is None or c.domain == domain]

    def validate(self):
        errors = []
        for case in self._cases.values():
            if not case.input_path:
                errors.append(f"{case.case_id}: missing input_path")
            if not case.domain:
                errors.append(f"{case.case_id}: missing domain")
        return errors
