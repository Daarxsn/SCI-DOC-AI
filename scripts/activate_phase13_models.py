import argparse
import json
from backend.core.config import Settings
from backend.core.model_registry import assert_runtime_dependencies, runtime_status

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["ocr", "translation", "equation", "diagram"], required=True)
    args = parser.parse_args()
    config = Settings(ml_runtime_enabled=True, ml_preload=False)
    selected = next(item for item in runtime_status(config)["models"] if item["key"] == args.model)
    if not selected["configured"]:
        raise SystemExit(f"{args.model} is not configured. Set its provider first.")
    assert_runtime_dependencies(config)
    if args.model == "ocr":
        from backend.ocr.factory import create_ocr_adapter
        create_ocr_adapter(config)._get_engine()
    elif args.model == "translation":
        from backend.translation.factory import create_translation_adapter
        create_translation_adapter(config)._load()
    elif args.model == "equation":
        from backend.mathematics.model_adapter import Pix2TexEquationAdapter
        Pix2TexEquationAdapter(config.ml_device)._load()
    else:
        if not config.diagram_model:
            raise SystemExit("DIAGRAM_MODEL must point to a trained model before activation.")
        from backend.diagrams.model_adapter import UltralyticsDiagramDetector
        UltralyticsDiagramDetector(config.diagram_model, config.ml_device)._load()
    print(json.dumps({"model": args.model, "status": "LOADED", "runtime": runtime_status(config)}, indent=2))

if __name__ == "__main__":
    main()
