import json

from flask import Response


def test_api_should_get_all_bookings(client):
    response = client.get("/api/reservas")
    bookings = json.loads(response.data)
    assert len(bookings) == 4
    assert response.status_code == 200


def test_api_should_get_a_booking_by_uuid(client):
    response = client.get("/api/reservas/e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    booking = json.loads(response.data)
    assert booking["guest"]["document"] == "00157624242"


def test_api_should_return_status_code_404_for_a_inexisting_booking(client):
    response = client.get("/api/reservas/e08f76b8-0e71-4a48-a85a-bf7e8f61479e")
    assert response.status_code == 404


def test_api_should_create_a_new_booking(client):
    booking_dto = {
        "check_in": "2024-09-15T08:30:00",
        "check_out": "2024-09-18T12:30:00",
        "guest_document": "00157624242",
        "accommodation_id": 1,
    }
    response: Response = client.post(
        "/api/reservas/cadastro",
        data=json.dumps(booking_dto),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 201
    assert response.json
    assert response.json["uuid"]
    assert response.json["created_at"]


def test_api_should_return_status_code_400(client):
    response = client.post(
        "/api/reservas/cadastro",
        data=json.dumps({}),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400


def test_api_should_delete_an_accommodation(client):
    response = client.delete("/api/reservas/e08f76e8-0e71-4a48-a85a-bf7e8f61479e")
    assert response.status_code == 200
    assert response.text == "DELETED"


def test_api_should_return_status_code_404_on_delete(client):
    response = client.delete("/api/reservas/e08f76e8-0e71-4a48-a85a-Cf7e8f61479e")
    assert response.status_code == 404


def test_api_should_update_an_accommodation(client):
    updated_booking_data = {
        "uuid": "e08f76e8-0e71-4a48-a85a-bf7e8f61479e",
        "status": "Finalizada",
        "check_in": "2024-06-15T08:30:00",
        "check_out": "2024-06-18T17:30:00",
        "guest": {
            "document": "00157624242",
            "name": "Bento Luiz",
            "surname": "Vervloet Machado da Silva Neto",
            "country": "Brazil",
            "created_at": "2024-03-15T10:30:00",
            "phone": "48992054211",
        },
        "accommodation": {
            "id": 6,
            "name": "Estacionamento para overlanders",
            "status": "Disponível",
            "total_guests": 4,
            "single_beds": 0,
            "double_beds": 0,
            "min_nights": 2,
            "price": 100,
            "created_at": "2000-01-01T00:15:00",
            "amenities": ["ducha"],
        },
    }
    response = client.put(
        "/api/reservas",
        data=json.dumps(updated_booking_data),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 200
    assert response.text == "UPDATED"


def test_api_should_return_status_code_404_on_update(client):
    updated_booking_data = {
        "uuid": "e08f76e8-0e72-4a48-a85a-bf7e8f61479e",
        "status": "Finalizada",
        "check_in": "2024-06-15T08:30:00",
        "check_out": "2024-06-18T17:30:00",
        "guest": {
            "document": "00157624242",
            "name": "Bento Luiz",
            "surname": "Vervloet Machado da Silva Neto",
            "country": "Brazil",
            "created_at": "2024-03-15T10:30:00",
            "phone": "48992054211",
        },
        "accommodation": {
            "id": 6,
            "name": "Estacionamento para overlanders",
            "status": "Disponível",
            "total_guests": 4,
            "single_beds": 0,
            "double_beds": 0,
            "min_nights": 2,
            "price": 100,
            "created_at": "2000-01-01T00:15:00",
            "amenities": ["ducha"],
        },
    }
    response = client.put(
        "/api/reservas",
        data=json.dumps(updated_booking_data),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 404
