def startup_template() -> str:
    return """import os
from fastapi import FastAPI

UPLOAD_DIRS = [
    "uploads",
    "uploads/users",
]

def create_upload_dirs():
    #Cria todas as pastas necessárias para uploads.Se já existirem, não faz nada.
    
    for directory in UPLOAD_DIRS:
        os.makedirs(directory, exist_ok=True)


def register_startup_events(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        create_upload_dirs()
        print("\\033[92m✓\\033[0m pastas de upload criadas com sucesso")

"""
