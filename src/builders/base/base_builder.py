from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
from ..utils.file_system import FileSystem


class BaseBuilder(ABC):
    """ Base class for all CLI builders. Defines standard contract and common utilities. """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.fs = FileSystem()


    def validate_path(self):
        """ Ensures that the base directory exists. """
        if not self.base_path.exists():
            raise FileNotFoundError(f"Base path '{self.base_path}' does not exist.")

    def ensure_structure(self, folders: List[Path]):
        """ Creates multiple folders. """
        for folder in folders:
            self.fs.create_dir(folder)

    def create_file(self, path: Path, content: str):
        """ Wrapper for creating a file. """
        self.fs.create_file(path, content)

    def append_file(self, path: Path, content: str):
        """ Wrapper for appending content. """
        self.fs.append_to_file(path, content)

    def install_dependencies(self, dependencies: List[str]):
        """ Install dependencies in the project. """
        self.fs.install_dependencies(dependencies)

    @abstractmethod
    def build(self):
        """ The main method that executes the construction. It must be implemented by all builders. """
        pass

    def before_build(self):
        """ Hook executed before build. Can be overridden. """
        pass

    def after_build(self):
        """ Hook executed after build. Can be overridden. """
        pass

    def run(self):
        """ Standard method that executes a complete cycle. Should not be overridden. """
        self.validate_path()
        self.before_build()
        self.build()
        self.after_build()