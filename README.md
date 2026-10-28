# TaskFlow

Base inicial de um sistema web usando Python e Flask.

## Executar localmente

No PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

A aplicação ficará disponível em `http://127.0.0.1:5000`.

## Rotas iniciais

- `GET /`: confirma que a API está funcionando.
- `GET /health`: endpoint simples para monitoramento.

## Próximos passos sugeridos

1. Adicionar configuração por ambiente e variáveis no `.env`.
2. Definir os modelos de dados e integrar um banco, como SQLite.
3. Criar autenticação e separar as áreas públicas e privadas.
4. Adicionar testes automatizados para as rotas.
