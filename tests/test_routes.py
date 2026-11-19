import pytest


@pytest.mark.parametrize("url", ["/", "/health", "/about", "/contact"])
def test_rotas_respondem_ok(client, url):
    resposta = client.get(url)
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


@pytest.mark.parametrize("url", ["/tasks/abc", "/nao-existe"])
def test_url_invalida_retorna_404(client, url):
    assert client.get(url).status_code == 404

def test_recurso_inexistente_retorna_404(client):
    resposta = client.get("/tasks/9999")
    assert resposta.status_code == 404
    assert resposta.get_json()["message"] == "Recurso não encontrado."
