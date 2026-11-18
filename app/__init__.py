from flask import Flask

from app.extensions import db, login_manager, migrate
from config import config_by_name


def create_app(config_name="development"):
    if config_name not in config_by_name:
        raise ValueError(f"Configuração desconhecida: {config_name!r}")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY não definida (veja o arquivo .env.example).")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models  # noqa: F401  (registra os modelos no db.metadata)
    from app.auth import auth
    from app.routes import main

    for blueprint in (main, auth):
        app.register_blueprint(blueprint)
    return app
