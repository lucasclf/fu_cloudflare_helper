from collections.abc import Callable
from dataclasses import dataclass

from import_report import ImportBatchReport
from import_targets import ImportTarget


ImportTask = Callable[[], list[ImportBatchReport]]


@dataclass(frozen=True)
class ImportStep:
    target: ImportTarget
    label: str
    description: str
    handler: ImportTask