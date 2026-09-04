from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {
        "projeto" : "Task API",
        "status": "em desenvolvimento"
    }