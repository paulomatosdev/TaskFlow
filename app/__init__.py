from flask import Flask


# Application factory
def create_app(config_name="development"):
    app = Flask(__name__)

    # Configurações do app (podem mudar dependendo do ambiente)
    if config_name == "development":
        app.config["DEBUG"] = True
        app.config["SECRET_KEY"] = "chave-secreta-dev"
    else:
        app.config["DEBUG"] = False
        app.config["SECRET_KEY"] = "chave-super-segura-producao"

    from app.routes import main

    app.register_blueprint(main)
    return app
