import importlib
import os
import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    import database
    import models
    import main

    importlib.reload(database)
    importlib.reload(models)
    importlib.reload(main)

    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)

    with TestClient(main.app) as test_client:
        yield test_client

    database.engine.dispose()
    os.remove(db_path)


def test_full_crud_flow(client):
    create_response = client.post(
        "/books",
        json={"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi"},
    )
    assert create_response.status_code == 200
    created_book = create_response.json()
    assert created_book["title"] == "Dune"
    assert created_book["status"] == "available"

    book_id = created_book["id"]

    list_response = client.get("/books")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/books/{book_id}",
        json={"status": "borrowed", "genre": "Classic Sci-Fi"},
    )
    assert update_response.status_code == 200
    updated_book = update_response.json()
    assert updated_book["status"] == "borrowed"
    assert updated_book["genre"] == "Classic Sci-Fi"

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/books/{book_id}")
    assert missing_response.status_code == 404
