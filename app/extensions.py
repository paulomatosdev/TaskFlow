from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Instâncias únicas das extensões, criadas sem app.
# São ligadas ao app dentro da factory com init_app(app).
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
