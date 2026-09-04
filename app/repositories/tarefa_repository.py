from sqlalchemy.orm import Session

from app.models.tarefa import Tarefa


class TarefaRepository:

    def salvar(self, db: Session, tarefa: Tarefa):
        db.add(tarefa)
        db.commit()
        db.refresh(tarefa)
        return tarefa

    def listar(self, db: Session):
        return db.query(Tarefa).all()

    def buscar_por_id(self, db: Session, id: int):
        return db.query(Tarefa).filter(Tarefa.id == id).first()

    def atualizar(self, db: Session, tarefa: Tarefa, titulo: str, descricao: str):
        tarefa.titulo = titulo
        tarefa.descricao = descricao

        db.commit()
        db.refresh(tarefa)
        return tarefa

    def deletar(self, db: Session, tarefa: Tarefa):
        db.delete(tarefa)
        db.commit()

    def alterar_status(self, db: Session, tarefa: Tarefa, status):
        tarefa.status = status
        db.commit()
        db.refresh(tarefa)
        return tarefa