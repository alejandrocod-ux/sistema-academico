from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
