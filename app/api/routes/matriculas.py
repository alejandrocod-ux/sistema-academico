from fastapi import APIRouter, HTTPException
from app.schemas.matricula import MatriculaCreate

router = APIRouter(
    prefix="/matriculas",
    tags=["Matrículas"]
)

matriculas = []


@router.post("/", status_code=201)
def cadastrar_matricula(matricula: MatriculaCreate):

    nova_matricula = {
        "id": len(matriculas) + 1,
        **matricula.model_dump()
    }

    matriculas.append(nova_matricula)

    return {
        "success": True,
        "message": "Matrícula realizada com sucesso.",
        "data": nova_matricula
    }


@router.get("/")
def listar_matriculas():
    return {
        "success": True,
        "data": matriculas
    }


@router.get("/{id}")
def buscar_matricula(id: int):

    for matricula in matriculas:
        if matricula["id"] == id:
            return {
                "success": True,
                "data": matricula
            }

    raise HTTPException(
        status_code=404,
        detail="Matrícula não encontrada."
    )


@router.put("/{id}")
def atualizar_matricula(id: int, matricula: MatriculaCreate):

    for matricula_existente in matriculas:

        if matricula_existente["id"] == id:

            matricula_existente.update(
                matricula.model_dump()
            )

            return {
                "success": True,
                "message": "Matrícula atualizada com sucesso.",
                "data": matricula_existente
            }

    raise HTTPException(
        status_code=404,
        detail="Matrícula não encontrada."
    )


@router.delete("/{id}", status_code=204)
def excluir_matricula(id: int):

    for indice, matricula in enumerate(matriculas):

        if matricula["id"] == id:
            matriculas.pop(indice)
            return

    raise HTTPException(
        status_code=404,
        detail="Matrícula não encontrada."
    )