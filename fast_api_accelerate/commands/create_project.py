import typer
from pathlib import Path
from ..builders.project_builder import ProjectBuilder


create_app = typer.Typer(help="Create a new FastAPI project")

@create_app.command("project")
def create_project(name: str = typer.Argument(..., help="Project name"),path: str = typer.Option(".", "--path", "-p"),database: bool = typer.Option(True, "--database/--no-database"),auth: bool = typer.Option(True, "--auth/--no-auth")):
    """Create a new production-ready FastAPI project."""

    base_path = Path(path).resolve()

    if not base_path.exists():
        typer.secho("x Base path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    project_path = base_path / name

    if project_path.exists():
        typer.secho(" x Project already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("🚀 Creating FastAPI project...", fg=typer.colors.CYAN)

    builder = ProjectBuilder(base_path=base_path,project_name=name)
    builder.run()

    typer.secho("✓ Project created successfully!", fg=typer.colors.GREEN)