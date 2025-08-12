from pydantic import BaseModel
from pydantic import conint


class LoginInput(BaseModel):
    username: str
    password: str


class LoginOutput(BaseModel):
    access_token: str


class PowInput(BaseModel):
    base: int
    exp: int


class NInput(BaseModel):
    n: conint(ge=0)


class ResultOutput(BaseModel):
    result: int
