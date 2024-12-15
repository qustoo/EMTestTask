import json

import pytest


@pytest.mark.asyncio
async def test_get_book(async_client, set_up_data, book_data):
    book_id = set_up_data["book"]["id"]
    response = await async_client.get("/books/{book_id}/".format(book_id=book_id))
    assert response.status_code == 200
    assert book_id == response.json()["id"]
    assert book_data["title"] == response.json()["title"]
    assert book_data["description"] == response.json()["description"]
    # -1 = Borrowed book
    assert book_data["count"] - 1 == response.json()["count"]


@pytest.mark.asyncio
async def test_get_books(async_client, set_up_data, book_data):
    author_id = set_up_data["author"]["id"]

    response = await async_client.get("/books/")

    assert response.status_code == 200

    books = response.json()
    assert len(books) == 1
    assert books[0]["title"] == book_data["title"]
    assert books[0]["description"] == book_data["description"]
    assert books[0]["count"] == book_data["count"] - 1
    assert books[0]["author_id"] == author_id


@pytest.mark.asyncio
async def test_edit_book(set_up_data, async_client, edit_book_data):
    book_id = set_up_data["book"]["id"]
    response = await async_client.put(
        url="/books/{book_id}/".format(book_id=book_id),
        content=json.dumps(edit_book_data),
    )
    assert response.status_code == 200
    assert bool(response.json())
