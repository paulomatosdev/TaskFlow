from app import create_app

# Chamamos a fábrica para gerar o nosso app configurado
app = create_app("development")

if __name__ == "__main__":
  app.run()