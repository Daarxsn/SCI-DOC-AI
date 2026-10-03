from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3

    def allows(self, retry_count: int) -> bool:
        return retry_count < self.max_attempts
