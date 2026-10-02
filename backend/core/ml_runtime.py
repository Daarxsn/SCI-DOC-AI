from importlib.util import find_spec


def package_available(package_name: str) -> bool:
    return find_spec(package_name) is not None


def runtime_status() -> dict[str, bool]:
    """Return optional ML package availability without loading model weights."""
    return {
        "paddlepaddle": package_available("paddle"),
        "paddleocr": package_available("paddleocr"),
        "torch": package_available("torch"),
        "transformers": package_available("transformers"),
        "sentencepiece": package_available("sentencepiece"),
        "ultralytics": package_available("ultralytics"),
        "pix2tex": package_available("pix2tex"),
        "pytesseract": package_available("pytesseract"),
    }


def select_device(requested: str = "auto") -> str:
    if requested and requested != "auto":
        return requested
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"
