from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.tarefa_exceptions import TarefaNaoEncontradaException


async def tarefa_nao_encontrada_handler(
    request: Request,
    exc: TarefaNaoEncontradaException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )