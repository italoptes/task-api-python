from sqlalchemy.orm import Session

from app.exceptions.tarefa_exceptions import TarefaNaoEncontradaException
from app.models.tarefa import StatusTarefa, Tarefa
from app.repositories.tarefa_repository import TarefaRepository


class TarefaService:

    def __init__(self):
        self.repository = TarefaRepository()

    def criar(self, db: Session, titulo: str, descricao: str):
        tarefa = Tarefa(titulo=titulo,descricao=descricao,status=StatusTarefa.PENDENTE)

        return self.repository.salvar(db, tarefa)

    def listar(self, db: Session):
        return self.repository.listar(db)

    def buscar_por_id(self, db: Session, id: int):
        tarefa = self.repository.buscar_por_id(db, id)
        if tarefa is None:
            raise TarefaNaoEncontradaException("Tarefa não encontrada")
        return tarefa

    def editar_por_id(self,  db: Session,id: int, titulo: str,descricao: str ):
        tarefa = self.repository.buscar_por_id(db, id)
        if tarefa is None:
            raise TarefaNaoEncontradaException("Tarefa não encontrada")
        return self.repository.atualizar(db,tarefa,titulo,descricao)

    def alterar_status(self, db: Session,id: int,status: StatusTarefa ):
        tarefa = self.repository.buscar_por_id(db, id)
        if tarefa is None:
            raise TarefaNaoEncontradaException( "Tarefa não encontrada")
        return self.repository.alterar_status(db,tarefa,status)

    def deletar(self, db: Session, id: int):
        tarefa = self.repository.buscar_por_id(db, id)
        if tarefa is None:
            raise TarefaNaoEncontradaException("Tarefa não encontrada")
        self.repository.deletar(db, tarefa)