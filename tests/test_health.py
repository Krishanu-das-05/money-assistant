import pytest
from django.db import OperationalError, connection


@pytest.mark.django_db
def test_healthz_ok_with_working_db(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok"}


def test_healthz_503_when_db_unreachable(client, monkeypatch):
    def broken_cursor(*args, **kwargs):
        raise OperationalError("database unreachable")

    monkeypatch.setattr(connection, "cursor", broken_cursor)

    response = client.get("/healthz")

    assert response.status_code == 503
    assert response.json()["db"] == "error"
