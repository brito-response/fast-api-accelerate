import typer
from pathlib import Path
from ..builders.test_builder import TestBuilder 


tests_app = typer.Typer(help="Configure tests for a FastAPI project")

@tests_app.command("setup")
def setup_tests(path: str = typer.Option(".", "--path", "-p", help="Base path of the project")):
    """Configure test structure and add pytest settings to pyproject.toml."""

    base_path = Path(path).resolve()

    if not base_path.exists():
        typer.secho("\033[0;31m x \033[0m Path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("🧪 Setting up test structure...", fg=typer.colors.CYAN)

    builder = TestBuilder(base_path=base_path)
    builder.run()

    typer.secho("\033[0;32m✓\033[0m Test structure and configuration added!", fg=typer.colors.GREEN)