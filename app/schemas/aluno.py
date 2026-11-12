from pydantic import BaseModel
from datetime import date


class AlunoCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    matricula: str
    data_nascimento: date
    status: str