from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import hello_world
from app.security import authentication


load_dotenv(dotenv_path="credentials.env")

app = FastAPI()

app.include_router(hello_world.router)
app.include_router(authentication.router)

@app.get("/")
def root():
    return "This is root"

