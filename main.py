from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import hello_world
from app.routers import carona
from app.security import authentication


load_dotenv(dotenv_path="credentials.env")

app = FastAPI()
app.include_router(hello_world.router)
app.include_router(authentication.router)
app.include_router(carona.router)

@app.get("/ping")
def ping():
    return "pong"
