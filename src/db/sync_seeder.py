import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from db.seeder import seed_db
from db.base import Base

def run_seeder():
    # We need to adapt the DATABASE_URL for a synchronous driver
    # The `seed_db` function is synchronous
    sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_database_url)
    
    # Create tables if they don't exist
    # This is usually handled by migrations (Alembic), but for a seeder it can be useful
    # to ensure the schema is there.
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    
    try:
        print("Starting to seed database...")
        seed_db(db_session)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    run_seeder() 