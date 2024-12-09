from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
