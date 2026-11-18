import importlib

import pytest

import config

SQLITE_PADRAO = "sqlite:///dados.db"
POSTGRES = "postgresql+psycopg://usuario:senha@localhost/taskflow"


@pytest.fixture
def recarregar_config(monkeypatch):
    # config.py lê o ambiente ao ser importado; ignora um .env real da máquina
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    yield lambda: importlib.reload(config)
    monkeypatch.undo()
    importlib.reload(config)


@pytest.mark.parametrize("valor, esperado", [
    (None, SQLITE_PADRAO), ("", SQLITE_PADRAO), (POSTGRES, POSTGRES)])
def test_database_url(monkeypatch, recarregar_config, valor, esperado):
    if valor is None:
        monkeypatch.delenv("DATABASE_URL", raising=False)
    else:
        monkeypatch.setenv("DATABASE_URL", valor)
    assert recarregar_config().Config.SQLALCHEMY_DATABASE_URI == esperado
