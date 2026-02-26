def pyproject_template(name:str ) -> str:
    return f"""
[project]
name = "{name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "aiofiles>=25.1.0",
    "alembic>=1.18.4",
    "asyncpg>=0.31.0",
    "bcrypt>=5.0.0",
    "email-validator>=2.3.0",
    "fastapi>=0.131.0",
    "passlib[bcrypt]>=1.7.4",
    "psycopg2>=2.9.11",
    "pydantic>=2.12.5",
    "pydantic-settings>=2.13.1",
    "python-jose[cryptography]>=3.5.0",
    "python-multipart>=0.0.22",
    "sqlalchemy>=2.0.46",
    "uvicorn>=0.41.0",
]

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

[tool.setuptools]
package-dir = {{"" = "src"}}

[tool.setuptools.packages.find]
where = ["src"]

"""