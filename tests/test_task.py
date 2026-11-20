import pytest

from app.models import User
from app.models.task import Task
from tests.test_auth import USUARIO, entrar

URL_CRIAR = "/tasks"


@pytest.fixture
def cliente_logado(client, usuario):
    entrar(client)
    return client


def criar(client, **dados):
    return client.post(URL_CRIAR, json={"title": "Estudar Flask", **dados})


def test_criar_tarefa_logado(cliente_logado, db):
    resposta = criar(cliente_logado)
    assert resposta.status_code == 201
    assert resposta.get_json()["task"]["status"] == "pendente"

    task = db.session.scalar(db.select(Task))
    ana = db.session.scalar(db.select(User).filter_by(email=USUARIO["email"]))
    assert task.user_id == ana.id


@pytest.mark.parametrize("titulo", ["", "   "])
def test_titulo_vazio_retorna_400(cliente_logado, titulo):
    resposta = criar(cliente_logado, title=titulo)
    assert resposta.status_code == 400 and "title" in resposta.get_json()["errors"]


def test_criar_sem_login_retorna_401(client):
    assert criar(client).status_code == 401


def test_data_em_formato_errado_retorna_400(cliente_logado):
    resposta = criar(cliente_logado, due_date="31/12/2026")
    assert resposta.status_code == 400 and "due_date" in resposta.get_json()["errors"]
