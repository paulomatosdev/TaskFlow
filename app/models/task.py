from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))