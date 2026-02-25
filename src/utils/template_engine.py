from string import Template
from pathlib import Path
from typing import Dict


class TemplateEngine:
    """ Responsável por renderizar templates da CLI.

        Pode renderizar:
        - Templates em memória (string)
        - Templates de arquivos
    """

    def render_string(self, template_str: str, context: Dict[str, str]) -> str:
        """ Renderiza template a partir de string. """
        template = Template(template_str)
        return template.safe_substitute(**context)

    def render_file(self, template_path: str | Path, context: Dict[str, str]) -> str:
        """ Renderiza template a partir de arquivo. """
        path = Path(template_path)

        if not path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        content = path.read_text(encoding="utf-8")

        return self.render_string(content, context)