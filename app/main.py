from fastapi import FastAPI

from app.controllers.tarefa_controller import router as tarefa_router
from app.exceptions.handlers import tarefa_nao_encontrada_handler
from app.exceptions.tarefa_exceptions import TarefaNaoEncontradaException

app = FastAPI()

app.add_exception_handler(
    TarefaNaoEncontradaException,
    tarefa_nao_encontrada_handler
)

app.include_router(tarefa_router)