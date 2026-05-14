from typing import Any

from constants import (
    BOND_TARGET_TYPE_FREEFORM,
    BOND_TARGET_TYPE_MONSTER,
    BOND_TARGET_TYPE_NPC,
    BOND_TARGET_TYPE_PC,
    EQUIPMENT_ITEM_FIELDS,
)
from json_loader import load_json_array
from normalizers.common import (
    replace_field_name_by_id,
    replace_optional_field_name_by_id,
)
from request_definitions import ImportDefinition


class PcNormalizer:
    def replace_pc_name_by_id(
        self,
        normalized_pcs: dict[str, Any],
        definition: ImportDefinition,
        field_name: str,
    ) -> list[dict[str, Any]]:
        items = load_json_array(definition.json_file)

        return replace_field_name_by_id(
            normalized_map=normalized_pcs,
            items=items,
            field_name=field_name,
            error_label="Pc",
        )

    def replace_pc_and_item_names_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_items: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_items,
            items=normalized,
            field_name="item_id",
            error_label="Item",
        )

    def replace_pc_equipment_names_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_items: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        for field_name in EQUIPMENT_ITEM_FIELDS:
            normalized = replace_optional_field_name_by_id(
                normalized_map=normalized_items,
                items=normalized,
                field_name=field_name,
                error_label="Item",
            )

        return normalized

    def replace_pc_job_names_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_jobs: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_jobs,
            items=normalized,
            field_name="job_id",
            error_label="Job",
        )

    def replace_pc_power_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_powers: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_powers,
            items=normalized,
            field_name="power_id",
            error_label="Power",
        )

    def replace_pc_spell_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_spells: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_spells,
            items=normalized,
            field_name="spell_id",
            error_label="Spell",
        )

    def replace_pc_monster_spell_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_monster_spells: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_monster_spells,
            items=normalized,
            field_name="monster_action_id",
            error_label="Monster Spell",
        )

    def replace_pc_arcana_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_arcanas: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        normalized = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        return replace_field_name_by_id(
            normalized_map=normalized_arcanas,
            items=normalized,
            field_name="arcana_id",
            error_label="Arcana",
        )

    def replace_bond_targets_by_ids(
        self,
        normalized_pcs: dict[str, Any],
        normalized_npcs: dict[str, Any],
        normalized_monsters: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        items = self.replace_pc_name_by_id(
            normalized_pcs=normalized_pcs,
            definition=definition,
            field_name="pc_id",
        )

        for item in items:
            target_type = item.get("target_type")
            target_id = item.get("target_id")
            target_name = item.get("target_name")

            if not isinstance(target_type, str):
                raise RuntimeError(f"target_type inválido: {target_type}")

            if target_type == BOND_TARGET_TYPE_PC:
                self._replace_bond_target_id(
                    item=item,
                    target_id=target_id,
                    normalized_map=normalized_pcs,
                    error_label="PC alvo",
                )
                item["target_name"] = None

            elif target_type == BOND_TARGET_TYPE_NPC:
                self._replace_bond_target_id(
                    item=item,
                    target_id=target_id,
                    normalized_map=normalized_npcs,
                    error_label="NPC alvo",
                )
                item["target_name"] = None

            elif target_type == BOND_TARGET_TYPE_MONSTER:
                self._replace_bond_target_id(
                    item=item,
                    target_id=target_id,
                    normalized_map=normalized_monsters,
                    error_label="Monster alvo",
                )
                item["target_name"] = None

            elif target_type == BOND_TARGET_TYPE_FREEFORM:
                if target_id is not None:
                    raise RuntimeError(
                        f"target_id deve ser null quando target_type for freeform: {target_id}"
                    )

                if not isinstance(target_name, str) or not target_name.strip():
                    raise RuntimeError(
                        f"target_name obrigatório quando target_type for freeform: {target_name}"
                    )

                item["target_id"] = None

            else:
                raise RuntimeError(f"target_type inválido: {target_type}")

        return items

    @staticmethod
    def _replace_bond_target_id(
        item: dict[str, Any],
        target_id: Any,
        normalized_map: dict[str, Any],
        error_label: str,
    ) -> None:
        if not isinstance(target_id, str):
            raise RuntimeError(f"target_id inválido para {error_label}: {target_id}")

        normalized_target_id = normalized_map.get(target_id)

        if normalized_target_id is None:
            raise RuntimeError(f"{error_label} não encontrado no mapa: {target_id}")

        item["target_id"] = normalized_target_id