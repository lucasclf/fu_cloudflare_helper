import json
from typing import Any


def build_id_map(
    entities: list[dict[str, Any]],
    entity_label: str,
    name_field: str = "name",
    id_field: str = "id",
) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for entity in entities:
        name = entity.get(name_field)
        entity_id = entity.get(id_field)

        if not isinstance(name, str) or not name.strip():
            raise RuntimeError(
                _build_invalid_entity_error(
                    entity_label=entity_label,
                    reason=f"campo '{name_field}' inválido",
                    entity=entity,
                )
            )

        if entity_id is None:
            raise RuntimeError(
                _build_invalid_entity_error(
                    entity_label=entity_label,
                    reason=f"campo '{id_field}' ausente ou nulo",
                    entity=entity,
                )
            )

        normalized[name] = entity_id

    return normalized


def replace_field_name_by_id(
    normalized_map: dict[str, Any],
    items: list[dict[str, Any]],
    field_name: str,
    error_label: str,
) -> list[dict[str, Any]]:
    for index, item in enumerate(items):
        field_value = item.get(field_name)

        if field_value is None:
            raise RuntimeError(
                _build_missing_field_error(
                    field_name=field_name,
                    error_label=error_label,
                    index=index,
                    item=item,
                )
            )

        if not isinstance(field_value, str):
            raise RuntimeError(
                _build_invalid_field_error(
                    field_name=field_name,
                    field_value=field_value,
                    expected_type="string",
                    error_label=error_label,
                    index=index,
                    item=item,
                )
            )

        if not field_value.strip():
            raise RuntimeError(
                _build_invalid_field_error(
                    field_name=field_name,
                    field_value=field_value,
                    expected_type="string não vazia",
                    error_label=error_label,
                    index=index,
                    item=item,
                )
            )

        entity_id = normalized_map.get(field_value)

        if entity_id is None:
            raise RuntimeError(
                _build_not_found_error(
                    field_name=field_name,
                    field_value=field_value,
                    error_label=error_label,
                    normalized_map=normalized_map,
                    index=index,
                    item=item,
                )
            )

        item[field_name] = entity_id

    return items


def replace_optional_field_name_by_id(
    normalized_map: dict[str, Any],
    items: list[dict[str, Any]],
    field_name: str,
    error_label: str,
) -> list[dict[str, Any]]:
    for index, item in enumerate(items):
        field_value = item.get(field_name)

        if field_value is None:
            continue

        if not isinstance(field_value, str):
            raise RuntimeError(
                _build_invalid_field_error(
                    field_name=field_name,
                    field_value=field_value,
                    expected_type="string ou null",
                    error_label=error_label,
                    index=index,
                    item=item,
                )
            )

        if not field_value.strip():
            raise RuntimeError(
                _build_invalid_field_error(
                    field_name=field_name,
                    field_value=field_value,
                    expected_type="string não vazia ou null",
                    error_label=error_label,
                    index=index,
                    item=item,
                )
            )

        entity_id = normalized_map.get(field_value)

        if entity_id is None:
            raise RuntimeError(
                _build_not_found_error(
                    field_name=field_name,
                    field_value=field_value,
                    error_label=error_label,
                    normalized_map=normalized_map,
                    index=index,
                    item=item,
                )
            )

        item[field_name] = entity_id

    return items


def _build_invalid_entity_error(
    entity_label: str,
    reason: str,
    entity: dict[str, Any],
) -> str:
    return (
        f"{entity_label} inválido retornado pela API.\n"
        f"Motivo: {reason}.\n"
        f"Entidade recebida:\n{_format_json(entity)}"
    )


def _build_missing_field_error(
    field_name: str,
    error_label: str,
    index: int,
    item: dict[str, Any],
) -> str:
    return (
        f"{error_label} não pôde ser normalizado.\n"
        f"Motivo: campo obrigatório ausente ou nulo.\n"
        f"Campo esperado: {field_name}\n"
        f"Índice do item no JSON: {index}\n"
        f"Item completo:\n{_format_json(item)}"
    )


def _build_invalid_field_error(
    field_name: str,
    field_value: Any,
    expected_type: str,
    error_label: str,
    index: int,
    item: dict[str, Any],
) -> str:
    return (
        f"{error_label} não pôde ser normalizado.\n"
        f"Motivo: campo com tipo ou valor inválido.\n"
        f"Campo: {field_name}\n"
        f"Valor recebido: {field_value!r}\n"
        f"Tipo recebido: {type(field_value).__name__}\n"
        f"Valor esperado: {expected_type}\n"
        f"Índice do item no JSON: {index}\n"
        f"Item completo:\n{_format_json(item)}"
    )


def _build_not_found_error(
    field_name: str,
    field_value: str,
    error_label: str,
    normalized_map: dict[str, Any],
    index: int,
    item: dict[str, Any],
) -> str:
    available_keys = _format_available_keys(normalized_map)

    return (
        f"{error_label} não encontrado no mapa de IDs.\n"
        f"Campo: {field_name}\n"
        f"Valor procurado: {field_value}\n"
        f"Índice do item no JSON: {index}\n"
        f"Chaves disponíveis no mapa: {available_keys}\n"
        f"Item completo:\n{_format_json(item)}"
    )


def _format_available_keys(
    normalized_map: dict[str, Any],
    limit: int = 20,
) -> str:
    keys = list(normalized_map.keys())

    if not keys:
        return "nenhuma chave disponível"

    preview = keys[:limit]
    formatted_preview = ", ".join(preview)

    if len(keys) > limit:
        remaining = len(keys) - limit
        return f"{formatted_preview} ... (+{remaining} outras)"

    return formatted_preview


def _format_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        default=str,
    )