from fastapi import APIRouter, HTTPException
from app.schemas.disciplina import DisciplinaCreate

router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)

disciplinas = []


@router.post("/", status_code=201)
def cadastrar_disciplina(disciplina: DisciplinaCreate):
    nova = {
        "id": len(disciplinas) + 1,
        **disciplina.model_dump()
    }

    disciplinas.append(nova)

    return {
        "success": True,
        "message": "Disciplina cadastrada com sucesso.",
        "data": nova
    }


@router.get("/")
def listar_disciplinas():
    return {
        "success": True,
        "data": disciplinas
    }


@router.get("/{id}")
def buscar_disciplina(id: int):
    for disciplina in disciplinas:
        if disciplina["id"] == id:
            return {"success": True, "data": disciplina}

    raise HTTPException(404, "Disciplina não encontrada.")


@router.put("/{id}")
def atualizar_disciplina(id: int, disciplina: DisciplinaCreate):
    for existente in disciplinas:
        if existente["id"] == id:
            existente.update(disciplina.model_dump())

            return {
                "success": True,
                "message": "Disciplina atualizada com sucesso.",
                "data": existente
            }

    raise HTTPException(404, "Disciplina não encontrada.")


@router.delete("/{id}", status_code=204)
def excluir_disciplina(id: int):
    for indice, disciplina in enumerate(disciplinas):
        if disciplina["id"] == id:
            disciplinas.pop(indice)
            return

    raise HTTPException(404, "Disciplina não encontrada.")