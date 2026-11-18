import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client_sem_csrf(app):
    """Cliente que NÃO envia token: usado para provar que a proteção está ativa."""
    return app.test_client()


@pytest.fixture
def client(app):
    """Cliente que busca um token válido em /csrf-token e o envia em toda requisição.

    O token fica ligado à sessão; o test client guarda o cookie, então ele continua
    válido nas requisições seguintes (inclusive depois de login/logout).
    """
    client = app.test_client()
    token = client.get("/csrf-token").get_json()["csrf_token"]
    client.environ_base["HTTP_X_CSRFTOKEN"] = token
    return client


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def usuario(client):
    """Cadastra a usuária padrão de tests.test_auth.USUARIO."""
    from tests.test_auth import cadastrar

    resposta = cadastrar(client)
    assert resposta.status_code == 201
