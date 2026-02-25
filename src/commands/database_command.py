import typer
from pathlib import Path
from typing import Optional

from src.builders.database_builder import DatabaseBuilder

app = typer.Typer(help="Database configuration commands")


@app.command("install")
def install_database(path: str = typer.Option(".","--path","-p",help="Base path of the project"),db_type: str = typer.Option("postgres","--type",help="Database type: postgres | sqlite | mysql"),url: Optional[str] = typer.Option(None,"--url",help="Custom database URL (overrides --type)"),alembic: bool = typer.Option(True,"--alembic/--no-alembic",help="Enable Alembic migrations")):
    """
    Install async database configuration into an existing project.
    """

    base_path = Path(path).resolve()

    if not base_path.exists():
        typer.secho("❌ Path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    database_url = url

    if not database_url:
        if db_type == "postgres":
            database_url = ("postgresql+asyncpg://postgres:postgres@localhost:5432/app_db")
        elif db_type == "sqlite":
            database_url = "sqlite+aiosqlite:///./app.db"
        elif db_type == "mysql":
            database_url = ("mysql+aiomysql://root:root@localhost:3306/app_db")
        else:
            typer.secho("❌ Invalid database type.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    typer.secho("🛢 Configuring Database...", fg=typer.colors.CYAN)

    builder = DatabaseBuilder(base_path=base_path,database_url=database_url,use_alembic=alembic)

    builder.run()

    typer.secho("✅ Database configured successfully!", fg=typer.colors.GREEN)