from import_report import ImportBatchReport
from http_client import ApiClient
from normalizers import build_id_map
from normalizers.monster_normalizer import MonsterNormalizer
from request_definitions import ImportDefinition
from services.batch_import_service import BatchImportService


class MonsterImportService:
    def __init__(
        self,
        api_client: ApiClient,
        batch_import_service: BatchImportService,
        monster_normalizer: MonsterNormalizer,
    ) -> None:
        self._api_client = api_client
        self._batch_import_service = batch_import_service
        self._monster_normalizer = monster_normalizer

    def create_monsters_with_dependencies(
        self,
        monster_definition: ImportDefinition,
        trait_definition: ImportDefinition,
        affinity_definition: ImportDefinition,
        action_definition: ImportDefinition,
    ) -> list[ImportBatchReport]:
        reports: list[ImportBatchReport] = []

        reports.append(
            self._batch_import_service.import_from_definition(
                monster_definition,
                label="monsters",
            )
        )

        monsters = self._api_client.get_public_monsters()
        normalized_monsters = build_id_map(monsters, "Monster")

        normalized_traits = self._monster_normalizer.replace_monster_name_by_id(
            normalized_monsters=normalized_monsters,
            definition=trait_definition,
            field_name="monster_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=trait_definition.path,
                identifier_field=trait_definition.identifier,
                items=normalized_traits,
                label="monster traits",
            )
        )

        normalized_affinity = self._monster_normalizer.replace_monster_name_by_id(
            normalized_monsters=normalized_monsters,
            definition=affinity_definition,
            field_name="monster_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=affinity_definition.path,
                identifier_field=affinity_definition.identifier,
                items=normalized_affinity,
                label="monster affinities",
            )
        )

        normalized_action = self._monster_normalizer.replace_monster_name_by_id(
            normalized_monsters=normalized_monsters,
            definition=action_definition,
            field_name="monster_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=action_definition.path,
                identifier_field=action_definition.identifier,
                items=normalized_action,
                label="monster actions",
            )
        )

        return reports