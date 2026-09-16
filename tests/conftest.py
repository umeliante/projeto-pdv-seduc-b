import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.auth import Base, get_admin, get_usuario_logado, get_usuario_opcional

@pytest.fixture()
def db_session_test():

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )
    Base.metadata.create_all(bind=engine)

    sessiontest = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = sessiontest()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session_test):

    def get_db_test():
        yield db_session_test
        
    def usuario_falso():
        return {"sub": "teste@teste.com", "nome": "Teste", "roles": "admin"}

    app.dependency_overrides[get_db] = get_db_test
    app.dependency_overrides[get_usuario_logado] = usuario_falso
    app.dependency_overrides[get_usuario_opcional] = usuario_falso
    app.dependency_overrides[get_admin] = usuario_falso


    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()