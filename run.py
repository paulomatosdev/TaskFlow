import os

from app import create_app

# Chamamos a fábrica para gerar o nosso app configurado.
# O ambiente vem da variável APP_ENV (padrão: development).
app = create_app(os.environ.get("APP_ENV", "development"))

if __name__ == "__main__":
    app.run()
