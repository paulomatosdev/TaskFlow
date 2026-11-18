"""Testes de segurança: CSRF, duplicidade de cadastro e ciclo de sessão.

Fixtures (tests/conftest.py):
- client: envia um token CSRF válido (obtido em /csrf-token) em toda requisição;
- client_sem_csrf: não envia token nenhum.
"""
import pytest

from app.auth.routes import EMAIL_DUPLICADO
from tests.test_auth import USUARIO, cadastrar, entrar, total_usuarios

CREDENCIAIS = {"email": USUARIO["email"], "password": USUARIO["password"]}
ROTAS_PROTEGIDAS = ["/register", "/login", "/logout"]


def token_de(client):
    return client.get("/csrf-token").get_json()["csrf_token"]


def assert_erro_csrf(resposta):
    corpo = resposta.get_json()
    assert resposta.status_code == 400 and resposta.is_json
    assert corpo["status"] == "error" and "csrf_token" in corpo["errors"]


# --- Cenários da tarefa ------------------------------------------------------

def test_solicitar_token_csrf_retorna_200(client_sem_csrf):
    resposta = client_sem_csrf.get("/csrf-token")
    corpo = resposta.get_json()
    assert resposta.status_code == 200 and corpo["status"] == "ok"
    assert isinstance(corpo["csrf_token"], str) and corpo["csrf_token"]


def test_cadastro_sem_token_retorna_400(client_sem_csrf, db):
    assert_erro_csrf(client_sem_csrf.post("/register", json=USUARIO))
    assert total_usuarios(db) == 0


def test_login_com_token_invalido_retorna_400(client_sem_csrf, usuario):
    token_de(client_sem_csrf)  # a sessão tem um token, mas enviamos outro
    resposta = client_sem_csrf.post("/login", json=CREDENCIAIS,
                                    headers={"X-CSRFToken": "token-forjado"})
    assert_erro_csrf(resposta)
    assert client_sem_csrf.get("/me").status_code == 401  # não autenticou


def test_token_de_outra_sessao_retorna_400(app, client_sem_csrf, db):
    token_alheio = token_de(app.test_client())  # token válido, mas de outra sessão
    token_de(client_sem_csrf)
    resposta = client_sem_csrf.post("/register", json=USUARIO,
                                    headers={"X-CSRFToken": token_alheio})
    assert_erro_csrf(resposta)
    assert total_usuarios(db) == 0


def test_cadastro_com_token_valido_retorna_201(client, db):
    resposta = cadastrar(client)
    assert resposta.status_code == 201 and resposta.get_json()["status"] == "ok"
    assert total_usuarios(db) == 1


def test_cadastro_duplicado_retorna_409(client, db, usuario):
    resposta = cadastrar(client)
    corpo = resposta.get_json()
    assert resposta.status_code == 409 and corpo["status"] == "error"
    assert corpo["errors"]["email"] == [EMAIL_DUPLICADO]
    assert total_usuarios(db) == 1


def test_me_sem_login_retorna_401(client):
    resposta = client.get("/me")
    assert resposta.status_code == 401 and resposta.get_json()["status"] == "error"


def test_me_autenticado_retorna_200(client, usuario):
    assert entrar(client).status_code == 200
    resposta = client.get("/me")
    assert resposta.status_code == 200
    assert resposta.get_json()["user"]["email"] == USUARIO["email"]


def test_logout_sem_token_retorna_400_e_mantem_sessao(client, usuario):
    entrar(client)
    del client.environ_base["HTTP_X_CSRFTOKEN"]  # mesma sessão, sem o header
    assert_erro_csrf(client.post("/logout", json={}))
    assert client.get("/me").status_code == 200


def test_me_apos_logout_valido_retorna_401(client, usuario):
    entrar(client)
    assert client.post("/logout", json={}).status_code == 200
    assert client.get("/me").status_code == 401


# --- Cobertura extra ----------------------------------------------------------

def test_protecao_csrf_global_ativa(app):
    assert app.config.get("WTF_CSRF_ENABLED", True) is True
    assert "csrf" in app.extensions


@pytest.mark.parametrize("url", ROTAS_PROTEGIDAS)
def test_rotas_protegidas_sem_token_retornam_400(client_sem_csrf, url):
    assert_erro_csrf(client_sem_csrf.post(url, json=USUARIO))


@pytest.mark.parametrize("url", ROTAS_PROTEGIDAS)
def test_rotas_protegidas_com_token_invalido_retornam_400(client_sem_csrf, url):
    token_de(client_sem_csrf)
    assert_erro_csrf(client_sem_csrf.post(url, json=USUARIO,
                                          headers={"X-CSRFToken": "token-forjado"}))


def test_login_sem_token_nao_autentica(client_sem_csrf, usuario):
    assert_erro_csrf(client_sem_csrf.post("/login", json=CREDENCIAIS))
    assert client_sem_csrf.get("/me").status_code == 401


def test_csrf_vem_antes_da_checagem_de_json(client_sem_csrf):
    # sem token, mesmo um corpo não JSON recebe 400 (CSRF) e não 415
    assert_erro_csrf(client_sem_csrf.post("/register", data=USUARIO))
