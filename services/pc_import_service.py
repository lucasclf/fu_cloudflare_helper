from import_report import ImportBatchReport
from http_client import ApiClient
from normalizers import build_id_map
from normalizers.pc_normalizer import PcNormalizer
from request_definitions import ImportDefinition
from services.batch_import_service import BatchImportService


class PcImportService:
    def __init__(
        self,
        api_client: ApiClient,
        batch_import_service: BatchImportService,
        pc_normalizer: PcNormalizer,
    ) -> None:
        self._api_client = api_client
        self._batch_import_service = batch_import_service
        self._pc_normalizer = pc_normalizer

    def create_pcs_with_dependencies(
        self,
        pc_definition: ImportDefinition,
        equip_definition: ImportDefinition,
        inventory_definition: ImportDefinition,
        job_definition: ImportDefinition,
        power_definition: ImportDefinition,
        bond_definition: ImportDefinition,
        spell_definition: ImportDefinition,
        arcana_definition: ImportDefinition,
        player_monster_spell_definition: ImportDefinition,
    ) -> list[ImportBatchReport]:
        reports: list[ImportBatchReport] = []

        reports.append(
            self._batch_import_service.import_from_definition(
                pc_definition,
                label="pcs",
            )
        )

        pcs = self._api_client.get_public_pcs()
        items = self._api_client.get_public_items()
        jobs = self._api_client.get_public_jobs()
        powers = self._api_client.get_public_powers()
        spells = self._api_client.get_public_spells()
        monster_spells = self._api_client.get_public_monsters_actions()
        arcanas = self._api_client.get_public_arcanas()
        monsters = self._api_client.get_public_monsters()
        npcs = self._api_client.get_public_npcs()

        normalized_pcs = build_id_map(pcs, "Pc")
        normalized_items = build_id_map(items, "Item")
        normalized_jobs = build_id_map(jobs, "Job")
        normalized_powers = build_id_map(powers, "Power")
        normalized_spells = build_id_map(spells, "Spell")
        normalized_monster_spells = build_id_map(monster_spells, "Monster Spell")
        normalized_arcanas = build_id_map(arcanas, "Arcana")
        normalized_monsters = build_id_map(monsters, "Monster")
        normalized_npcs = build_id_map(npcs, "Npc")

        normalized_inventory = self._pc_normalizer.replace_pc_and_item_names_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_items=normalized_items,
            definition=inventory_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=inventory_definition.path,
                identifier_field=inventory_definition.identifier,
                items=normalized_inventory,
                label="pc inventory",
            )
        )

        normalized_equipment = self._pc_normalizer.replace_pc_equipment_names_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_items=normalized_items,
            definition=equip_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=equip_definition.path,
                identifier_field=equip_definition.identifier,
                items=normalized_equipment,
                label="pc equipment",
            )
        )

        normalized_player_jobs = self._pc_normalizer.replace_pc_job_names_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_jobs=normalized_jobs,
            definition=job_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=job_definition.path,
                identifier_field=job_definition.identifier,
                items=normalized_player_jobs,
                label="pc jobs",
            )
        )

        normalized_player_powers = self._pc_normalizer.replace_pc_power_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_powers=normalized_powers,
            definition=power_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=power_definition.path,
                identifier_field=power_definition.identifier,
                items=normalized_player_powers,
                label="pc powers",
            )
        )

        normalized_player_spells = self._pc_normalizer.replace_pc_spell_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_spells=normalized_spells,
            definition=spell_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=spell_definition.path,
                identifier_field=spell_definition.identifier,
                items=normalized_player_spells,
                label="pc spells",
            )
        )

        normalized_player_monster_spells = self._pc_normalizer.replace_pc_monster_spell_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_monster_spells=normalized_monster_spells,
            definition=player_monster_spell_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=player_monster_spell_definition.path,
                identifier_field=player_monster_spell_definition.identifier,
                items=normalized_player_monster_spells,
                label="pc monster spells",
            )
        )

        normalized_player_arcanas = self._pc_normalizer.replace_pc_arcana_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_arcanas=normalized_arcanas,
            definition=arcana_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=arcana_definition.path,
                identifier_field=arcana_definition.identifier,
                items=normalized_player_arcanas,
                label="pc arcanas",
            )
        )

        normalized_player_bonds = self._pc_normalizer.replace_bond_targets_by_ids(
            normalized_pcs=normalized_pcs,
            normalized_npcs=normalized_npcs,
            normalized_monsters=normalized_monsters,
            definition=bond_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=bond_definition.path,
                identifier_field=bond_definition.identifier,
                items=normalized_player_bonds,
                label="pc bonds",
            )
        )

        return reports