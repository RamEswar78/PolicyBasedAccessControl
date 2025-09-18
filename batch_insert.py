import csv
from sqlalchemy.orm import Session
from app2.db import engine, Base, SessionLocal
from app2 import models

# ---------- Create tables if not exist ----------
Base.metadata.create_all(bind=engine)


def load_users(csv_path: str, db: Session):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:  # utf-8-sig removes BOM
        reader = csv.DictReader(f)
        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]  # remove extra spaces
        users = [
            models.User(
                id=int(row["id"]),
                username=row["username"].strip(),
                email=row["email"].strip(),
            )
            for row in reader
        ]
        db.add_all(users)
        db.commit()
        print(f"✅ Loaded {len(users)} users")


def load_employees(csv_path: str, db: Session):
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]  # remove extra spaces
        employees = [
            models.Employee(
                id=int(row["id"]),
                user_id=int(row["user_id"]),
                dept=row["dept"],
                role=row["role"],
                context=row["context"],
            )
            for row in reader
        ]
        db.add_all(employees)
        db.commit()
        print(f"✅ Loaded {len(employees)} employees")


def load_records(csv_path: str, db: Session):
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        records = [
            models.Record(
                id=int(row["id"]),
                owner_id=int(row["owner_id"]),
                dept=row["dept"],
                sensitivity=row["sensitivity"],
            )
            for row in reader
        ]
        db.add_all(records)
        db.commit()
        print(f"✅ Loaded {len(records)} records")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_users("app2/data/users.csv", db)
        load_employees("app2/data/employees.csv", db)
        load_records("app2/data/records.csv", db)
    finally:
        db.close()
