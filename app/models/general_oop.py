from pydantic import BaseModel

class HTTPBasicResponse(BaseModel):
    status_code: int
    detail: str
