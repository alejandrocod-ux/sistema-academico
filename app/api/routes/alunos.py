from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.routes.auth import obter_usuario_atual
from app.models.usuario import Usuario

from app.schemas.aluno import AlunoCreate
from app.database.connection import get_db
from app.models.aluno import Aluno

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


@router.post("/", status_code=201)
def cadastrar_aluno(
    aluno: AlunoCreate,
    db: Session = Depends(get_db)
):
    novo_aluno = Aluno(
        nome=aluno.nome,
        cpf=aluno.cpf,
        email=aluno.email,
        matricula=aluno.matricula,
        data_nascimento=aluno.data_nascimento,
        status=aluno.status
    )

    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)

    return {
        "success": True,
        "message": "Aluno cadastrado com sucesso.",
        "data": {
            "id": novo_aluno.id,
            "nome": novo_aluno.nome,
            "cpf": novo_aluno.cpf,
            "email": novo_aluno.email,
            "matricula": novo_aluno.matricula,
            "data_nascimento": novo_aluno.data_nascimento,
            "status": novo_aluno.status
        }
    }


@router.get("/")
def listar_alunos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    alunos = db.query(Aluno).all()

    return {
        "success": True,
        "data": [
            {
                "id": aluno.id,
                "nome": aluno.nome,
                "cpf": aluno.cpf,
                "email": aluno.email,
                "matricula": aluno.matricula,
                "data_nascimento": aluno.data_nascimento,
                "status": aluno.status
            }
            for aluno in alunos
        ]
    }


@router.get("/{id}")
def buscar_aluno(
    id: int,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado."
        )

    return {
        "success": True,
        "data": {
            "id": aluno.id,
            "nome": aluno.nome,
            "cpf": aluno.cpf,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "data_nascimento": aluno.data_nascimento,
            "status": aluno.status
        }
    }


@router.put("/{id}")
def atualizar_aluno(
    id: int,
    aluno: AlunoCreate,
    db: Session = Depends(get_db)
):
    aluno_existente = db.query(Aluno).filter(Aluno.id == id).first()

    if not aluno_existente:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado."
        )

    aluno_existente.nome = aluno.nome
    aluno_existente.cpf = aluno.cpf
    aluno_existente.email = aluno.email
    aluno_existente.matricula = aluno.matricula
    aluno_existente.data_nascimento = aluno.data_nascimento
    aluno_existente.status = aluno.status

    db.commit()
    db.refresh(aluno_existente)

    return {
        "success": True,
        "message": "Aluno atualizado com sucesso.",
        "data": {
            "id": aluno_existente.id,
            "nome": aluno_existente.nome,
            "cpf": aluno_existente.cpf,
            "email": aluno_existente.email,
            "matricula": aluno_existente.matricula,
            "data_nascimento": aluno_existente.data_nascimento,
            "status": aluno_existente.status
        }
    }


@router.delete("/{id}", status_code=204)
def excluir_aluno(
    id: int,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado."
        )

    db.delete(aluno)
    db.commit()

    return