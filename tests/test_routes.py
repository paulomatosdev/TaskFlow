import pytest


@pytest.mark.parametrize("url", ["/", "/health", "/about", "/contact"])
def test_rotas_respondem_ok(client, url):
    resposta = client.get(url)
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


@pytest.mark.parametrize("url", ["/tasks/abc", "/nao-existe"])
def test_url_invalida_retorna_404(client, url):
    assert client.get(url).status_code == 404


def test_url_inexistente_retorna_404_em_json(client):
    # /nao-existe nunca terá rota. Tarefa inexistente (/tasks/9999) é outro caso:
    # com @login_required, um client não logado recebe 401 antes de qualquer busca.
    resposta = client.get("/nao-existe")
    assert resposta.status_code == 404 and resposta.is_json
    assert resposta.get_json() == {"status": "error", "message": "Recurso não encontrado."}
