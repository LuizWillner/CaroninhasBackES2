from pydantic import BaseModel

class BasicResponse(BaseModel):
    response: str
