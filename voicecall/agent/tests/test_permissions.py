from voicecall_agent.events import PermissionReply
from voicecall_agent.permissions import (
    TEMPORARY_PERMISSION_SECONDS,
    PermissionStore,
    normalize_wa_id,
)

NOW = 1_700_000_000.0


def test_normalize():
    assert normalize_wa_id("+54 911 5555-0000") == "5491155550000"
    assert normalize_wa_id("5491155550000") == "5491155550000"


def test_accept_temporal_dura_7_dias():
    store = PermissionStore()
    store.on_reply(
        PermissionReply(from_wa_id="5491155550000", response="accept"), now=NOW
    )
    assert store.is_granted("+5491155550000", now=NOW + 1)
    assert store.is_granted("+5491155550000", now=NOW + TEMPORARY_PERMISSION_SECONDS - 1)
    assert not store.is_granted("+5491155550000", now=NOW + TEMPORARY_PERMISSION_SECONDS + 1)


def test_accept_con_expiracion_de_meta():
    store = PermissionStore()
    store.on_reply(
        PermissionReply(
            from_wa_id="5491155550000", response="accept", expiration_timestamp=int(NOW) + 60
        ),
        now=NOW,
    )
    assert store.is_granted("5491155550000", now=NOW + 30)
    assert not store.is_granted("5491155550000", now=NOW + 61)


def test_accept_permanente_no_expira():
    store = PermissionStore()
    store.on_reply(
        PermissionReply(from_wa_id="5491155550000", response="accept", is_permanent=True),
        now=NOW,
    )
    assert store.is_granted("5491155550000", now=NOW + 10 * TEMPORARY_PERMISSION_SECONDS)


def test_reject_revoca():
    store = PermissionStore()
    store.on_reply(PermissionReply(from_wa_id="5491155550000", response="accept"), now=NOW)
    store.on_reply(PermissionReply(from_wa_id="5491155550000", response="reject"), now=NOW + 1)
    assert not store.is_granted("5491155550000", now=NOW + 2)


def test_sync_desde_api():
    store = PermissionStore()
    store.grant_from_api("5491155550000", "temporary", NOW + 100)
    assert store.is_granted("5491155550000", now=NOW + 50)
    store.grant_from_api("5491155550000", "no_permission", None)
    assert not store.is_granted("5491155550000", now=NOW + 50)


def test_desconocido_no_tiene_permiso():
    assert not PermissionStore().is_granted("5491155550000")
