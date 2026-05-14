from fabula_helper.importers.import_report import ImportBatchReport
from fabula_helper.http.http_client import ApiClient
from fabula_helper.normalizers import build_id_map
from fabula_helper.normalizers.faction_normalizer import FactionNormalizer
from fabula_helper.definitions.request_definitions import ImportDefinition
from fabula_helper.services.batch_import_service import BatchImportService


class FactionImportService:
    def __init__(
        self,
        api_client: ApiClient,
        batch_import_service: BatchImportService,
        faction_normalizer: FactionNormalizer,
    ) -> None:
        self._api_client = api_client
        self._batch_import_service = batch_import_service
        self._faction_normalizer = faction_normalizer

    def create_entities(
        self,
        faction_definition: ImportDefinition,
    ) -> list[ImportBatchReport]:
        locations = self._api_client.get_public_locations()
        normalized_locations = build_id_map(locations, "Location")

        normalized_factions = self._faction_normalizer.replace_location_names_by_ids(
            normalized_locations=normalized_locations,
            definition=faction_definition,
        )

        return [
            self._batch_import_service.import_items(
                path=faction_definition.path,
                identifier_field=faction_definition.identifier,
                items=normalized_factions,
                label="factions",
            )
        ]