from dataclasses import dataclass

from http_client import ApiClient
from services import (
    BatchImportService,
    FactionImportService,
    JobImportService,
    MonsterImportService,
    NpcImportService,
    PcImportService,
)


@dataclass(frozen=True)
class ImportContext:
    api_client: ApiClient
    batch_import_service: BatchImportService
    faction_import_service: FactionImportService
    job_import_service: JobImportService
    monster_import_service: MonsterImportService
    npc_import_service: NpcImportService
    pc_import_service: PcImportService