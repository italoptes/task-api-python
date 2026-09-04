from pydantic import BaseModel

from app.models.tarefa import StatusTarefa


class TarefaCreate(BaseModel):
    titulo: str
    descricao: str


class TarefaUpdate(BaseModel):
    titulo: str
    descricao: str


class TarefaStatusUpdate(BaseModel):
    status: StatusTarefa


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: StatusTarefa

    model_config = {
        "from_attributes": True
    }