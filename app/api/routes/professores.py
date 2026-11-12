
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.models.professor import Professor
from app.models.turma import Turma
from app.models.usuario import Usuario
from app.schemas.professor import ProfessorCreate
from app.api.routes.auth import obter_usuario_atual


router = APIRouter(
    prefix="/professores",
    tags=["Professores"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_professor(
    professor: ProfessorCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    existente = db.query(Professor).filter(
        (Professor.cpf == professor.cpf) |
        (Professor.email == professor.email)
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="CPF ou e-mail já cadastrado."
        )

    novo_professor = Professor(
        nome=professor.nome,
        cpf=professor.cpf,
        email=professor.email,
        area_atuacao=professor.area_atuacao,
        status=professor.status
    )

    try:
        db.add(novo_professor)
        db.commit()
        db.refresh(novo_professor)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não foi possível cadastrar. CPF ou e-mail já existente."
        )

    return {
        "success": True,
        "message": "Professor cadastrado com sucesso.",
        "data": {
            "id": novo_professor.id,
            "nome": novo_professor.nome,
            "cpf": novo_professor.cpf,
            "email": novo_professor.email,
            "area_atuacao": novo_professor.area_atuacao,
            "status": novo_professor.status
        }
    }


@router.get("/")
def listar_professores(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    professores = db.query(Professor).all()

    return {
        "success": True,
        "data": [
            {
                "id": professor.id,
                "nome": professor.nome,
                "cpf": professor.cpf,
                "email": professor.email,
                "area_atuacao": professor.area_atuacao,
                "status": professor.status
            }
            for professor in professores
        ]
    }


@router.get("/{id}")
def buscar_professor(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    professor = db.query(Professor).filter(
        Professor.id == id
    ).first()

    if not professor:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado."
        )

    return {
        "success": True,
        "data": {
            "id": professor.id,
            "nome": professor.nome,
            "cpf": professor.cpf,
            "email": professor.email,
            "area_atuacao": professor.area_atuacao,
            "status": professor.status
        }
    }


@router.put("/{id}")
def atualizar_professor(
    id: int,
    professor: ProfessorCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    professor_existente = db.query(Professor).filter(
        Professor.id == id
    ).first()

    if not professor_existente:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado."
        )

    duplicado = db.query(Professor).filter(
        Professor.id != id,
        (
            (Professor.cpf == professor.cpf) |
            (Professor.email == professor.email)
        )
    ).first()

    if duplicado:
        raise HTTPException(
            status_code=409,
            detail="CPF ou e-mail já cadastrado para outro professor."
        )

    professor_existente.nome = professor.nome
    professor_existente.cpf = professor.cpf
    professor_existente.email = professor.email
    professor_existente.area_atuacao = professor.area_atuacao
    professor_existente.status = professor.status

    try:
        db.commit()
        db.refresh(professor_existente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não foi possível atualizar. CPF ou e-mail já existente."
        )

    return {
        "success": True,
        "message": "Professor atualizado com sucesso.",
        "data": {
            "id": professor_existente.id,
            "nome": professor_existente.nome,
            "cpf": professor_existente.cpf,
            "email": professor_existente.email,
            "area_atuacao": professor_existente.area_atuacao,
            "status": professor_existente.status
        }
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_professor(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    professor = db.query(Professor).filter(
        Professor.id == id
    ).first()

    if not professor:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado."
        )

    turma_associada = db.query(Turma).filter(
        Turma.id_professor == id
    ).first()

    if turma_associada:
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: existem turmas vinculadas a este professor."
        )

    db.delete(professor)
    db.commit()

    return
