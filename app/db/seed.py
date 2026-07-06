"""Synthetic seed data for local demos and portfolio screenshots."""

from datetime import date

from sqlmodel import Session, select

from app.db.database import engine, init_db
from app.models.client import Client
from app.models.goal import Goal
from app.models.inbody_record import InBodyRecord
from app.models.plan import Plan


def get_synthetic_clients() -> list[dict[str, object]]:
    """Return synthetic client records for demos."""
    return [
        {
            "first_name": "Alex",
            "last_name": "Morgan",
            "email": "alex.morgan.demo@example.com",
            "phone": "+1-555-0101",
            "gender": "male",
            "birth_date": date(1990, 5, 20),
            "main_goal": "fat_loss",
        },
        {
            "first_name": "Jordan",
            "last_name": "Lee",
            "email": "jordan.lee.demo@example.com",
            "phone": "+1-555-0102",
            "gender": "female",
            "birth_date": date(1988, 11, 3),
            "main_goal": "recomposition",
        },
        {
            "first_name": "Taylor",
            "last_name": "Reed",
            "email": "taylor.reed.demo@example.com",
            "phone": "+1-555-0103",
            "gender": "non_binary",
            "birth_date": date(1995, 2, 14),
            "main_goal": "muscle_gain",
        },
    ]


def get_synthetic_records() -> dict[str, list[dict[str, object]]]:
    """Return synthetic InBody-style records keyed by client email."""
    return {
        "alex.morgan.demo@example.com": [
            {
                "measurement_date": date(2026, 1, 5),
                "weight_kg": 88.0,
                "body_fat_percentage": 28.0,
                "skeletal_muscle_mass_kg": 34.0,
                "bmi": 27.2,
                "visceral_fat_level": 10,
                "basal_metabolic_rate": 1780,
                "waist_hip_ratio": 0.91,
            },
            {
                "measurement_date": date(2026, 3, 5),
                "weight_kg": 84.5,
                "body_fat_percentage": 24.5,
                "skeletal_muscle_mass_kg": 34.4,
                "bmi": 26.1,
                "visceral_fat_level": 8,
                "basal_metabolic_rate": 1805,
                "waist_hip_ratio": 0.88,
            },
        ],
        "jordan.lee.demo@example.com": [
            {
                "measurement_date": date(2026, 1, 10),
                "weight_kg": 66.2,
                "body_fat_percentage": 31.0,
                "skeletal_muscle_mass_kg": 24.2,
                "bmi": 24.3,
                "visceral_fat_level": 7,
                "basal_metabolic_rate": 1380,
                "waist_hip_ratio": 0.82,
            },
            {
                "measurement_date": date(2026, 3, 10),
                "weight_kg": 65.8,
                "body_fat_percentage": 28.3,
                "skeletal_muscle_mass_kg": 25.0,
                "bmi": 24.1,
                "visceral_fat_level": 6,
                "basal_metabolic_rate": 1415,
                "waist_hip_ratio": 0.80,
            },
        ],
        "taylor.reed.demo@example.com": [
            {
                "measurement_date": date(2026, 1, 15),
                "weight_kg": 73.0,
                "body_fat_percentage": 19.2,
                "skeletal_muscle_mass_kg": 32.8,
                "bmi": 23.8,
                "visceral_fat_level": 5,
                "basal_metabolic_rate": 1690,
                "waist_hip_ratio": 0.84,
            },
            {
                "measurement_date": date(2026, 3, 15),
                "weight_kg": 75.1,
                "body_fat_percentage": 19.7,
                "skeletal_muscle_mass_kg": 34.1,
                "bmi": 24.5,
                "visceral_fat_level": 5,
                "basal_metabolic_rate": 1740,
                "waist_hip_ratio": 0.84,
            },
        ],
    }


def seed_database() -> dict[str, int]:
    """Seed the local database with synthetic records if it is empty."""
    init_db()

    with Session(engine) as session:
        existing_count = len(session.exec(select(Client)).all())
        if existing_count:
            return {"clients_created": 0, "records_created": 0}

        clients_created = 0
        records_created = 0
        records_by_email = get_synthetic_records()

        for client_payload in get_synthetic_clients():
            client = Client(**client_payload)
            session.add(client)
            session.commit()
            session.refresh(client)
            clients_created += 1

            session.add(
                Goal(
                    client_id=client.id,
                    goal_type=client.main_goal,
                    target_weight_kg=82.0 if client.main_goal == "fat_loss" else None,
                    target_body_fat_percentage=22.0,
                    target_muscle_mass_kg=35.0 if client.main_goal != "fat_loss" else None,
                    deadline=date(2026, 7, 1),
                    notes="Synthetic goal for local demo data.",
                )
            )
            session.add(
                Plan(
                    client_id=client.id,
                    plan_type="hybrid",
                    weekly_training_sessions=4,
                    calorie_target=2300,
                    protein_target_g=160,
                    notes="Synthetic plan for coaching workflow demos.",
                )
            )

            for record_payload in records_by_email[str(client.email)]:
                session.add(InBodyRecord(client_id=client.id, **record_payload))
                records_created += 1

        session.commit()
        return {"clients_created": clients_created, "records_created": records_created}


if __name__ == "__main__":
    result = seed_database()
    print(result)

