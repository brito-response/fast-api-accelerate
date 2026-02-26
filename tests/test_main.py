import pytest
from typer.testing import CliRunner
from fast_api_accelerate.main import app


class TestCLIEntryPoint:
    """Tests related to CLI bootstrap and command registration."""

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

    def test_cli_starts_and_show_help_message(self):
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Fast API Accelerate" in result.output

    def test_registered_commands(self):
        result = self.runner.invoke(app, ["--help"])
        assert "create" in result.output
        assert "tests" in result.output 


class TestCreateCommand:
    """Tests for the 'create' command."""
    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

    def test_create_requires_name_command_should_fail_without_project_name(self):
        result = self.runner.invoke(app, ["create"])
        assert result.exit_code != 0