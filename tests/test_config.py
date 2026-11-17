import importlib

import pytest

import config

SQLITE_PADRAO = "sqlite:///dados.db"


@pytest.fixture
def recarregar_config(monkeypatch):
    """Recarrega config.py depois de ajustar as variáveis de ambiente.

    As classes de config leem os.environ na importação, então é preciso
    recarregar o módulo para que vejam o valor definido no teste.
    """
    # Impede que um .env real da máquina interfira no teste
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)

    def _recarregar():
        return importlib.reload(config)

    yield _recarregar

    # Restaura o módulo com o ambiente original para os demais testes
    monkeypatch.undo()
    importlib.reload(config)


def test_database_url_ausente_usa_sqlite(monkeypatch, recarregar_config):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    cfg = recarregar_config()
    assert cfg.Config.SQLALCHEMY_DATABASE_URI == SQLITE_PADRAO


def test_database_url_vazia_usa_sqlite(monkeypatch, recarregar_config):
    monkeypatch.setenv("DATABASE_URL", "")
    cfg = recarregar_config()
    assert cfg.Config.SQLALCHEMY_DATABASE_URI == SQLITE_PADRAO


def test_database_url_definida_e_respeitada(monkeypatch, recarregar_config):
    url = "postgresql+psycopg://usuario:senha@localhost/taskflow"
    monkeypatch.setenv("DATABASE_URL", url)
    cfg = recarregar_config()
    assert cfg.Config.SQLALCHEMY_DATABASE_URI == url
