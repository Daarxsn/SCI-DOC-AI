from importlib.util import find_spec


def package_available(package_name: str) -> bool:
    return find_spec(package_name) is not None


def runtime_status() -> dict[str, bool]:
    """Return availability of optional P1 ML packages.

    This performs no model download or heavyweight import. It is safe to use
    from health/diagnostic tooling before an ML environment is installed.
    """
    return {
        "paddleocr": package_available("paddleocr"),
        "torch": package_available("torch"),
        "transformers": package_available("transformers"),
        "sentencepiece": package_available("sentencepiece"),
        "pytesseract": package_available("pytesseract"),
    }
