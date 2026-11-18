import pytest

from app import create_app


def test_app_usa_config_de_teste(app):
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


def test_config_desconhecida_gera_erro():
    with pytest.raises(ValueError):
        create_app("nao-existe")


def test_extensoes_registradas(app):
    assert {"migrate", "sqlalchemy"} <= app.extensions.keys()
