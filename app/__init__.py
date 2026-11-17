from flask import Flask

from app.extensions import db, migrate
from config import config_by_name


def create_app(config_name="development"):
    """Application factory: cria e configura uma instância do app."""
    app = Flask(__name__)

    # Configurações carregadas de config.py / variáveis de ambiente
    if config_name not in config_by_name:
        raise ValueError(f"Configuração desconhecida: {config_name!r}")
    app.config.from_object(config_by_name[config_name])

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY não definida. Configure a variável de ambiente "
            "SECRET_KEY (veja o arquivo .env.example)."
        )

    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os modelos para que fiquem registrados no db.metadata
    from app import models  # noqa: F401

    # Blueprints
    from app.routes import main

    app.register_blueprint(main)

    return app
