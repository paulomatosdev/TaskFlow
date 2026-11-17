import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    """App configurado para testes, com banco SQLite em memória."""
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Cliente HTTP para fazer requisições às rotas."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Sessão do banco pronta para uso dentro do contexto do app."""
    return _db
