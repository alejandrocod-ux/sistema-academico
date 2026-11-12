from pydantic import BaseModel


class TurmaCreate(BaseModel):
    codigo: str
    id_disciplina: int
    id_professor: int
    periodo_letivo: str
    horario: str
    status: str