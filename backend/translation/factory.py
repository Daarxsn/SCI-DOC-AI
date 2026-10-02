from backend.core.config import Settings, settings
from backend.translation.adapter import TranslationAdapter
from backend.translation.huggingface_adapter import HuggingFaceNllbAdapter
from backend.translation.rule_based_adapter import RuleBasedAdapter


def create_translation_adapter(config: Settings = settings) -> TranslationAdapter:
    provider = config.translation_provider.strip().lower()
    if provider == "rule-based-dev":
        return RuleBasedAdapter()
    if provider == "huggingface-nllb":
        return HuggingFaceNllbAdapter(model_name=config.translation_model, device=config.ml_device)
    raise ValueError(
        f"Unsupported translation provider '{config.translation_provider}'. "
        "Supported providers: rule-based-dev, huggingface-nllb."
    )
