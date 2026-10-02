from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionResult:
    metric: str
    current: float
    baseline: float
    delta: float
    passed: bool


class RegressionGate:
    def __init__(self, max_drop: float = 0.02):
        self.max_drop = max_drop

    def compare(self, metric: str, current: float, baseline: float) -> RegressionResult:
        delta = current - baseline
        return RegressionResult(
            metric=metric,
            current=current,
            baseline=baseline,
            delta=delta,
            passed=delta >= -self.max_drop,
        )
