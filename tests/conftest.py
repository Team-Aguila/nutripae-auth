import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from db.session import SessionLocal, get_db, engine
# Se importa Base y todos los modelos para que Base.metadata los conozca
import models 
from db.seeder import seed_db

@pytest.fixture(scope="session", autouse=True)
def db_engine():
    """
    Fixture que se ejecuta una vez por sesión de tests.
    Crea todas las tablas de la base de datos antes de los tests
    y las elimina después.
    """
    # Importar todos los modelos es crucial para que Base los registre
    models.Base.metadata.create_all(bind=engine)
    # Populate initial data (roles, permissions, users, etc.)
    db_session = SessionLocal()
    try:
        seed_db(db_session)
    finally:
        db_session.close()
    yield
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db(db_engine) -> Session:
    """
    Crea una sesión de base de datos para un test, envuelta en una
    transacción que se revierte al final.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db: Session) -> TestClient:
    """
    Obtiene un TestClient que usa la sesión de base de datos transaccional.
    """
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db] 