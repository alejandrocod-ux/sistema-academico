from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Matricula(Base):
    __tablename__ = "matriculas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_aluno: Mapped[int] = mapped_column(ForeignKey("alunos.id"))
    id_turma: Mapped[int] = mapped_column(ForeignKey("turmas.id"))
    data_matricula: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20))