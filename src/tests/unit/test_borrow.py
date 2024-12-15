import json
from datetime import date

import pytest
from starlette import status


@pytest.mark.asyncio
async def test_get_borrow(set_up_data, async_client, borrow_data):
    book_id = set_up_data["book"]["id"]
    borrow_id = set_up_data["borrow"]["id"]
    response = await async_client.get(
        "/borrows/{borrow_id}/".format(borrow_id=borrow_id)
    )
    borrow = response.json()
    assert response.status_code == 200
    assert borrow_id == borrow["id"]
    assert book_id == borrow["book_id"]
    assert borrow_data["reader_name"] == borrow["reader_name"]
    assert borrow_data["borrow_date"] == borrow["borrow_date"]


@pytest.mark.asyncio
async def test_get_borrows(async_client, set_up_data, borrow_data):
    book_id = set_up_data["book"]["id"]

    response = await async_client.get("/borrows/")
    assert response.status_code == 200

    borrows = response.json()
    assert len(borrows) == 1
    assert borrows[0]["reader_name"] == borrow_data["reader_name"]
    assert borrows[0]["borrow_date"] == borrow_data["borrow_date"]
    assert borrows[0]["book_id"] == book_id


@pytest.mark.asyncio
async def test_return_borrowed_book(
    set_up_data,
    async_client,
):
    book_id = set_up_data["book"]["id"]
    borrow_id = set_up_data["borrow"]["id"]
    book_response = await async_client.get("/books/{book_id}/".format(book_id=book_id))

    response = await async_client.patch(
        url="/borrows/{borrow_id}/return/".format(borrow_id=borrow_id),
        content=json.dumps(
            {"book_id": book_id, "return_date": date.today().isoformat()}
        ),
    )
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json())

    updated_book_response = await async_client.get(
        "/books/{book_id}/".format(book_id=book_id)
    )

    assert updated_book_response.json()["count"] - book_response.json()["count"] == 1


@pytest.mark.asyncio
async def test_return_already_returned_book(
    set_up_data,
    async_client,
):
    book_id = set_up_data["book"]["id"]
    borrow_id = set_up_data["borrow"]["id"]
    response = await async_client.patch(
        url="/borrows/{borrow_id}/return/".format(borrow_id=borrow_id),
        content=json.dumps(
            {"book_id": book_id, "return_date": date.today().isoformat()}
        ),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
