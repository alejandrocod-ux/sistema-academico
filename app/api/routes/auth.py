from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioPublico, TokenResponse
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    criar_token_jwt,
    decodificar_token_jwt,
    gerar_hash_senha,
    verificar_senha,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UsuarioPublico, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        ativo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=TokenResponse)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    token = criar_token_jwt(usuario.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticação necessária ou token inválido/expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credenciais is None:
        raise erro

    try:
        payload = decodificar_token_jwt(credenciais.credentials)
        usuario_id = int(payload.get("sub", ""))
    except (InvalidTokenError, ValueError, TypeError):
        raise erro

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None or not usuario.ativo:
        raise erro

    return usuario


@router.get("/me", response_model=UsuarioPublico)
def consultar_usuario_autenticado(usuario: Usuario = Depends(obter_usuario_atual)):
    return usuario
