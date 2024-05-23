# CaroninhasBackES2

Projeto da disciplina Engenharia de Software 2 | Back-end | Universidade Federal Fluminense | 2020.2

## Configurando ambiente de desenvolvimento

1. Baixar e instalar **Python 3.10**
	- No **Windows**, baixar e instalar pelo executável no [site](https://www.python.org/downloads/).
		
	- No **Ubuntu**, instalar pelo comando do terminal:
		```shell
		>> sudo apt-get install python3.10
		```

2. Criar ambiente virtual
	- No **Windows**:
		```shell
		>> py -m venv .venv
		```
		
	- No **Ubuntu**:
		```shell
		>> python3 -m venv .venv
		```

3. Ativar ambiente virtual. Sempre ativar quando ligar a máquina e iniciar o desenvolvimento.

	- No **Windows**:
		```shell
		>> .\.venv/Scripts/activate
		```

	- No **Ubuntu**:
		```shell
		>> source .venv/bin/activate
		```

4. Caso esteja no Windows, trocar politica de segurança do Windows, se necessário (executar comando abaixo no powershell como administrador):
	```shell
	>> Set-ExecutionPolicy AllSigned
	```

5. Instalar dependencies no venv.
	```shell
	>> pip install -r requirements.txt
	```

6. Baixar e instalar o SGBD **PostgreSQL**.
	- No **Windows**, baixar e instalar pelo executável no [site](https://www.postgresql.org/download/windows/).

	- No **Ubuntu**, executar os comandos:
		```shell
		>> sudo apt update
		>> sudo apt install postgresql
		```

7. Criar um database para a aplicação.
	- Se o PostgreSQL tiver sido instalado no **Windows**, isso pode ser feito pelo PGAdmin ou por qualquer outro programa administrador de banco de dados (ex. DBeaver.)
	- Se o PostgreSQL tiver sido instalado no **Ubuntu**, isso pode ser feito via terminal ao trocar para o usuário padrão postgres, criar um novo database via comando no terminal:
		```shell
		>> su - postgres  # troca para usuário padrão postgres
		>> createdb YourDatabaseName  # cria database
		```

8. No **Ubuntu**, para alterar a senha padrão ("postgres") do usuário padrão ("postgres"), basta aplicar os comandos:
	```
	>> sudo -u postgres psql  # vai abrir o terminal do psql
	postgres=# \password postgres
	Enter new password: YourPassword
	postgres=# \q
	>>
	```

9. É recomendável que o database seja conectado num programa administrador de banco de dados, para facilitar o desenvolvimento e depuração da aplicação e do banco. Recomenda-se o **DBeaver**:
	1. Apertar Ctrl+Shift+N.
	2. Selecionar PostgreSQL.
	3. Preencher dados da conexão Host: localhost, Porta: 5432 (porta padrão se não foi alterada), Banco de dados: YourDatabaseName, Nome de usuário: postgres (padrão se não foi alterado), Senha: YourPassword.
	4. Clicar em testar conexão e, caso não haja erros, clicar em concluir

10. **Para usuários do WSL**: No caso de ter instalado o **PostgreSQL no WSL** e o **Dbeaver no Windows**, basta preencher os dados de conexão do Dbeaver da forma descrita no item acima, como se o PostgreSQL estivesse no Windows (localhost pode ser usado para programas rodando no WSL que podem ser acessados do Windows). Talvez seja somente necessário permitir conexões TCP no WSL2 e reiniciar o postgres através dos comandos (Ubuntu):
	```shell
	>> sudo ufw allow 5432/tcp  # Deve aparecer algo como "Rules updated" e/ou "Rules updated (v6)"
	>> sudo service postgresql restar
	```

11. Terminando a configuração, criar um arquivo credentials.env para armazenar variáveis de ambiente e outras informações sensíveis. 

12. Adicionar variável de ambiente *DB_URI* em credentials.env contendo o link do database criado
	```
	DB_URI=postgresql+psycopg2://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName
	```

8. Adicionar variável de ambiente *HASH_SECRET_KEY* em credentials.env contendo a chave usada para fazer o hash. Exemplo:
	```
	HASH_SECRET_KEY=chavesecreta123
	```