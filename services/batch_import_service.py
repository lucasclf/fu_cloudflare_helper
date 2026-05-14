import logging
from typing import Any

from console_progress import ConsoleProgress
from http_client import ApiClient
from import_report import ImportBatchReport, ImportItemError
from json_loader import load_json_array
from request_definitions import ImportDefinition


logger = logging.getLogger(__name__)


class BatchImportService:
    def __init__(self, api_client: ApiClient) -> None:
        self._api_client = api_client

    def import_from_definition(
        self,
        definition: ImportDefinition,
        params: dict[str, Any] | None = None,
        label: str | None = None,
    ) -> ImportBatchReport:
        items = load_json_array(definition.json_file)

        return self.import_items(
            path=definition.path,
            identifier_field=definition.identifier,
            items=items,
            params=params,
            label=label,
        )

    def import_items(
        self,
        path: str,
        identifier_field: str,
        items: list[dict[str, Any]],
        params: dict[str, Any] | None = None,
        label: str | None = None,
    ) -> ImportBatchReport:
        import_label = label or path

        total = len(items)
        created = 0
        already_exists = 0
        errors: list[ImportItemError] = []

        progress = ConsoleProgress(
            total=total,
            label=import_label,
        )

        for index, item in enumerate(items, start=1):
            identifier = str(item.get(identifier_field, "sem nome"))

            result = self._api_client.post(
                path=path,
                body=item,
                identifier=identifier,
                params=params,
            )

            if result.created:
                created += 1

            elif result.already_exists:
                already_exists += 1

            elif result.error:
                error = ImportItemError(
                    identifier=identifier,
                    status_code=result.status_code,
                    message=result.error_message or "Erro desconhecido.",
                )
                errors.append(error)

                logger.error(
                    "Erro ao importar %s | path=%s | status=%s | erro=%s",
                    identifier,
                    path,
                    result.status_code,
                    result.error_message,
                )

            progress.update(index)

        progress.finish()

        return ImportBatchReport(
            label=import_label,
            path=path,
            total=total,
            created=created,
            already_exists=already_exists,
            errors=errors,
        )