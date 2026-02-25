import typer

app = typer.Typer(help="🚀 Fast API Accelerate - Enterprise FastAPI Scaffolding CLI", add_completion=False)

@app.command()
def create(name: str = typer.Argument(...,help="Project name"), swagger: bool = typer.Option(True, "--swagger/--no-swagger", help="Enable Swagger docs"),docker: bool = typer.Option(False, "--docker", help="Include Docker support"),auth: bool = typer.Option(False, "--auth", help="Include authentication module"),database: str = typer.Option(None,"--database",help="Database provider (postgres, mysql, sqlite)"),orm: str = typer.Option("sqlalchemy","--orm",help="ORM to use (sqlalchemy, sqlmodel)"),alembic: bool = typer.Option(True, "--alembic/--no-alembic", help="Include Alembic migrations"),tests: bool = typer.Option(True, "--tests/--no-tests", help="Include test structure"),clean_arch: bool = typer.Option(True, "--clean-arch/--no-clean-arch", help="Use Clean Architecture structure")):
    """Create a new FastAPI backend project with full configuration."""
    print("Creating project...")
    print(locals())

@app.command()
def resource(name: str = typer.Argument(..., help="Resource name"),crud: bool = typer.Option(True, "--crud/--no-crud", help="Generate CRUD endpoints"),dto: bool = typer.Option(True, "--dto/--no-dto", help="Generate DTO schemas"),service: bool = typer.Option(True, "--service/--no-service", help="Generate service layer"),repository: bool = typer.Option(True, "--repository/--no-repository", help="Generate repository layer")):
    """Generate a full resource (Controller + Service + Repository + DTO)."""
    print("Generating resource...")
    print(locals())


@app.command()
def auth(provider: str = typer.Option("jwt","--provider",help="Authentication provider (jwt, oauth2)"),roles: bool = typer.Option(False, "--roles", help="Enable role-based authorization"),refresh_token: bool = typer.Option(True, "--refresh-token", help="Enable refresh tokens")):
    """Generate authentication & authorization module."""
    print("Generating auth module...")
    print(locals())

@app.command()
def database(provider: str = typer.Argument(..., help="Database provider (postgres, mysql, sqlite)"),async_mode: bool = typer.Option(True, "--async/--sync", help="Use async engine"),migration: bool = typer.Option(True, "--migration/--no-migration", help="Enable migrations")):
    """Configure database and ORM."""
    print("Configuring database...")
    print(locals())

@app.command()
def di(container: bool = typer.Option(True, "--container", help="Generate DI container"),factories: bool = typer.Option(True, "--factories", help="Generate factory pattern")):
    """Generate Dependency Injection structure."""
    print("Generating DI structure...")
    print(locals())

@app.command()
def swagger(disable: bool = typer.Option(False, "--disable", help="Disable Swagger docs"),custom: bool = typer.Option(False, "--custom", help="Generate custom Swagger configuration"),):
    """Configure Swagger / OpenAPI."""
    print("Configuring Swagger...")
    print(locals())

def run():
    app()

if __name__ == "__main__":
    run()