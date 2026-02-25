import typer
from enum import Enum


class LogLevel(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


class Logger:
    """
    Logger central da CLI.
    Desacoplado da regra de negócio.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def info(self, message: str):
        if self.verbose:
            self._print(message, LogLevel.INFO)

    def success(self, message: str):
        self._print(message, LogLevel.SUCCESS)

    def warning(self, message: str):
        self._print(message, LogLevel.WARNING)

    def error(self, message: str):
        self._print(message, LogLevel.ERROR)

    def debug(self, message: str):
        if self.verbose:
            self._print(message, LogLevel.DEBUG)

    def _print(self, message: str, level: LogLevel):
        color_map = {
        LogLevel.INFO: typer.colors.BLUE,LogLevel.SUCCESS: typer.colors.GREEN,LogLevel.WARNING: typer.colors.YELLOW,
        LogLevel.ERROR: typer.colors.RED,LogLevel.DEBUG: typer.colors.MAGENTA,
        }

        typer.secho(message, fg=color_map.get(level, typer.colors.WHITE))