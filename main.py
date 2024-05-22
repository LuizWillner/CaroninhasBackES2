from fastapi import FastAPI
from dotenv import load_dotenv

from app.security import authentication
from app.routers import hello_world, pedido_carona
from app.routers import carona
from app.routers import motorista
from app.routers import veiculo
from app.routers import user_carona


load_dotenv(dotenv_path="credentials.env")

app = FastAPI()

# Configure CORS para permitir qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


app.include_router(hello_world.router)
app.include_router(authentication.router)
app.include_router(carona.router)
app.include_router(motorista.router)
app.include_router(veiculo.router)
app.include_router(user_carona.router)
app.include_router(pedido_carona.router)


@app.get("/ping")
def ping():
    return "pong"
