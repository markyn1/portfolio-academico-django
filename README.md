# Portfólio Acadêmico

Aplicação web desenvolvida com Django para o contexto **Portfólio Acadêmico**: cadastro e gestão de projetos de alunos, com descrição, tecnologias utilizadas, integrantes e status de desenvolvimento.

**Disciplina:** Programação Web I — IFSE Campus Lagarto  
**Professor:** Jean Louis

## Integrantes do grupo

- Marcos Henrique Garcia Pereira
- Márcio Pierre Santos Monteiro

## Tecnologias utilizadas

- Python 3
- Django 6
- HTML / CSS
- SQLite

## Estrutura do projeto

- `accounts` — autenticação, perfil e cadastro de usuários
- `portfolio` — entidade principal `Projeto`, CRUD, busca e relacionamentos
- `core` — configurações e URLs raiz
- `templates/base.html` — layout e navegação compartilhados

## Como executar o projeto

### 1. Clonar e entrar na pasta

```bash
cd portfolio-academico-django
```

### 2. Ambiente virtual e dependências

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Banco de dados e dados de exemplo

As migrações já estão versionadas no repositório. **Execute nesta ordem** (obrigatório):

```bash
python manage.py migrate
python manage.py loaddata dados_exemplo
```

**Usuários de demonstração (após `loaddata`):**

Todos usam a mesma senha: **`demo123`**

| Usuário          | Nome              | E-mail                    |
|------------------|-------------------|---------------------------|
| `demo`           | Usuário Demonstração | demo@example.com       |
| `ana.silva`      | Ana Silva         | ana.silva@example.com     |
| `joao.santos`    | João Santos       | joao.santos@example.com   |
| `maria.oliveira` | Maria Oliveira    | maria.oliveira@example.com |

A fixture inclui 4 perfis completos, 10 tecnologias e 8 projetos com todos os campos preenchidos.

### 4. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

- Não autenticado → redireciona para login
- Após login → listagem de projetos em `/portfolio/`

## Requisitos funcionais implementados

| RF | Descrição | Implementação |
|----|-----------|---------------|
| RF01 | Autenticação (nome, e-mail, senha, login/logout Django) | `RegistroForm`, `LoginView`, `LogoutView` em `accounts/` |
| RF02 | Perfil com edição | `perfil_view`, `editar_perfil_view`, model `Profile` |
| RF03 | Modelo central (≥5 campos) | Model `Projeto` em `portfolio/models.py` |
| RF04 | CRUD completo (autenticado) | Views em `portfolio/views.py` + templates |
| RF05 | Relacionamento FK/M2M na interface | `autor` → User; `tecnologias` → Tecnologia (badges) |
| RF06 | Forms com validação personalizada | `clean_*` em `ProjetoForm` e `RegistroForm` |
| RF07 | Busca/filtro GET na listagem | Parâmetro `busca` em `lista_projetos_view` |
| RF08 | `@login_required` e edição só pelo autor | Decorators + checagem `projeto.autor` |
| RF09 | `base.html`, navegação, Django Messages | `templates/base.html` + `messages` nas views |
| RF10 | Migrations e dados de exemplo | `migrations/` + `loaddata dados_exemplo` |

## Capturas de tela

**Login** (`/accounts/login/`)

![Tela de login](docs/screenshots/login.png)

**Listagem de projetos** (`/portfolio/`)

![Listagem de projetos](docs/screenshots/lista-projetos.png)

## Observações

- O cadastro solicita **nome de usuário** além de nome, e-mail e senha (padrão do modelo `User` do Django).
- O arquivo `db.sqlite3` não deve ser versionado (está no `.gitignore`); use `migrate` + `loaddata` em cada máquina.
- Para gerar `requirements.txt` atualizado: `pip freeze > requirements.txt`
