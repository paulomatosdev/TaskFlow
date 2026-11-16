from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Application factory
def create_app(config_name="development"):
    app = Flask(__name__)

    # Configurações do app carregadas de config.py / variáveis de ambiente
    if config_name not in config_by_name:
        raise ValueError(f"Configuração desconhecida: {config_name!r}")
    app.config.from_object(config_by_name[config_name])

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY não definida. Configure a variável de ambiente "
            "SECRET_KEY (veja o arquivo .env.example)."
        )

    from app.routes import main

    
    class Base(DeclarativeBase):
        pass

    db = SQLAlchemy(model_class=Base)
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"

    db.init_app(app)

    app.register_blueprint(main)
    return app
