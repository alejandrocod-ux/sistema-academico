from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base

from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.disciplina import Disciplina
from app.models.turma import Turma
from app.models.matricula import Matricula
from app.models.usuario import Usuario

from app.api.routes import (
    alunos,
    professores,
    disciplinas,
    turmas,
    matriculas,
    auth
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gerenciamento Acadêmico",
    version="1.0.0"
)

app.include_router(alunos.router)
app.include_router(professores.router)
app.include_router(disciplinas.router)
app.include_router(turmas.router)
app.include_router(matriculas.router)
app.include_router(auth.router)


@app.get("/")
def inicio():
    return {
        "mensagem": "API do Sistema Acadêmico funcionando!"
    }