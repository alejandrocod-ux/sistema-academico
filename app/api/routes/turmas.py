from fastapi import APIRouter, HTTPException
from app.schemas.turma import TurmaCreate

router = APIRouter(
    prefix="/turmas",
    tags=["Turmas"]
)

turmas = []


@router.post("/", status_code=201)
def cadastrar_turma(turma: TurmaCreate):
    nova_turma = {
        "id": len(turmas) + 1,
        **turma.model_dump()
    }

    turmas.append(nova_turma)

    return {
        "success": True,
        "message": "Turma cadastrada com sucesso.",
        "data": nova_turma
    }


@router.get("/")
def listar_turmas():
    return {
        "success": True,
        "data": turmas
    }


@router.get("/{id}")
def buscar_turma(id: int):
    for turma in turmas:
        if turma["id"] == id:
            return {
                "success": True,
                "data": turma
            }

    raise HTTPException(
        status_code=404,
        detail="Turma não encontrada."
    )


@router.put("/{id}")
def atualizar_turma(id: int, turma: TurmaCreate):
    for turma_existente in turmas:
        if turma_existente["id"] == id:
            turma_existente.update(turma.model_dump())

            return {
                "success": True,
                "message": "Turma atualizada com sucesso.",
                "data": turma_existente
            }

    raise HTTPException(
        status_code=404,
        detail="Turma não encontrada."
    )


@router.delete("/{id}", status_code=204)
def excluir_turma(id: int):
    for indice, turma in enumerate(turmas):
        if turma["id"] == id:
            turmas.pop(indice)
            return

    raise HTTPException(
        status_code=404,
        detail="Turma não encontrada."
    )