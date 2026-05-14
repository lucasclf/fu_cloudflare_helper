from fabula_helper.config.config import Settings
from fabula_helper.http.http_client import ApiClient
from fabula_helper.importers.import_context import ImportContext
from fabula_helper.normalizers.faction_normalizer import FactionNormalizer
from fabula_helper.normalizers.job_normalizer import JobNormalizer
from fabula_helper.normalizers.monster_normalizer import MonsterNormalizer
from fabula_helper.normalizers.npc_normalizer import NpcNormalizer
from fabula_helper.normalizers.pc_normalizer import PcNormalizer
from fabula_helper.services import (
    BatchImportService,
    FactionImportService,
    JobImportService,
    MonsterImportService,
    NpcImportService,
    PcImportService,
)


class ImportContextFactory:
    @staticmethod
    def create(settings: Settings) -> ImportContext:
        api_client = ApiClient(settings)

        batch_import_service = BatchImportService(api_client)

        faction_normalizer = FactionNormalizer()
        job_normalizer = JobNormalizer()
        monster_normalizer = MonsterNormalizer()
        npc_normalizer = NpcNormalizer()
        pc_normalizer = PcNormalizer()

        faction_import_service = FactionImportService(
            api_client=api_client,
            batch_import_service=batch_import_service,
            faction_normalizer=faction_normalizer,
        )

        job_import_service = JobImportService(
            api_client=api_client,
            batch_import_service=batch_import_service,
            job_normalizer=job_normalizer,
        )

        monster_import_service = MonsterImportService(
            api_client=api_client,
            batch_import_service=batch_import_service,
            monster_normalizer=monster_normalizer,
        )

        npc_import_service = NpcImportService(
            api_client=api_client,
            batch_import_service=batch_import_service,
            npc_normalizer=npc_normalizer,
        )

        pc_import_service = PcImportService(
            api_client=api_client,
            batch_import_service=batch_import_service,
            pc_normalizer=pc_normalizer,
        )

        return ImportContext(
            api_client=api_client,
            batch_import_service=batch_import_service,
            faction_import_service=faction_import_service,
            job_import_service=job_import_service,
            monster_import_service=monster_import_service,
            npc_import_service=npc_import_service,
            pc_import_service=pc_import_service,
        )