from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Instância única do SQLAlchemy, criada sem app.
# É ligada ao app dentro da factory com db.init_app(app).
db = SQLAlchemy(model_class=Base)
