from import_report import ImportBatchReport
from http_client import ApiClient
from normalizers import build_id_map
from normalizers.npc_normalizer import NpcNormalizer
from request_definitions import ImportDefinition
from services.batch_import_service import BatchImportService


class NpcImportService:
    def __init__(
        self,
        api_client: ApiClient,
        batch_import_service: BatchImportService,
        npc_normalizer: NpcNormalizer,
    ) -> None:
        self._api_client = api_client
        self._batch_import_service = batch_import_service
        self._npc_normalizer = npc_normalizer

    def create_npcs_with_dependencies(
        self,
        npc_definition: ImportDefinition,
        special_rules_definition: ImportDefinition,
        npc_inventory_definition: ImportDefinition,
        npc_equipment_definition: ImportDefinition,
    ) -> list[ImportBatchReport]:
        reports: list[ImportBatchReport] = []

        reports.append(
            self._batch_import_service.import_from_definition(
                npc_definition,
                label="npcs",
            )
        )

        npcs = self._api_client.get_public_npcs()
        normalized_npcs = build_id_map(npcs, "Npc")

        items = self._api_client.get_public_items()
        normalized_items = build_id_map(items, "Item")

        normalized_special_rules = self._npc_normalizer.replace_npc_name_by_id(
            normalized_npcs=normalized_npcs,
            definition=special_rules_definition,
            field_name="npc_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=special_rules_definition.path,
                identifier_field=special_rules_definition.identifier,
                items=normalized_special_rules,
                label="npc special rules",
            )
        )

        normalized_npc_inventory = self._npc_normalizer.replace_npc_and_item_names_by_ids(
            normalized_npcs=normalized_npcs,
            normalized_items=normalized_items,
            definition=npc_inventory_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=npc_inventory_definition.path,
                identifier_field=npc_inventory_definition.identifier,
                items=normalized_npc_inventory,
                label="npc inventory",
            )
        )

        normalized_npc_equipment = self._npc_normalizer.replace_npc_and_item_names_by_ids(
            normalized_npcs=normalized_npcs,
            normalized_items=normalized_items,
            definition=npc_equipment_definition,
        )
        reports.append(
            self._batch_import_service.import_items(
                path=npc_equipment_definition.path,
                identifier_field=npc_equipment_definition.identifier,
                items=normalized_npc_equipment,
                label="npc equipment",
            )
        )

        return reports