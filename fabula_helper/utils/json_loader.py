import json
from pathlib import Path
from typing import Any


def load_json_array(json_file: str | Path) -> list[dict[str, Any]]:
    path = Path(json_file)

    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise RuntimeError(f"Arquivo JSON não encontrado: {path}") from error

    try:
        items = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Erro ao ler JSON {path}: {error}") from error

    if not isinstance(items, list):
        raise RuntimeError(f"O arquivo JSON deve conter um array de objetos: {path}")

    return items