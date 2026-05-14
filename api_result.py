from dataclasses import dataclass


@dataclass(frozen=True)
class ApiPostResult:
    status_code: int | None
    created: bool
    already_exists: bool
    error: bool
    error_message: str | None = None