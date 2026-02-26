from pathlib import Path
from .base import BaseBuilder
from ..templates.tests import test_auth_controller_template, test_auth_service_template

class TestBuilder(BaseBuilder):
    """Builder responsável por criar estrutura de testes e configurar pytest."""

    def build(self):
        self._create_tests_folder()
        self._update_pyproject()

    def _create_tests_folder(self):
        tests_path = self.base_path / "tests"
        modules_path = tests_path / "modules"
        auth_tests_path = modules_path / "auth"
        users_tests_path = modules_path / "users"

        folders = [tests_path, modules_path, auth_tests_path, users_tests_path]
        self.ensure_structure(folders)

        # Criar __init__.py
        for folder in folders:
            self.create_file(folder / "__init__.py", "")

        # Templates de teste
        self.create_file(auth_tests_path / "test_auth_controller.py", test_auth_controller_template())
        self.create_file(auth_tests_path / "test_auth_service.py", test_auth_service_template())

    def _update_pyproject(self):
        pyproject_path = self.base_path / "pyproject.toml"
        if not pyproject_path.exists():
            return

        # Append pytest config if não existir
        pytest_config = """

        [dependency-groups]
        dev = [
            "httpx>=0.28.1",
            "pytest>=9.0.2",
            "pytest-asyncio>=1.3.0",
            "pytest-cov>=7.0.0",
            "pytest-mock>=3.15.1",
        ]

        [tool.pytest.ini_options]
        filterwarnings = [
            "ignore::DeprecationWarning"
        ]
        pythonpath = ["."]
        testpaths = ["tests"]
        """
        self.append_file(pyproject_path, pytest_config)