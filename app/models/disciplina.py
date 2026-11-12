from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150))
    codigo: Mapped[str] = mapped_column(String(20), unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    carga_horaria: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20))