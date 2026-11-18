from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Task, User


def criar_usuario(db, email="ana@exemplo.com", senha="senha123"):
    user = User(name="Ana", email=email)
    user.set_password(senha)
    db.session.add(user)
    db.session.commit()
    return user


def commit_falha(db, *objetos):
    db.session.add_all(objetos)
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_criar_usuario(db):
    user = criar_usuario(db)
    assert user.id is not None and user.created_at is not None
    assert repr(user) == "<User ana@exemplo.com>"


def test_senha_e_salva_como_hash(db):
    user = criar_usuario(db, senha="minhasenha123")
    assert user._password_hash.startswith("scrypt:")
    assert user.check_password("minhasenha123") is True
    assert user.check_password("senhaerrada") is False


def test_mesma_senha_gera_hashes_diferentes(db):
    a = criar_usuario(db, email="a@exemplo.com", senha="igual")
    b = criar_usuario(db, email="b@exemplo.com", senha="igual")
    assert a._password_hash != b._password_hash


def test_usuario_sem_senha_falha(db):
    commit_falha(db, User(name="Sem senha", email="x@exemplo.com"))


def test_email_deve_ser_unico(db):
    criar_usuario(db)
    outro = User(name="Outra", email="ana@exemplo.com")
    outro.set_password("x")
    commit_falha(db, outro)


def test_user_loader_e_flask_login(app, db):
    user = criar_usuario(db)
    carregar = app.login_manager._user_callback
    assert carregar(str(user.id)) is user and carregar("9999") is None
    assert user.is_authenticated and user.is_active and user.get_id() == str(user.id)


def test_criar_tarefa_com_valores_padrao(db):
    task = Task(title="Estudar Flask", user=criar_usuario(db))
    db.session.add(task)
    db.session.commit()
    assert (task.priority, task.status, task.description) == ("media", "pendente", None)
    assert task.created_at is not None and task.updated_at is not None
    assert repr(task) == "<Task 'Estudar Flask'>"


def test_relacionamento_usuario_tarefas(db):
    user = criar_usuario(db)
    db.session.add_all([Task(title="A", user=user, due_date=date(2026, 12, 1)),
                        Task(title="B", user=user, category="trabalho")])
    db.session.commit()
    assert len(user.tasks) == 2 and user.tasks[0].user is user


def test_tarefa_sem_usuario_falha(db):
    commit_falha(db, Task(title="Órfã"))


def test_apagar_usuario_apaga_tarefas(db):
    user = criar_usuario(db)
    db.session.add(Task(title="A", user=user))
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    assert db.session.query(Task).count() == 0
