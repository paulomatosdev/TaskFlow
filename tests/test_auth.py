import pytest

from app.models import User

USUARIO = {"name": "Ana", "email": "ana@exemplo.com",
           "password": "senha1234", "confirm_password": "senha1234"}
LOGIN_INVALIDO = "E-mail ou senha inválidos."


def cadastrar(client, **dados):
    return client.post("/register", json={**USUARIO, **dados})


def entrar(client, email="ana@exemplo.com", password="senha1234"):
    return client.post("/login", json={"email": email, "password": password})


def total_usuarios(db):
    return db.session.query(User).count()


@pytest.fixture
def usuario(client):
    cadastrar(client)


def test_cadastro_cria_usuario(client, db):
    resposta = cadastrar(client, name="  Ana  ", email="  ANA@Exemplo.com ")
    corpo = resposta.get_json()
    assert resposta.status_code == 201 and corpo["status"] == "ok"
    assert corpo["user"]["email"] == "ana@exemplo.com" and corpo["user"]["name"] == "Ana"
    assert "password" not in str(corpo)  # nunca devolve senha nem hash
    assert db.session.scalar(db.select(User)).check_password("senha1234")


def test_cadastro_email_duplicado(client, db, usuario):
    resposta = cadastrar(client, email="ANA@exemplo.com")
    assert resposta.status_code == 400
    assert resposta.get_json()["errors"]["email"] == ["Este e-mail já está cadastrado."]
    assert total_usuarios(db) == 1


@pytest.mark.parametrize("dados, campo", [
    ({"confirm_password": "outra1234"}, "confirm_password"),
    ({"password": "curta", "confirm_password": "curta"}, "password"),
    ({"email": "nao-e-email"}, "email"),
    ({"name": ""}, "name"),
    ({"name": "   "}, "name"),
])
def test_cadastro_invalido_nao_cria_usuario(client, db, dados, campo):
    resposta = cadastrar(client, **dados)
    assert resposta.status_code == 400 and campo in resposta.get_json()["errors"]
    assert total_usuarios(db) == 0


def test_cadastro_sem_json_retorna_415(client, db):
    assert client.post("/register", data=USUARIO).status_code == 415
    assert total_usuarios(db) == 0


def test_register_so_aceita_post(client):
    assert client.get("/register").status_code == 405


def test_login_valido(client, usuario):
    resposta = entrar(client, email="  ANA@exemplo.com")
    assert resposta.status_code == 200
    assert resposta.get_json()["user"]["email"] == "ana@exemplo.com"


@pytest.mark.parametrize("email, senha", [
    ("ana@exemplo.com", "errada123"), ("ninguem@exemplo.com", "senha1234")])
def test_login_invalido_mesma_mensagem(client, usuario, email, senha):
    resposta = entrar(client, email=email, password=senha)
    assert resposta.status_code == 401 and resposta.get_json()["message"] == LOGIN_INVALIDO


def test_login_campos_vazios(client):
    resposta = client.post("/login", json={})
    assert resposta.status_code == 400
    assert {"email", "password"} <= resposta.get_json()["errors"].keys()


def test_me_sem_login_retorna_401(client):
    resposta = client.get("/me")
    assert resposta.status_code == 401 and resposta.get_json()["status"] == "error"


def test_me_depois_do_login(client, usuario):
    entrar(client)
    resposta = client.get("/me")
    assert resposta.status_code == 200 and resposta.get_json()["user"]["name"] == "Ana"


def test_logout_encerra_sessao(client, usuario):
    entrar(client)
    assert client.post("/logout", json={}).status_code == 200
    assert client.get("/me").status_code == 401


def test_logout_sem_login_retorna_401(client):
    assert client.post("/logout", json={}).status_code == 401
