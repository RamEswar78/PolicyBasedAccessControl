from app2.db import Base, engine
from app2.models import User, Employee, Record


def create_tables():
    print("📦 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")


if __name__ == "__main__":
    create_tables()
