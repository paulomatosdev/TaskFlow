# TaskFlow — Gerenciador inteligente de tarefas

O TaskFlow é um sistema web para organizar tarefas pessoais e profissionais.
O projeto está sendo desenvolvido com Flask e evoluirá para uma aplicação com
autenticação, CRUD de tarefas, quadro Kanban e indicadores de produtividade.

## Status do projeto

Neste momento, o projeto possui uma base Flask funcional com:

- Factory `create_app`.
- Rota inicial (`GET /`).
- Endpoint de saúde (`GET /health`).
- Ambiente virtual e dependências iniciais configurados.

As funcionalidades de autenticação, banco de dados e gerenciamento de tarefas
estão planejadas para as próximas etapas.

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

## Executar localmente

Com o ambiente virtual ativado:

```powershell
python run.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

Para verificar se a aplicação está respondendo, acesse:

- `GET /` — rota inicial.
- `GET /health` — endpoint de saúde.

## Estrutura planejada

```text
TaskFlow/
├── app/
│   ├── __init__.py
│   ├── models.py
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

1. Configurar a aplicação por ambiente e variáveis no `.env`.
2. Integrar SQLAlchemy e criar os modelos `User` e `Task`.
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
