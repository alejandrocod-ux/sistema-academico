from pydantic import BaseModel


class DisciplinaCreate(BaseModel):
    nome: str
    codigo: str
    descricao: str | None = None
    carga_horaria: int
    status: str