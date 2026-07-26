import pytest

from voicecall_agent.config import get_settings


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    """Entorno controlado para todos los tests."""
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "token-test")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "111222333")
    monkeypatch.setenv("WHATSAPP_WABA_ID", "999888777")
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "verificador")
    monkeypatch.setenv("META_APP_SECRET", "supersecreto")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("AGENT_API_TOKEN", "token-interno")
    monkeypatch.setenv("ALLOWED_DESTINATIONS", "+5491155550000")
    monkeypatch.setenv("MAX_CALL_MINUTES", "10")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
