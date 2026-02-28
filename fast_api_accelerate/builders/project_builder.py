from pathlib import Path
from .base import BaseBuilder
from ..templates.projects import config_database_template, setup_db_template, readme_template, main_project_template, pyproject_template, base_repository_template, base_service_template, all_models_template, config_conection_template, config_container_ioc_template, startup_template 
from ..templates.modules import client_type_template, auth_service_template, auth_controller_template, user_model_template
from ..templates.schemas import  init_dtos_template
from ..utils.file_system import FileSystem

class ProjectBuilder(BaseBuilder):
    """Builder principal responsável por criar a aplicação base completa: FastAPI, core, base, modules, database e auth."""
    FILE_INIT:str = "__init__.py"
    FILE_DATABASE:str = "database.py"

    def __init__(self, base_path: Path, project_name: str, with_database: bool = True, with_auth: bool = True):
        super().__init__(base_path)
        self.project_name = project_name
        self.project_path = (self.base_path / project_name).resolve()
        self.fs = FileSystem(self.project_path)

        self.with_database = with_database
        self.with_auth = with_auth

        # Paths principais
        self.src_path = self.project_path / "src"
        self.core_path = self.src_path / "core"
        self.base_path_pkg = self.src_path / "base"
        self.models_path = self.src_path / "models"
        self.modules_path = self.src_path / "modules"

    def _create_project_root(self):
        self.ensure_structure([self.project_path])

    def _create_app_structure(self):
        folders = [self.src_path, self.core_path, self.base_path_pkg, self.models_path, self.modules_path]
        self.ensure_structure(folders)
        for folder in folders:
            self.create_file(folder / self.FILE_INIT, "")

    def _create_main_file(self):
        self.create_file(self.src_path.parent / "main.py",main_project_template(name=self.project_name))

    def _create_pyproject(self):
        self.create_file(self.project_path / "pyproject.toml",pyproject_template(name=self.project_name))

    def _create_readme(self):
        self.create_file(self.project_path / "README.md", readme_template(name=self.project_name))

    def _create_setup_db(self):
        if self.with_database:
            self.create_file(self.project_path / "setup_db.py", setup_db_template())

    def _create_core_files(self):
        files = ["configs.py", "container_ioc.py", self.FILE_DATABASE, "startup.py", self.FILE_INIT]
        for f in files:
            self.create_file(self.core_path / f, "")

    def _configure_database(self):
        db_file = self.core_path / self.FILE_DATABASE
        self.update_file(db_file, config_database_template())

    def _create_config_conection(self):
        config_file = self.core_path / "configs.py"
        self.update_file(config_file, config_conection_template())
    
    def _create_container_ioc_conection(self):
        container_ioc_file = self.core_path / "container_ioc.py"
        self.update_file(container_ioc_file, config_container_ioc_template())

    def _create_startup_app(self):
        startup_file = self.core_path / "startup.py"
        self.update_file(startup_file, startup_template())

    def _create_base_files(self):
        self.create_file(self.base_path_pkg / "base_repository.py", base_repository_template())
        self.create_file(self.base_path_pkg / "base_service.py", base_service_template())

    def _create_models(self):
        self.create_file(self.models_path / "__all_models.py", all_models_template())
        self.create_file(self.models_path / "user.py", user_model_template())

    def _create_users_module(self):
        module_path = self.modules_path / "users"
        self.ensure_structure([module_path])
        for sub in ["controllers", "services", "repositories", "dtos"]:
            self.ensure_structure([module_path / sub])
            self.create_file(module_path / sub / self.FILE_INIT, "")
        self.create_file(module_path / self.FILE_INIT, "")

    def _create_auth_module(self):
        module_path = self.modules_path / "auth"
        
        # Cria a estrutura base
        submodules = ["controllers", "services", "dtos", "utils"]
        for sub in submodules:
            path = module_path / sub
            self.ensure_structure([path])
            
        # utils/__init__.py
        utils_init = module_path / "utils" / self.FILE_INIT
        self.create_file(utils_init,"from .client_type import ClientType\n\n__all__ = ['ClientType']")
        # utils/client_type.py
        self.create_file(module_path / "utils" / "client_type.py", client_type_template())

        # services/__init__.py
        services_init = module_path / "services" / self.FILE_INIT
        self.create_file(services_init,"from .auth_service import AuthService\n\n__all__ = ['AuthService']")
        # services/auth_service.py
        self.create_file(module_path / "services" / "auth_service.py", auth_service_template())

        # dtos/__init__.py
        dtos_init = module_path / "dtos" / self.FILE_INIT
        self.create_file(dtos_init, init_dtos_template() )
        # dtos templates
        for dto in ["login", "refresh", "token", "refreshrequest"]:
            self.create_file(module_path / "dtos" / f"{dto}.py", f"# Defina a classe {dto.capitalize()} aqui")

        # controllers/__init__.py
        controllers_init = module_path / "controllers" / self.FILE_INIT
        self.create_file(controllers_init,"from .auth_controller import AuthController\n\n__all__ = ['AuthController']")
        # controllers/auth_controller.py
        self.create_file(module_path / "controllers" / "auth_controller.py", auth_controller_template())

    def _create_modules(self, additional_modules: list[str] = []):
        """ Cria módulos opcionais (não obrigatórios) com estrutura padrão: controllers, services, repositories e dtos. """
        for module in additional_modules:
            module_path = self.modules_path / module
            self.ensure_structure([module_path])
            for sub in ["controllers", "services", "repositories", "dtos"]:
                sub_path = module_path / sub
                self.ensure_structure([sub_path])
                self.create_file(sub_path / self.FILE_INIT, "")
            self.create_file(module_path / self.FILE_INIT, "")

    def build(self):
        self._create_project_root()
        self._create_app_structure()
        self._create_main_file()
        self._create_pyproject()
        self._create_readme()
        self._create_setup_db()
        self._create_core_files()
        self._configure_database()
        self._create_config_conection()
        self._create_container_ioc_conection()
        self._create_startup_app()
        self._create_base_files()
        self._create_models()
        self._create_modules()

        if self.with_database:
            self._configure_database()

        if self.with_auth:
            self._create_auth_module()

        self._create_users_module()
        self._create_modules(additional_modules=[]) # Módulos opcionais que o usuário quiser

        self.install_dependencies()