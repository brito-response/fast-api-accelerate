import typer
from pathlib import Path
from typing import List

from src.builders.resource_builder import ResourceBuilder

app = typer.Typer(help="Resource generation commands")


@app.command("create")
def create_resource(
    name: str = typer.Argument(..., help="Resource name (e.g. user)"),
    fields: List[str] = typer.Argument(
        None,
        help="Fields for the resource (e.g. name email age)",
    ),
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Base path of the project",
    ),
    crud: bool = typer.Option(
        True,
        "--crud/--no-crud",
        help="Generate CRUD endpoints",
    ),
):
    """
    Generate a new async CRUD resource.
    """

    base_path = Path(path).resolve()

    if not base_path.exists():
        typer.secho("❌ Path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not name.isidentifier():
        typer.secho("❌ Invalid resource name.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"📦 Creating resource '{name}'...", fg=typer.colors.CYAN)

    builder = ResourceBuilder(
        base_path=base_path,
        resource_name=name,
        fields=fields or [],
        with_crud=crud,
    )

    builder.run()

    typer.secho("✅ Resource created successfully!", fg=typer.colors.GREEN)