from pydantic import BaseModel

#Equivalente ao DTO em java
class TarefaCreate(BaseModel):
    titulo: str
    descricao: str