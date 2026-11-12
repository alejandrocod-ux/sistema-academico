from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(
        String(150)
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True
    )

    area_atuacao: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )