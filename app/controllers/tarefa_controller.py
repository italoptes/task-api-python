from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.tarefa import (
    TarefaCreate,
    TarefaResponse,
    TarefaStatusUpdate,
    TarefaUpdate
)
from app.services.tarefa_service import TarefaService

router = APIRouter()

service = TarefaService()

@router.post("/tarefas",response_model=TarefaResponse)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return service.criar(db, tarefa.titulo, tarefa.descricao)

@router.get("/tarefas",response_model=list[TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return service.listar(db)

@router.get("/tarefas/{id}",response_model=TarefaResponse)
def buscar_tarefa_por_id(id: int,db: Session = Depends(get_db)):
    return service.buscar_por_id(db, id)

@router.put("/tarefas/{id}",response_model=TarefaResponse)
def atualizar_tarefa(id: int,tarefa: TarefaUpdate,db: Session = Depends(get_db)):
    return service.editar_por_id( db,  id,  tarefa.titulo,  tarefa.descricao)

@router.patch("/tarefas/{id}/status",response_model=TarefaResponse)
def alterar_status( id: int,tarefa: TarefaStatusUpdate,db: Session = Depends(get_db)):
    return service.alterar_status(db,  id,tarefa.status)

@router.delete( "/tarefas/{id}", status_code=204)
def deletar_tarefa( id: int,db: Session = Depends(get_db)):
    service.deletar(db, id)