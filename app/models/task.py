from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    priority: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    due_date: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    created_at: Mapped[str] = mapped_column()
    updated_at: Mapped[str] = mapped_column()




    



