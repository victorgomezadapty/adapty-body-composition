"""API integration tests using an in-memory SQLite database."""

from collections.abc import Generator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db.database import get_session
from app.main import app


@pytest.fixture(name="client")
def client_fixture() -> Generator[TestClient, None, None]:
    """Create a test client backed by an isolated in-memory database."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)

    def get_test_session() -> Generator[Session, None, None]:
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)


def create_client_payload(email: str = "alex.demo@example.com") -> dict[str, object]:
    """Return a valid synthetic client payload."""
    return {
        "first_name": "Alex",
        "last_name": "Demo",
        "email": email,
        "phone": "+1-555-0100",
        "gender": "male",
        "birth_date": "1990-05-20",
        "main_goal": "fat_loss",
    }


def create_client(client: TestClient, email: str = "alex.demo@example.com") -> int:
    """Create a synthetic client and return its id."""
    response = client.post("/clients", json=create_client_payload(email=email))
    assert response.status_code == 201
    return int(response.json()["id"])


def create_record_payload(
    measurement_date: str = "2026-01-01",
    weight_kg: float = 88.0,
    body_fat_percentage: float = 28.0,
    skeletal_muscle_mass_kg: float = 34.0,
) -> dict[str, object]:
    """Return a valid synthetic InBody-style record payload."""
    return {
        "measurement_date": measurement_date,
        "weight_kg": weight_kg,
        "body_fat_percentage": body_fat_percentage,
        "skeletal_muscle_mass_kg": skeletal_muscle_mass_kg,
        "bmi": 27.2,
        "visceral_fat_level": 10,
        "basal_metabolic_rate": 1780,
        "waist_hip_ratio": 0.91,
    }


def test_create_get_update_delete_client(client: TestClient) -> None:
    """Client CRUD endpoints should support the full MVP lifecycle."""
    client_id = create_client(client)

    list_response = client.get("/clients")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/clients/{client_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "alex.demo@example.com"

    update_response = client.patch(
        f"/clients/{client_id}",
        json={"main_goal": "recomposition"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["main_goal"] == "recomposition"

    delete_response = client.delete(f"/clients/{client_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/clients/{client_id}")
    assert missing_response.status_code == 404


def test_duplicate_client_email_returns_409(client: TestClient) -> None:
    """Client emails should be unique for the MVP."""
    create_client(client)
    response = client.post("/clients", json=create_client_payload())

    assert response.status_code == 409


def test_pagination_and_filtering(client: TestClient) -> None:
    """List clients should support pagination and filtering."""
    create_client(client, email="first@example.com")
    create_client(client, email="second@example.com")

    paged_response = client.get("/clients?skip=1&limit=1")
    assert paged_response.status_code == 200
    assert len(paged_response.json()) == 1

    search_response = client.get("/clients?search=second")
    assert search_response.status_code == 200
    assert search_response.json()[0]["email"] == "second@example.com"

    goal_response = client.get("/clients?main_goal=fat_loss")
    assert goal_response.status_code == 200
    assert len(goal_response.json()) == 2


def test_create_update_delete_inbody_record(client: TestClient) -> None:
    """InBody-style record endpoints should support CRUD."""
    client_id = create_client(client)
    create_response = client.post(
        f"/clients/{client_id}/inbody-records",
        json=create_record_payload(),
    )
    assert create_response.status_code == 201
    record_id = create_response.json()["id"]

    list_response = client.get(f"/clients/{client_id}/inbody-records")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/inbody-records/{record_id}")
    assert get_response.status_code == 200
    assert get_response.json()["weight_kg"] == 88.0

    update_response = client.patch(
        f"/inbody-records/{record_id}",
        json={"weight_kg": 87.2},
    )
    assert update_response.status_code == 200
    assert update_response.json()["weight_kg"] == 87.2

    all_records_response = client.get("/inbody-records")
    assert all_records_response.status_code == 200
    assert len(all_records_response.json()) == 1

    delete_response = client.delete(f"/inbody-records/{record_id}")
    assert delete_response.status_code == 204


def test_invalid_inbody_record_values_return_422(client: TestClient) -> None:
    """Invalid metric values should be rejected by request validation."""
    client_id = create_client(client)
    payload = create_record_payload(weight_kg=-10.0)

    response = client.post(f"/clients/{client_id}/inbody-records", json=payload)

    assert response.status_code == 422


def test_missing_client_returns_404(client: TestClient) -> None:
    """Nested resources should return 404 when the client does not exist."""
    response = client.post(
        "/clients/999/inbody-records",
        json=create_record_payload(),
    )

    assert response.status_code == 404


def test_goals_and_plans_endpoints(client: TestClient) -> None:
    """Goals and plans should support create, list, update, and delete."""
    client_id = create_client(client)

    goal_response = client.post(
        f"/clients/{client_id}/goals",
        json={
            "goal_type": "fat_loss",
            "target_weight_kg": 82.0,
            "target_body_fat_percentage": 22.0,
            "deadline": date(2026, 6, 1).isoformat(),
            "notes": "Synthetic goal for testing.",
        },
    )
    assert goal_response.status_code == 201
    goal_id = goal_response.json()["id"]

    plan_response = client.post(
        f"/clients/{client_id}/plans",
        json={
            "plan_type": "hybrid",
            "weekly_training_sessions": 4,
            "calorie_target": 2300,
            "protein_target_g": 170,
            "notes": "Synthetic plan for testing.",
        },
    )
    assert plan_response.status_code == 201
    plan_id = plan_response.json()["id"]

    assert len(client.get(f"/clients/{client_id}/goals").json()) == 1
    assert len(client.get(f"/clients/{client_id}/plans").json()) == 1

    updated_goal = client.patch(f"/goals/{goal_id}", json={"notes": "Updated"})
    updated_plan = client.patch(f"/plans/{plan_id}", json={"weekly_training_sessions": 5})
    assert updated_goal.status_code == 200
    assert updated_plan.status_code == 200

    assert client.delete(f"/goals/{goal_id}").status_code == 204
    assert client.delete(f"/plans/{plan_id}").status_code == 204


def test_summary_and_reports_with_two_records(client: TestClient) -> None:
    """Report endpoints should generate useful progress interpretation."""
    client_id = create_client(client)
    client.post(
        f"/clients/{client_id}/inbody-records",
        json=create_record_payload(),
    )
    client.post(
        f"/clients/{client_id}/inbody-records",
        json=create_record_payload(
            measurement_date="2026-03-01",
            weight_kg=84.5,
            body_fat_percentage=24.5,
            skeletal_muscle_mass_kg=34.4,
        ),
    )

    summary_response = client.get(f"/clients/{client_id}/summary")
    coach_response = client.get(f"/clients/{client_id}/coach-report")
    client_response = client.get(f"/clients/{client_id}/client-report")

    assert summary_response.status_code == 200
    assert summary_response.json()["summary"]["classification"] == "positive"
    assert coach_response.status_code == 200
    assert "Weight change" in coach_response.json()["message"]
    assert client_response.status_code == 200
    assert "medical diagnosis" in client_response.json()["disclaimer"]


def test_summary_without_enough_records(client: TestClient) -> None:
    """Summary endpoint should handle clients with fewer than two records."""
    client_id = create_client(client)
    client.post(
        f"/clients/{client_id}/inbody-records",
        json=create_record_payload(),
    )

    response = client.get(f"/clients/{client_id}/summary")

    assert response.status_code == 200
    assert response.json()["summary"]["trend_available"] is False
    assert response.json()["summary"]["classification"] == "not_enough_data"
