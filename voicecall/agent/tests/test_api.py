"""Tests de la API HTTP (auth, validación, webhooks) con factories fake."""

import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from voicecall_agent.main import create_app

AUTH = {"Authorization": "Bearer token-interno"}


class FakeConnection:
    async def create_offer(self):
        return "v=0"

    async def create_answer_for(self, sdp, sdp_type):
        return "v=0"

    async def apply_remote_answer(self, sdp):
        pass

    async def disconnect(self):
        pass


async def fake_starter(connection, session):
    class Handle:
        def cancel(self):
            pass

    return Handle()


def make_client() -> TestClient:
    app = create_app(connection_factory=FakeConnection, pipeline_starter=fake_starter)
    return TestClient(app)


def test_healthz():
    with make_client() as client:
        assert client.get("/healthz").json() == {"ok": True}


def test_calls_sin_token_da_401():
    with make_client() as client:
        assert client.post("/calls", json={"to": "+5491155550000"}).status_code == 401


def test_calls_numero_invalido_da_422():
    with make_client() as client:
        response = client.post("/calls", json={"to": "hola"}, headers=AUTH)
        assert response.status_code == 422


def test_calls_fuera_de_allowlist_da_403():
    with make_client() as client:
        response = client.post("/calls", json={"to": "+5491199999999"}, headers=AUTH)
        assert response.status_code == 403


def test_calls_ref_inexistente_da_404():
    with make_client() as client:
        assert client.get("/calls/noexiste", headers=AUTH).status_code == 404


def test_webhook_verify_ok():
    with make_client() as client:
        response = client.get(
            "/webhooks/whatsapp",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "verificador",
                "hub.challenge": "12345",
            },
        )
        assert response.status_code == 200
        assert response.text == "12345"


def test_webhook_verify_token_incorrecto():
    with make_client() as client:
        response = client.get(
            "/webhooks/whatsapp",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "otro",
                "hub.challenge": "12345",
            },
        )
        assert response.status_code == 403


def test_webhook_post_firma_invalida_da_403():
    with make_client() as client:
        response = client.post(
            "/webhooks/whatsapp",
            content=b"{}",
            headers={"X-Hub-Signature-256": "sha256=malamala"},
        )
        assert response.status_code == 403


def test_webhook_post_firmado_ok():
    body = json.dumps({"object": "whatsapp_business_account", "entry": []}).encode()
    signature = "sha256=" + hmac.new(b"supersecreto", body, hashlib.sha256).hexdigest()
    with make_client() as client:
        response = client.post(
            "/webhooks/whatsapp",
            content=body,
            headers={
                "X-Hub-Signature-256": signature,
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"received": 0}
