from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioPublico(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
