# TaskFlow — Gerenciador inteligente de tarefas

O TaskFlow é um sistema web para organizar tarefas pessoais e profissionais.
O projeto está sendo desenvolvido com Flask e evoluirá para uma aplicação com
autenticação, CRUD de tarefas, quadro Kanban e indicadores de produtividade.

## Status do projeto

Neste momento, o projeto possui uma base Flask funcional com:

- Factory `create_app`.
- Configuração por ambiente (`development`, `production` e `testing`) em
  `config.py`, com valores sensíveis lidos de variáveis de ambiente (`.env`).
- Banco de dados com Flask-SQLAlchemy e migrações com Flask-Migrate.
- Modelos `User` e `Task` com relacionamento um-para-muitos.
- Rotas `GET /`, `/health`, `/about`, `/contact` e `/tasks/<id>` (veja
  [Rotas disponíveis](#rotas-disponíveis)).
- Testes automatizados com pytest.

As funcionalidades de autenticação e gerenciamento de tarefas estão planejadas
para as próximas etapas.

## Funcionalidades planejadas

- Cadastro, login e logout de usuários.
- Tarefas com título, descrição, prioridade, prazo e categoria.
- Operações CRUD de tarefas.
- Quadro Kanban com os status:
  - Pendente
  - Em andamento
  - Concluído
- Filtros por status, prioridade e categoria.
- Busca por título ou descrição.
- Indicadores de produtividade e tarefas atrasadas.
- Controle de acesso às tarefas do usuário autenticado.

## Tecnologias

- Python
- Flask
- SQLAlchemy
- SQLite no desenvolvimento
- PostgreSQL em produção
- Bootstrap ou Tailwind CSS
- Flask-Login para autenticação
- Flask-WTF e WTForms para formulários e validação

## Pré-requisitos

- Python 3.10 ou superior
- PowerShell no Windows

## Instalação

Clone o repositório e entre na pasta do projeto:

```powershell
git clone https://github.com/paulomatosdev/TaskFlow.git
cd TaskFlow
```

Crie e ative o ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Configuração

As configurações sensíveis ficam em variáveis de ambiente, nunca no código.
Copie o arquivo de exemplo e preencha os valores:

```powershell
Copy-Item .env.example .env
```

| Variável       | Descrição                                        | Padrão                    |
| -------------- | ------------------------------------------------ | ------------------------- |
| `APP_ENV`      | Ambiente: `development` ou `production`.         | `development`             |
| `SECRET_KEY`   | Chave secreta do Flask. Obrigatória em produção. | —                         |
| `DATABASE_URL` | URL de conexão do banco de dados.                | SQLite em `instance/dados.db` |

Para gerar uma chave segura:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Em desenvolvimento, se `SECRET_KEY` não for definida, uma chave aleatória é
gerada a cada execução (as sessões são perdidas ao reiniciar). Em produção, a
aplicação não inicia sem `SECRET_KEY`.

## Banco de dados

O esquema do banco é controlado por migrações (pasta `migrations/`). Para
criar ou atualizar as tabelas:

```powershell
flask --app run db upgrade
```

Depois de alterar um modelo em `app/models/`, gere uma nova migração e
aplique-a:

```powershell
flask --app run db migrate -m "Descrição da alteração"
flask --app run db upgrade
```

> `db migrate` apenas **gera** o script da migração; as tabelas só são
> criadas ou alteradas no banco com `db upgrade`.

## Executar localmente

Com o ambiente virtual ativado:

```powershell
python run.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

## Rotas disponíveis

Todas as rotas respondem em JSON.

| Método | Rota              | Descrição                                       |
| ------ | ----------------- | ----------------------------------------------- |
| GET    | `/`               | Rota inicial; confirma que a API está no ar.    |
| GET    | `/health`         | Endpoint de saúde (`{"status": "ok"}`).         |
| GET    | `/about`          | Informações sobre o TaskFlow.                   |
| GET    | `/contact`        | Informações de contato.                         |
| GET    | `/tasks/<id>`     | Detalhes de uma tarefa (ainda simulado).        |

> **Observação:** `GET /tasks/<id>` ainda não consulta o banco de dados — apenas
> devolve uma mensagem com o número informado. O CRUD real de tarefas será
> implementado nas próximas etapas.

## Testes

Os testes usam um banco SQLite em memória (configuração `testing`), sem
afetar o banco de desenvolvimento. Com o ambiente virtual ativado:

```powershell
python -m pytest -v
```

| Arquivo                     | O que verifica                                          |
| --------------------------- | ------------------------------------------------------- |
| `tests/test_app.py`         | Factory, configuração e extensões registradas.          |
| `tests/test_routes.py`      | Respostas das rotas e erros 404.                        |
| `tests/test_models.py`      | Modelos, valores padrão, restrições e relacionamentos.  |
| `tests/test_migrations.py`  | Migrações aplicam/revertem e estão em dia com os modelos. |

## Estrutura atual

```text
TaskFlow/
├── app/
│   ├── __init__.py      # factory create_app
│   ├── extensions.py    # instâncias de SQLAlchemy e Migrate
│   ├── routes.py        # blueprint "main" com as rotas atuais
│   └── models/
│       ├── __init__.py  # exporta User e Task
│       ├── user.py
│       └── task.py
├── migrations/          # migrações do banco (Flask-Migrate / Alembic)
├── tests/               # testes automatizados (pytest)
│   ├── conftest.py      # fixtures app, client e db
│   └── test_*.py
├── .env.example         # modelo das variáveis de ambiente
├── .gitignore
├── config.py            # configurações por ambiente
├── project.md           # especificação completa do projeto
├── README.md
├── requirements.txt
└── run.py               # ponto de entrada da aplicação
```

O banco SQLite local fica em `instance/`, que é ignorada pelo Git.

O `.env` (com os valores reais) e a pasta `.venv` ficam fora do Git. Para
gerar um pacote ZIP somente com os arquivos versionados:

```powershell
git archive --format=zip -o TaskFlow.zip HEAD
```

## Estrutura planejada

```text
TaskFlow/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   ├── auth/
│   │   ├── routes.py
│   │   └── forms.py
│   ├── tasks/
│   │   ├── routes.py
│   │   └── forms.py
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
├── config.py
├── project.md
├── requirements.txt
└── run.py
```

## Próximas etapas

1. ~~Configurar a aplicação por ambiente e variáveis no `.env`.~~ ✔
2. ~~Integrar SQLAlchemy e criar os modelos `User` e `Task`.~~ ✔
3. Implementar cadastro, login, logout e controle de acesso.
4. Implementar o CRUD de tarefas.
5. Criar o painel e o quadro Kanban.
6. Adicionar filtros e indicadores de produtividade.
7. Criar testes para autenticação, tarefas e permissões.
8. Preparar o uso com PostgreSQL e o deploy.

## Segurança

- Senhas devem ser armazenadas somente com hash.
- Formulários devem ser protegidos contra CSRF.
- Cada usuário deve acessar apenas as próprias tarefas.
- Configurações sensíveis devem ser definidas por variáveis de ambiente.
- O modo debug não deve ser usado em produção.

Consulte o [project.md](project.md) para a especificação completa, o modelo de
dados, as rotas planejadas e os critérios de conclusão.
