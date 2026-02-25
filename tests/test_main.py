import pytest
from typer.testing import CliRunner
from main import app


class TestCLIEntryPoint:
    """Tests related to CLI bootstrap and command registration."""

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

    def test_cli_starts(self):
        """CLI should start and show help message."""
        result = self.runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "Fast API Accelerate" in result.output

    def test_registered_commands(self):
        """CLI should have all expected commands registered."""
        result = self.runner.invoke(app, ["--help"])

        assert "create" in result.output
        assert "resource" in result.output
        assert "auth" in result.output
        assert "database" in result.output
        assert "di" in result.output
        assert "swagger" in result.output

    def test_number_of_commands(self):
        """CLI should register exactly 6 commands."""
        assert len(app.registered_commands) == 6


class TestCreateCommand:
    """Tests for the 'create' command."""

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

    def test_create_requires_name(self):
        """Create command should fail without project name."""
        result = self.runner.invoke(app, ["create"])

        assert result.exit_code != 0

    def test_create_basic(self):
        """Create command should execute successfully with required argument."""
        result = self.runner.invoke(app, ["create", "my_project"])

        assert result.exit_code == 0
        assert "Creating project..." in result.output
        assert "my_project" in result.output

    def test_create_with_options(self):
        """Create command should accept optional flags."""
        result = self.runner.invoke(app,["create","my_project","--no-swagger","--docker","--auth","--database","postgres","--orm","sqlmodel"])

        assert result.exit_code == 0
        assert "postgres" in result.output
        assert "sqlmodel" in result.output