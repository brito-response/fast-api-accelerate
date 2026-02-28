def main_project_template(name:str ) -> str:
    return f"""from fastapi import FastAPI
from src.modules.users.controllers import UsersController
from src.modules.auth.controllers import AuthController
from fastapi.staticfiles import StaticFiles
from src.core.startup import register_startup_events

app = FastAPI(
    title="{name}", description="API para blog usandoFastAPI",
    version="1.0.0",
    contact={{"clodoaldo": "Neto","email": "clodoaldobritodev@gmail.com"}},
    license_info={{"license": "MIT","url": "https://opensource.org/licenses/MIT"}},
    swagger_ui_parameters={{"persistAuthorization": True}},
)

register_startup_events(app)

@app.get("/")
async def index():
    return {{"users":"/users","auth":"/auth","for documentação":"/docs"}}

usuarios = UsersController()
auth = AuthController()

app.include_router(usuarios.router)
app.include_router(auth.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
"""