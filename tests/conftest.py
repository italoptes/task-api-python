import psycopg
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import get_db
from app.models.tarefa import Base

# Tenta criar o banco de dados de teste se ele não existir
try:
    conn = psycopg.connect("postgresql://postgres:postgres@postgres:5432/postgres", autocommit=True)
    conn.execute("CREATE DATABASE taskdb_test")
    conn.close()
except psycopg.errors.DuplicateDatabase:
    pass
except Exception as e:
    print(f"Aviso: Não foi possível verificar/criar taskdb_test: {e}")

TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@postgres:5432/taskdb_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria as tabelas no banco de testes ao iniciar e as remove ao final."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Garante isolamento: Inicia transação e faz rollback após cada teste."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Retorna um TestClient injetando o banco de testes isolado."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
