from flask import Flask

from config import config_by_name


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

    app.register_blueprint(main)
    return app
