import pytest


@pytest.mark.parametrize(
    "url", ["/", "/health", "/about", "/contact", "/tasks/1"]
)
def test_rotas_respondem_ok(client, url):
    resposta = client.get(url)
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


def test_get_task_usa_o_id(client):
    resposta = client.get("/tasks/42")
    assert "42" in resposta.get_json()["message"]


def test_task_id_invalido_retorna_404(client):
    resposta = client.get("/tasks/abc")
    assert resposta.status_code == 404


def test_rota_inexistente_retorna_404(client):
    assert client.get("/nao-existe").status_code == 404
