from typing import Any

from json_loader import load_json_array
from normalizers.common import replace_field_name_by_id
from request_definitions import ImportDefinition


class MonsterNormalizer:
    def replace_monster_name_by_id(
        self,
        normalized_monsters: dict[str, Any],
        definition: ImportDefinition,
        field_name: str,
    ) -> list[dict[str, Any]]:
        items = load_json_array(definition.json_file)

        return replace_field_name_by_id(
            normalized_map=normalized_monsters,
            items=items,
            field_name=field_name,
            error_label="Monstro",
        )