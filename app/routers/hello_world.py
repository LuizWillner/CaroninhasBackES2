from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Annotated, Optional


router = APIRouter(prefix='/message')


@router.get("/hello-world")
def get_hello_world()-> str:
    return "Hello, world!"


@router.get("/me/{name}")
def get_personal_message(name: str) -> str:
    return f"Hi {name}"


@router.get("/me")
def present_self(name: str, age: int):
    return f"My name is {name} and I am {age} years old."