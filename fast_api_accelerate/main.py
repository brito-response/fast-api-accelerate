import typer
from fast_api_accelerate.commands.create_project import create_app
from fast_api_accelerate.commands.test_config_project import tests_app

app = typer.Typer(help="🚀 Fast API Accelerate - Enterprise FastAPI Scaffolding CLI", add_completion=False)

app.add_typer(create_app, name="create")
app.add_typer(tests_app, name="tests")

def run():
    app()

if __name__ == "__main__":
    run()