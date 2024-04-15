# CaroninhasBackES2

Projeto da disciplina Engenharia de Software 2 | Back-end | Universidade Federal Fluminense | 2020.2

## Configurando ambiente de desenvolvimento

1. Baixar e instalar **Python 3.12.2**

2. Baixar, instalar e criar um database no **PostgreSQL**

3. Criar ambiente virtual
	- No **Windows**:
		>> `py -m venv .venv`
		
	- No **Linux**:
		>> `python3.12 -m venv .venv`

4. Ativar ambiente virtual. Sempre ativar quando ligar a máquina e iniciar o desenvolvimento
	- No **Windows**:
		>> `.\.venv/Scripts/activate`

	- No **Linux**:
		>> `source .venv/bin/activate`

5. Caso esteja no Windows, trocar politica de segurança do Windows, se necessário (executar no powershell como adm)
	- No **Windows**:
		>> `Set-ExecutionPolicy AllSigned`

6. Instalar dependencies no venv
	>> `pip install -r requirements.txt`

7. Adicionar variável de ambiente *DB_URI* em credentials.env contendo o link do database criado
	- `DB_URI=postgresql+psycopg2://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName`

8. Adicionar variável de ambiente *HASH_SECRET_KEY* em credentials.env contendo a chave usada para fazer o hash. Exemplo:
	- `HASH_SECRET_KEY=chavesecreta123`