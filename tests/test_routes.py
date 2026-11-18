import pytest


@pytest.mark.parametrize("url", ["/", "/health", "/about", "/contact", "/tasks/1"])
def test_rotas_respondem_ok(client, url):
    resposta = client.get(url)
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


def test_get_task_usa_o_id(client):
    assert "42" in client.get("/tasks/42").get_json()["message"]


@pytest.mark.parametrize("url", ["/tasks/abc", "/nao-existe"])
def test_url_invalida_retorna_404(client, url):
    assert client.get(url).status_code == 404
