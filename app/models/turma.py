from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20))
    id_disciplina: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id")
    )
    id_professor: Mapped[int] = mapped_column(
        ForeignKey("professores.id")
    )
    periodo_letivo: Mapped[str] = mapped_column(String(20))
    horario: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20))