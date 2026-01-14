from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
import pytest
from app.main import app
from fastapi.testclient import TestClient

TEST_DB_URL = 'sqlite:///./test.db'

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False}
)


TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base.metadata.create_all(bind=engine)

@pytest.fixture()
def test_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def test_client(test_session):
    app.dependency_overrides[get_db] = lambda: test_session
    with TestClient(app) as client:
        yield client

