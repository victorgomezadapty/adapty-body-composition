"""Tests for synthetic seed data."""

from app.db.seed import get_synthetic_clients, get_synthetic_records


def test_synthetic_seed_data_has_clients_and_records() -> None:
    """Synthetic seed data should contain demo clients and longitudinal records."""
    clients = get_synthetic_clients()
    records_by_email = get_synthetic_records()

    assert len(clients) >= 3
    assert all("demo@example.com" in str(client["email"]) for client in clients)

    for client in clients:
        records = records_by_email[str(client["email"])]
        assert len(records) >= 2
        assert records[0]["measurement_date"] < records[-1]["measurement_date"]
