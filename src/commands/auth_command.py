import typer
from pathlib import Path
from typing import Optional

from src.builders.auth_builder import AuthBuilder

app = typer.Typer(help="Auth module commands")


@app.command("install")
def install_auth(path: str = typer.Option(".","--path","-p",help="Base path of the project"), jwt: bool = typer.Option(True,"--jwt/--no-jwt", help="Enable JWT authentication"), refresh_token: bool = typer.Option(True,"--refresh-token/--no-refresh-token", help="Enable refresh token support"), roles: bool = typer.Option(True,"--roles/--no-roles", help="Enable role-based authorization")):
    """Install authentication module into an existing project."""

    base_path = Path(path).resolve()

    if not base_path.exists():
        typer.secho("x Path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("🔐 Installing Auth Module...", fg=typer.colors.CYAN)

    builder = AuthBuilder(base_path=base_path,jwt=jwt,refresh_token=refresh_token,roles=roles,async_db=True)

    builder.run()

    typer.secho("✅ Auth module installed successfully!", fg=typer.colors.GREEN)