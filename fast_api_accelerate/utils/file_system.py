from pathlib import Path
from typing import List, Optional
import subprocess
import typer


class FileSystem:
    """ Classe utilitária responsável por manipular arquivos, diretórios e execução de comandos externos. """

    def __init__(self, project_path: Path, verbose: bool = True):
        self.verbose = verbose
        self.project_path = project_path
    
    def _log(self, message: str):
        if self.verbose:
            typer.secho(message, fg=typer.colors.BLUE)

    def create_dir(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            self._log(f"📁 Created directory: {path}")
        else:
            self._log(f"📁 Directory already exists: {path}")

    def create_file(self,path: Path, content: str, overwrite: bool = False):
        if path.exists() and not overwrite:
            self._log(f"⚠️ File already exists (skipped): {path}")
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        self._log(f"reated file📄: {path}")

    def append_to_file(self, path: Path, content: str):
        if not path.exists():
            self._log(f"⚠️ File does not exist for append: {path}")
            return

        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

        self._log(f"➕ Appended to file: {path}")

    def install_dependencies(self):
        self._log(f"📦 Installing project dependencies in {self.project_path}...")
        subprocess.run(["uv", "sync"], cwd=self.project_path, check=True)
        self._log("✅ Dependencies installed successfully.")

    def run_command(self, command: str):
        self._log(f"⚙️ Running command: {command}")
        subprocess.run(command.split(),check=True)