"""Configuración tipada del agente, cargada desde variables de entorno / .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Meta / WhatsApp Cloud API
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_waba_id: str = ""
    whatsapp_verify_token: str = "cambiame"
    meta_app_secret: str = ""
    graph_api_version: str = "v23.0"

    # OpenAI Realtime
    openai_api_key: str = ""
    openai_realtime_model: str = "gpt-realtime-2.1"
    openai_voice: str = "marin"

    # App
    agent_api_token: str = "cambiame-token-interno"
    public_base_url: str = "http://localhost:8000"
    allowed_destinations: str = ""
    max_call_minutes: int = 10
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def allowed_list(self) -> list[str]:
        """Números E.164 habilitados como destino. Vacío = nadie (seguro por defecto)."""
        return [n.strip() for n in self.allowed_destinations.split(",") if n.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
