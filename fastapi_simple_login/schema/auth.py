from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str


class LoginOutput(BaseModel):
    status: str
    token: str