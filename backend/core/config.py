from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SCI-DOC AI"
    api_version: str = "v1"
    debug: bool = False
    max_upload_size_mb: int = 50
    ocr_provider: str = "tesseract"
    ocr_language: str = "eng"
    translation_provider: str = "rule-based-dev"
    translation_model: str = "facebook/nllb-200-distilled-600M"
    equation_provider: str = "baseline"
    diagram_provider: str = "baseline"
    diagram_model: str = ""
    model_cache_dir: str | None = None
    ml_device: str = "auto"
    ml_runtime_enabled: bool = False
    ml_preload: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
