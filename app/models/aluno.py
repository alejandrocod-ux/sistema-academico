from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Aluno(Base):
    __tablename__ = "alunos"

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

    matricula: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    data_nascimento: Mapped[Date] = mapped_column(
        Date
    )

    status: Mapped[str] = mapped_column(
        String(20)
    )