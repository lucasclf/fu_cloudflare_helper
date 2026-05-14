from typing import Any

from fabula_helper.utils.json_loader import load_json_array
from fabula_helper.normalizers.common import replace_field_name_by_id
from fabula_helper.definitions.request_definitions import ImportDefinition


class NpcNormalizer:
    def replace_npc_name_by_id(
        self,
        normalized_npcs: dict[str, Any],
        definition: ImportDefinition,
        field_name: str,
    ) -> list[dict[str, Any]]:
        items = load_json_array(definition.json_file)

        return replace_field_name_by_id(
            normalized_map=normalized_npcs,
            items=items,
            field_name=field_name,
            error_label="Npc",
        )

    def replace_npc_and_item_names_by_ids(
        self,
        normalized_npcs: dict[str, Any],
        normalized_items: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_npc_name_by_id(
            normalized_npcs=normalized_npcs,
            definition=definition,
            field_name="npc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_items,
            items=normalized,
            field_name="item_id",
            error_label="Item",
        )