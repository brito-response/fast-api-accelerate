from pathlib import Path
from typing import List, Optional
import subprocess
import typer


class FileSystem:
    """ Classe utilitária responsável por manipular arquivos, diretórios e execução de comandos externos. """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

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

        self._log(f"📄 Created file: {path}")

    def append_to_file(self, path: Path, content: str):
        if not path.exists():
            self._log(f"⚠️ File does not exist for append: {path}")
            return

        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

        self._log(f"➕ Appended to file: {path}")

    def install_dependencies(self, dependencies: List[str]):
        """ Tenta instalar dependências usando uv. Se falhar, tenta pip. """
        for dep in dependencies:
            try:
                self._log(f"📦 Installing {dep} using uv...")
                subprocess.run(["uv", "add", dep],check=True)
            except Exception:
                self._log(f"⚠️ uv failed, trying pip for {dep}...")
                subprocess.run(["pip", "install", dep],check=True)

    def run_command(self, command: str):
        self._log(f"⚙️ Running command: {command}")

        subprocess.run(command.split(),check=True)

    def _log(self, message: str):
        if self.verbose:
            typer.secho(message, fg=typer.colors.BLUE)