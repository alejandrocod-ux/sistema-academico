import os
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if not SECRET_KEY or SECRET_KEY == "COLOQUE_UMA_CHAVE_SECRETA_FORTE_AQUI":
    raise RuntimeError(
        "JWT_SECRET_KEY não configurada. Crie o arquivo .env com uma chave secreta forte."
    )

password_hasher = PasswordHasher()


def gerar_hash_senha(senha: str) -> str:
    return password_hasher.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    try:
        return password_hasher.verify(senha_hash, senha_plana)
    except (VerifyMismatchError, VerificationError):
        return False


def criar_token_jwt(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)
    expiracao = agora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": expiracao,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
