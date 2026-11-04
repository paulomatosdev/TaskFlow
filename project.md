# TaskFlow — Gerenciador inteligente de tarefas

## Visão geral

O TaskFlow é um sistema web para organizar tarefas pessoais e profissionais de
forma simples, visual e produtiva. O projeto foi pensado para evoluir do nível
iniciante ao intermediário, demonstrando a construção de uma aplicação Flask
com autenticação, persistência de dados e operações CRUD.

## Objetivos

- Centralizar tarefas pessoais e profissionais em um único lugar.
- Permitir o acompanhamento do progresso por meio de um quadro Kanban.
- Facilitar a priorização de atividades e o controle de prazos.
- Exibir indicadores que ajudem o usuário a acompanhar sua produtividade.
- Praticar conceitos de rotas, templates, banco de dados e autenticação.

## Funcionalidades

### Usuários

- Cadastro de novos usuários.
- Login e logout.
- Senhas armazenadas de forma segura.
- Acesso restrito às tarefas do usuário autenticado.

### Tarefas

Cada tarefa deve permitir o cadastro de:

- Título.
- Descrição.
- Prioridade.
- Prazo de conclusão.
- Categoria.
- Status.
- Data de criação e última atualização.

Operações disponíveis:

- Criar tarefas.
- Visualizar tarefas.
- Editar tarefas.
- Excluir tarefas.
- Alterar o status da tarefa.

### Quadro Kanban

As tarefas serão organizadas em três colunas:

1. **Pendente**
2. **Em andamento**
3. **Concluído**

Quando possível, a alteração de status poderá ser feita por meio de interação
visual, como arrastar e soltar, sem impedir a alteração por formulários
tradicionais.

### Filtros e produtividade

- Filtrar tarefas por status.
- Filtrar tarefas por prioridade.
- Filtrar tarefas por categoria.
- Buscar tarefas por título ou descrição.
- Exibir a quantidade de tarefas por status.
- Exibir tarefas atrasadas.
- Exibir tarefas concluídas no período selecionado.

## Tecnologias

- **Backend:** Python e Flask.
- **ORM:** Flask-SQLAlchemy / SQLAlchemy.
- **Banco de dados para desenvolvimento:** SQLite.
- **Banco de dados para produção:** PostgreSQL.
- **Frontend:** HTML, CSS e Bootstrap ou Tailwind CSS.
- **Autenticação:** Flask-Login.
- **Formulários e validação:** Flask-WTF e WTForms.
- **Versionamento:** Git.

## Modelo de dados inicial

### User

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Identificador único |
| `name` | String | Nome do usuário |
| `email` | String | E-mail único do usuário |
| `password_hash` | String | Senha protegida por hash |
| `created_at` | DateTime | Data de criação da conta |

### Task

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Identificador único |
| `title` | String | Título da tarefa |
| `description` | Text | Detalhes da tarefa |
| `priority` | String | Baixa, média ou alta |
| `due_date` | Date | Prazo de conclusão |
| `category` | String | Categoria da tarefa |
| `status` | String | Pendente, em andamento ou concluído |
| `user_id` | Integer | Usuário proprietário da tarefa |
| `created_at` | DateTime | Data de criação |
| `updated_at` | DateTime | Data da última atualização |

Relacionamento:

- Um usuário pode possuir várias tarefas.
- Cada tarefa pertence a um único usuário.

## Rotas esperadas

### Autenticação

- `GET, POST /register` — cadastro de usuário.
- `GET, POST /login` — login.
- `GET /logout` — logout.

### Tarefas

- `GET /` — página inicial ou redirecionamento para o painel.
- `GET /dashboard` — painel principal.
- `GET, POST /tasks/new` — criação de tarefa.
- `GET, POST /tasks/<id>/edit` — edição de tarefa.
- `POST /tasks/<id>/delete` — exclusão de tarefa.
- `POST /tasks/<id>/status` — alteração de status.

## Organização sugerida

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
├── run.py
├── requirements.txt
└── project.md
```

## Requisitos de segurança

- Usar hash de senha, nunca armazenar senhas em texto puro.
- Validar os dados recebidos nos formulários.
- Garantir que o usuário só acesse e altere suas próprias tarefas.
- Proteger formulários contra CSRF.
- Usar variáveis de ambiente para configurações sensíveis.
- Desabilitar o modo de debug em produção.

## Etapas de implementação

1. Criar e configurar o ambiente Flask.
2. Configurar SQLAlchemy e as variáveis de ambiente.
3. Criar os modelos `User` e `Task`.
4. Implementar cadastro, login e logout.
5. Implementar o CRUD de tarefas.
6. Criar o painel com o quadro Kanban.
7. Adicionar filtros e indicadores de produtividade.
8. Aplicar o layout responsivo com Bootstrap ou Tailwind CSS.
9. Criar testes para autenticação, tarefas e permissões.
10. Configurar PostgreSQL e preparar o deploy.

## Critérios de conclusão

O projeto será considerado funcional quando:

- Um usuário puder criar uma conta e acessar o sistema.
- Cada usuário visualizar apenas suas próprias tarefas.
- O CRUD de tarefas estiver funcionando.
- As tarefas puderem mudar entre os três status do Kanban.
- Os filtros retornarem resultados corretos.
- O painel exibir indicadores básicos de produtividade.
- Senhas, permissões e formulários estiverem protegidos.
- A aplicação possuir testes para os fluxos principais.

## O que o projeto demonstra

- Criação de rotas com Flask.
- Renderização de templates.
- Integração com banco de dados.
- Modelagem de relacionamentos.
- Autenticação e controle de acesso.
- Operações CRUD.
- Validação de formulários.
- Construção de uma interface web responsiva.
- Organização de um projeto Python com estrutura modular.
