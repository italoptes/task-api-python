from dns.rdtypes import dnskeybase
from dns.rdtypes import dnskeybase
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tarefa import Tarefa
from app.repositories.tarefa_repository import TarefaRepository


class TarefaService:

    def __init__(self):
        self.repository = TarefaRepository()

    def criar(self, db: Session, titulo: str, descricao: str):
        tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao
        )

        return self.repository.salvar(db, tarefa)

    def listar(self, db: Session):
        return self.repository.listar(db)

    def buscar_por_id(self, db: Session, id: int):
        tarefa = self.repository.buscar_por_id(db, id)

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
        )
        return tarefa

    def editar_por_id(self, db: Session, id: int, titulo: str, descricao: str):
        tarefa = self.repository.buscar_por_id(db,id)
        if(tarefa is None):
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )
        return self.repository.atualizar(db, tarefa, titulo, descricao)

    def deletar(self, db: Session, id: int):
        tarefa = self.repository.buscar_por_id(db, id)

        if tarefa is None:
            raise HTTPException(
                status_code=404,
                detail="Tarefa não encontrada"
            )       

        self.repository.deletar(db, tarefa)