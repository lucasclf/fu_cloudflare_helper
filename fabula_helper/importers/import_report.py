from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ImportItemError:
    identifier: str
    status_code: int | None
    message: str


@dataclass(frozen=True)
class ImportBatchReport:
    label: str
    path: str
    total: int
    created: int
    already_exists: int
    errors: list[ImportItemError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)


@dataclass(frozen=True)
class ImportStepReport:
    target: str
    label: str
    batches: list[ImportBatchReport]

    @property
    def created(self) -> int:
        return sum(batch.created for batch in self.batches)

    @property
    def already_exists(self) -> int:
        return sum(batch.already_exists for batch in self.batches)

    @property
    def error_count(self) -> int:
        return sum(batch.error_count for batch in self.batches)


@dataclass(frozen=True)
class ImportRunReport:
    started_at: str
    finished_at: str
    only: str
    steps: list[ImportStepReport]

    @property
    def created(self) -> int:
        return sum(step.created for step in self.steps)

    @property
    def already_exists(self) -> int:
        return sum(step.already_exists for step in self.steps)

    @property
    def error_count(self) -> int:
        return sum(step.error_count for step in self.steps)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["summary"] = {
            "created": self.created,
            "already_exists": self.already_exists,
            "errors": self.error_count,
        }
        return data


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")