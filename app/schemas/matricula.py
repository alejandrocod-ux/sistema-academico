from pydantic import BaseModel
from datetime import date


class MatriculaCreate(BaseModel):
    id_aluno: int
    id_turma: int
    data_matricula: date
    status: str