import os
import sys
from fastapi.testclient import TestClient
import pytest
from dotenv import load_dotenv
load_dotenv(dotenv_path="../credentials.env")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from datetime import datetime
from app.models.user_oop import UserBase, UserCreate, UserUpdate
from app.models.veiculo_oop import MotoristaVeiculoModel
from app.models.general_oop import BasicResponse
from app.models.token_oop import TokenModel
from app.models.router_tags import RouterTags
from app.models.user_oop import UserWithoutMotorista, UserModel, MotoristaWithUser
from faker import Faker

fake = Faker()

def generate_random_user():
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "cpf": fake.numerify('###########'),
        "birthdate": fake.date_time_between(start_date='-50y', end_date='-18y').strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "iduff": fake.numerify('##########'),
        "phone": fake.numerify('###########'),
        "password": fake.password()
    }
user_data = generate_random_user()

@pytest.fixture
def test_client():
    return TestClient(app)

def test_create_user(test_client):
    # Envia uma requisição POST para criar o usuário
    response = test_client.post("/users/create", json=user_data)

    # Verifica se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verifica se os dados do usuário na resposta correspondem aos dados enviados
    assert response.json()["email"] == user_data["email"]
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["cpf"] == user_data["cpf"]
    assert response.json()["birthdate"] == user_data["birthdate"][:-7]

    # Verifica se o usuário foi criado com sucesso
    assert "id" in response.json()
    assert response.json()["active"] == True
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Foi criado um novo Usuario: Segue os dados:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")


def test_create_user_error_email_existe(test_client):

    # Envia uma requisição POST para criar o usuário
    response = test_client.post("/users/create", json=user_data)

    assert response.status_code >= 400 and response.status_code < 500
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Não foi possível criar o usuário. Pelo motivo de:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")

def test_login_sucesso(test_client):
        response = test_client.post("/token", data={"username": user_data["email"], "password": user_data["password"]})
    
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        print(f"\n\n\n#######################################\nTeste realizado com sucesso! Foi logado com sucesso! Segue os dados:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")

def test_login_senha_incorreta(test_client):
    response = test_client.post("/token", data={"username": user_data["email"], "password": "senha_incorreta"})
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Não foi possível logar. Pelo motivo de:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")

def test_login_email_incorreto(test_client):
    response = test_client.post("/token", data={"username": "email_incorreto", "password": user_data["password"]})
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Não foi possível logar. Pelo motivo de:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")

def test_read_my_user(test_client):
    response = test_client.post("/token", data={"username": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/users/me", headers=headers)
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Usuario:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")

def test_read_my_user_nao_logado(test_client):
    response = test_client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    print(f"\n\n\n#######################################\nTeste realizado com sucesso! Não foi possível ler o usuário. Pelo motivo de:\n\n {response.json()}\n#######################################\n\n\n\n\n\n")
