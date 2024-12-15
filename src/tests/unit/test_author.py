import json

import pytest


@pytest.mark.asyncio
async def test_get_author(async_client, set_up_data, author_data):
    author_id = set_up_data["author"]["id"]
    response = await async_client.get(
        "/authors/{author_id}/".format(author_id=author_id)
    )
    assert response.status_code == 200
    assert author_id == response.json()["id"]
    assert author_data["first_name"] == response.json()["first_name"]
    assert author_data["last_name"] == response.json()["last_name"]
    assert author_data["birth_date"] == response.json()["birth_date"]


@pytest.mark.asyncio
async def test_get_authors(async_client, author_data):
    response = await async_client.get("/authors/")
    assert response.status_code == 200

    authors = response.json()

    assert len(authors) == 1
    assert authors[0]["first_name"] == author_data["first_name"]
    assert authors[0]["last_name"] == author_data["last_name"]
    assert authors[0]["birth_date"] == author_data["birth_date"]


@pytest.mark.asyncio
async def test_edit_author(set_up_data, async_client, edit_author_data):
    author_id = set_up_data["author"]["id"]
    response = await async_client.put(
        url="/authors/{author_id}/".format(author_id=author_id),
        content=json.dumps(edit_author_data),
    )
    assert response.status_code == 200
    assert bool(response.json())
