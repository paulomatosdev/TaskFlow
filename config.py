import os
import secrets

from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env (se existir)
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///dados.db"
    )


class DevelopmentConfig(Config):
    DEBUG = True
    # Sem SECRET_KEY no .env, gera uma chave aleatória a cada execução.
    # Serve para desenvolvimento, mas as sessões são perdidas ao reiniciar.
    SECRET_KEY = Config.SECRET_KEY or secrets.token_hex(32)


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "chave-de-teste"
    # Banco em memória: cada teste começa limpo e não toca no dados.db
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
