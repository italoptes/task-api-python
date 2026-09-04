from fastapi import FastAPI

from app.controllers.tarefa_controller import router as tarefa_router

app = FastAPI()

app.include_router(tarefa_router)