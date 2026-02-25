from pathlib import Path
from typing import Optional

from .base import BaseBuilder
from ..templates import settings_database_template,file_database_template


class DatabaseBuilder(BaseBuilder):
    """ Builder responsável por configurar banco de dados async usando SQLAlchemy 2.0. """

    def __init__(self,base_path: Path,database_url: Optional[str] = None,use_alembic: bool = True):
        super().__init__(base_path)

        self.database_url = (database_url or "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db")
        self.use_alembic = use_alembic
        self.core_path = self.base_path / "app" / "core"


    def build(self):
        self._create_structure()
        self._create_env_file()
        self._create_config()
        self._create_database_file()

        if self.use_alembic:
            self._create_alembic()

        self._install_dependencies()

    def _create_structure(self):
        self.ensure_structure([self.core_path])


    def _create_env_file(self):
        env_path = self.base_path / ".env"

        if env_path.exists():
            return

        content = f"""DATABASE_URL={self.database_url} SECRET_KEY=supersecretkey"""
        self.create_file(env_path, content)


    def _create_config(self):
        self.create_file(self.core_path / "config.py", settings_database_template)

    def _create_database_file(self):
        self.create_file(self.core_path / "database.py", file_database_template)

    def _create_alembic(self):
        """ Inicializa Alembic no projeto. Assume que CLI pode rodar comandos shell. """
        self.fs.run_command("alembic init alembic")


    def _install_dependencies(self):
        deps = ["sqlalchemy>=2.0.0","asyncpg","alembic","pydantic-settings"]

        self.install_dependencies(deps)