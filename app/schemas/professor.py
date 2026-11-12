from pydantic import BaseModel


class ProfessorCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    area_atuacao: str
    status: str