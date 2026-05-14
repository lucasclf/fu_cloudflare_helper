from collections.abc import Callable
from dataclasses import dataclass

from fabula_helper.importers.import_report import ImportBatchReport
from fabula_helper.importers.import_targets import ImportTarget


ImportTask = Callable[[], list[ImportBatchReport]]


@dataclass(frozen=True)
class ImportStep:
    target: ImportTarget
    label: str
    description: str
    handler: ImportTask