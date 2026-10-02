from functools import lru_cache

from backend.translation.adapter import TranslationAdapter
from backend.translation.models import TranslationLanguage


LANGUAGE_CODES = {
    TranslationLanguage.ENGLISH: "eng_Latn",
    TranslationLanguage.HINDI: "hin_Deva",
    TranslationLanguage.MARATHI: "mar_Deva",
}


class HuggingFaceNllbAdapter(TranslationAdapter):
    """NLLB-200 translation adapter using Hugging Face Transformers."""

    name = "huggingface-nllb"

    def __init__(
        self,
        model_name: str = "facebook/nllb-200-distilled-600M",
        max_new_tokens: int = 512,
        num_beams: int = 4,
    ) -> None:
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.num_beams = num_beams

    @lru_cache(maxsize=1)
    def _load(self):
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "transformers and torch are required for the Hugging Face "
                "translation adapter."
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        return tokenizer, model

    def translate(
        self,
        text: str,
        *,
        source_language: TranslationLanguage,
        target_language: TranslationLanguage,
        context: str | None = None,
    ) -> tuple[str, float]:
        if source_language == target_language:
            return text, 1.0
        if source_language not in LANGUAGE_CODES or target_language not in LANGUAGE_CODES:
            raise ValueError("NLLB adapter supports English, Hindi, and Marathi only")
        if not text.strip():
            return text, 1.0

        tokenizer, model = self._load()
        tokenizer.src_lang = LANGUAGE_CODES[source_language]

        encoded = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )
        forced_bos_token_id = tokenizer.convert_tokens_to_ids(
            LANGUAGE_CODES[target_language]
        )
        generated = model.generate(
            **encoded,
            forced_bos_token_id=forced_bos_token_id,
            max_new_tokens=self.max_new_tokens,
            num_beams=self.num_beams,
        )
        translated = tokenizer.batch_decode(
            generated, skip_special_tokens=True
        )[0].strip()

        # NLLB has no calibrated document-level confidence score.
        # Keep the existing interface conservative until P2/P6 calibration.
        confidence = 0.75 if translated else 0.0
        return translated, confidence
