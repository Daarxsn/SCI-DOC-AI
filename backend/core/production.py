from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ProductionReadiness:
    ready: bool
    checks: dict[str, bool]
    errors: list[str]


REQUIRED_PRODUCTION_ENV = ("SCI_DOC_API_KEY", "SCI_DOC_TENANT_ID")


def check_production_readiness() -> ProductionReadiness:
    checks = {}
    errors = []
    for name in REQUIRED_PRODUCTION_ENV:
        present = bool(os.getenv(name))
        checks[name] = present
        if not present:
            errors.append(f"missing required production setting: {name}")

    debug = os.getenv("DEBUG", "false").lower() == "true"
    checks["debug_disabled"] = not debug
    if debug:
        errors.append("DEBUG must be false in production")

    return ProductionReadiness(ready=not errors, checks=checks, errors=errors)
