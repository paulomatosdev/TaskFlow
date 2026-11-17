from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Task, User


def criar_usuario(db, email="ana@exemplo.com"):
    user = User(name="Ana", email=email, password_hash="hash")
    db.session.add(user)
    db.session.commit()
    return user


def test_criar_usuario(db):
    user = criar_usuario(db)
    assert user.id is not None
    assert user.created_at is not None
    assert repr(user) == "<User ana@exemplo.com>"


def test_email_deve_ser_unico(db):
    criar_usuario(db)
    db.session.add(
        User(name="Outra", email="ana@exemplo.com", password_hash="x")
    )
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_criar_tarefa_com_valores_padrao(db):
    user = criar_usuario(db)
    task = Task(title="Estudar Flask", user=user)
    db.session.add(task)
    db.session.commit()

    assert task.priority == "media"
    assert task.status == "pendente"
    assert task.description is None
    assert task.created_at is not None
    assert task.updated_at is not None
    assert repr(task) == "<Task 'Estudar Flask'>"


def test_relacionamento_usuario_tarefas(db):
    user = criar_usuario(db)
    db.session.add_all([
        Task(title="A", user=user, due_date=date(2026, 12, 1)),
        Task(title="B", user=user, category="trabalho"),
    ])
    db.session.commit()

    assert len(user.tasks) == 2
    assert user.tasks[0].user is user


def test_tarefa_sem_usuario_falha(db):
    db.session.add(Task(title="Órfã"))
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_apagar_usuario_apaga_tarefas(db):
    user = criar_usuario(db)
    db.session.add(Task(title="A", user=user))
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    assert db.session.query(Task).count() == 0
