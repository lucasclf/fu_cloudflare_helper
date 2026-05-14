import json
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]


def load_json_array(json_file: str) -> list[JsonObject]:
    path = Path(json_file)

    try:
        content = path.read_text(encoding="utf-8")
        items = json.loads(content)
    except FileNotFoundError as error:
        raise RuntimeError(f"Arquivo JSON não encontrado: {path}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Erro ao ler JSON '{path}': {error}") from error

    if not isinstance(items, list):
        raise RuntimeError(f"O arquivo JSON '{path}' deve conter um array de objetos.")

    if not all(isinstance(item, dict) for item in items):
        raise RuntimeError(f"O arquivo JSON '{path}' deve conter apenas objetos dentro do array.")

    return items
