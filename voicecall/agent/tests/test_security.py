import hashlib
import hmac

from voicecall_agent.security import verify_meta_signature

SECRET = "supersecreto"
BODY = b'{"object":"whatsapp_business_account"}'


def _sign(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def test_firma_valida():
    assert verify_meta_signature(BODY, _sign(BODY, SECRET), SECRET)


def test_firma_invalida():
    assert not verify_meta_signature(BODY, _sign(BODY, "otro-secreto"), SECRET)


def test_firma_ausente():
    assert not verify_meta_signature(BODY, None, SECRET)


def test_header_malformado():
    assert not verify_meta_signature(BODY, "md5=abcdef", SECRET)


def test_sin_secret_configurado_pasa():
    assert verify_meta_signature(BODY, None, "")
