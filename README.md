# Portfólio Acadêmico

Aplicação web desenvolvida com Django para gerenciamento de projetos acadêmicos, permitindo cadastro de usuários, autenticação, edição de perfil e CRUD de projetos.

## Integrantes
- Márcio Pierre Santos Monteiro 
- Marcos Henrique Garcia Pereira

## Tecnologias utilizadas
- Python
- Django
- HTML
- CSS
- SQLite

## Funcionalidades implementadas
- Cadastro de usuário
- Login e logout
- Perfil do usuário com edição
- Cadastro de projetos
- Listagem de projetos
- Edição e exclusão de projetos
- Controle de acesso por usuário
- Busca de projetos
- Relacionamento com tecnologias

## Como executar o projeto

1. Clone o repositório ou extraia a pasta do projeto.
2. Crie e ative o ambiente virtual.
3. Instale as dependências.
4. Execute as migrações.
5. Inicie o servidor local.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```