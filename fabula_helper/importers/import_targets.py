from enum import StrEnum


class ImportTarget(StrEnum):
    ALL = "all"
    SESSIONS = "sessions"
    ARCANAS = "arcanas"
    LOCATIONS = "locations"
    FACTIONS = "factions"
    ITEMS = "items"
    JOBS = "jobs"
    MONSTERS = "monsters"
    NPCS = "npcs"
    PCS = "pcs"


IMPORT_TARGETS: tuple[ImportTarget, ...] = (
    ImportTarget.SESSIONS,
    ImportTarget.ARCANAS,
    ImportTarget.LOCATIONS,
    ImportTarget.FACTIONS,
    ImportTarget.ITEMS,
    ImportTarget.JOBS,
    ImportTarget.MONSTERS,
    ImportTarget.NPCS,
    ImportTarget.PCS,
)

ALL_IMPORT_TARGETS: tuple[ImportTarget, ...] = (
    ImportTarget.ALL,
    *IMPORT_TARGETS,
)


def import_target_choices() -> tuple[str, ...]:
    return tuple(target.value for target in ALL_IMPORT_TARGETS)