from pathlib import Path

from .base import BaseBuilder
from .database_builder import DatabaseBuilder
from .auth_builder import AuthBuilder


class ProjectBuilder(BaseBuilder):
    """ Builder principal responsável por criar a aplicação base.Orquestra outros builders. """

    def __init__(self,base_path: Path,project_name: str,with_database: bool = True,with_auth: bool = True,with_alembic: bool = True):
        super().__init__(base_path)

        self.project_name = project_name
        self.project_path = self.base_path / project_name

        self.with_database = with_database
        self.with_auth = with_auth
        self.with_alembic = with_alembic

    def build(self):
        self._create_project_root()
        self._create_app_structure()
        self._create_main_file()
        self._create_pyproject()

        if self.with_database:
            self._configure_database()

        if self.with_auth:
            self._configure_auth()

        self._install_base_dependencies()

    def _create_project_root(self):
        self.ensure_structure([self.project_path])

    def _create_app_structure(self):
        folders = [
            self.project_path / "app",
            self.project_path / "app" / "core",
            self.project_path / "app" / "modules",
        ]

        self.ensure_structure(folders)

        for folder in folders: # criar __init__.py
            self.create_file(folder / "__init__.py", "")


    def _create_main_file(self):
        content = """from fastapi import FastAPI
        app = FastAPI(title="My FastAPI App",version="1.0.0")

        @app.get("/")
        async def root():
            return {"message": "API Running 🚀"}
        """
        self.create_file(self.project_path / "app" / "main.py", content)


    def _create_pyproject(self):
        content = f"""[project]
        name = "{self.project_name}"
        version = "0.1.0"
        description = ""
        requires-python = ">=3.12"
        dependencies = []

        [dependency-groups]
        dev = [
            "pytest",
            "pytest-asyncio",
            "httpx",
            "black",
        ]
        """
        self.create_file(self.project_path / "pyproject.toml", content)


    def _configure_database(self):
        db_builder = DatabaseBuilder(base_path=self.project_path,use_alembic=self.with_alembic)
        db_builder.run()

    def _configure_auth(self):
        auth_builder = AuthBuilder(base_path=self.project_path,jwt=True,refresh_token=True,roles=True,async_db=True)
        auth_builder.run()

    def _install_base_dependencies(self):
        deps = ["fastapi","uvicorn[standard]"]

        self.install_dependencies(deps)