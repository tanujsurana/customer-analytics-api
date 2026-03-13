import random
from datetime import datetime, timedelta, timezone

from faker import Faker

from app.core.database import SessionLocal
from app.models.customer import Customer
from app.models.event import Event

fake = Faker()


ACQUISITION_CHANNELS = ["LinkedIn", "organic", "referral", "ads", "social"]
EVENT_TYPES = ["login", "purchase", "feature_use", "session_start", "search"]


def random_signup_date():
    now = datetime.now(timezone.utc)
    days_ago = random.randint(1, 90)
    return now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))


def random_event_time(signup_date):
    now = datetime.now(timezone.utc)
    delta = now - signup_date
    random_seconds = random.randint(0, max(1, int(delta.total_seconds())))
    return signup_date + timedelta(seconds=random_seconds)


def seed_data(num_customers=50, min_events=2, max_events=10):
    db = SessionLocal()

    try:
        created_customers = []

        for _ in range(num_customers):
            signup_date = random_signup_date()

            customer = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                signup_date=signup_date,
                country=fake.country(),
                acquisition_channel=random.choice(ACQUISITION_CHANNELS),
                status="active",
            )

            db.add(customer)
            db.flush()  # gets customer.id before commit
            created_customers.append(customer)

        for customer in created_customers:
            event_count = random.randint(min_events, max_events)

            for _ in range(event_count):
                event_type = random.choice(EVENT_TYPES)

                if event_type == "purchase":
                    event_value = random.randint(20, 500)
                elif event_type == "feature_use":
                    event_value = random.randint(1, 20)
                elif event_type == "session_start":
                    event_value = random.randint(5, 120)
                else:
                    event_value = 1

                event = Event(
                    customer_id=customer.id,
                    event_type=event_type,
                    event_time=random_event_time(customer.signup_date),
                    event_value=event_value,
                )

                db.add(event)

        db.commit()
        print(f"Seeded {num_customers} customers with events successfully.")

    except Exception as e:
        db.rollback()
        print("Error while seeding data:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
