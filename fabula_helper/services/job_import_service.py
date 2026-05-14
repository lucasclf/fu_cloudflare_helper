from fabula_helper.importers.import_report import ImportBatchReport
from fabula_helper.http.http_client import ApiClient
from fabula_helper.normalizers import build_id_map
from fabula_helper.normalizers.job_normalizer import JobNormalizer
from fabula_helper.definitions.request_definitions import ImportDefinition
from fabula_helper.services.batch_import_service import BatchImportService


class JobImportService:
    def __init__(
        self,
        api_client: ApiClient,
        batch_import_service: BatchImportService,
        job_normalizer: JobNormalizer,
    ) -> None:
        self._api_client = api_client
        self._batch_import_service = batch_import_service
        self._job_normalizer = job_normalizer

    def create_jobs_with_dependencies(
        self,
        job_definition: ImportDefinition,
        question_definition: ImportDefinition,
        alias_definition: ImportDefinition,
        power_definition: ImportDefinition,
        spell_definition: ImportDefinition,
    ) -> list[ImportBatchReport]:
        reports: list[ImportBatchReport] = []

        reports.append(
            self._batch_import_service.import_from_definition(
                job_definition,
                label="jobs",
            )
        )

        jobs = self._api_client.get_public_jobs()
        normalized_jobs = build_id_map(jobs, "Job")

        normalized_questions = self._job_normalizer.replace_job_name_by_id(
            normalized_jobs=normalized_jobs,
            definition=question_definition,
            field_name="job_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=question_definition.path,
                identifier_field=question_definition.identifier,
                items=normalized_questions,
                params={"nature": "job"},
                label="job questions",
            )
        )

        normalized_alias = self._job_normalizer.replace_job_name_by_id(
            normalized_jobs=normalized_jobs,
            definition=alias_definition,
            field_name="job_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=alias_definition.path,
                identifier_field=alias_definition.identifier,
                items=normalized_alias,
                params={"nature": "job"},
                label="job aliases",
            )
        )

        normalized_powers = self._job_normalizer.replace_job_names_by_ids(
            normalized_jobs=normalized_jobs,
            definition=power_definition,
            field_name="job_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=power_definition.path,
                identifier_field=power_definition.identifier,
                items=normalized_powers,
                params={"nature": "job"},
                label="job powers",
            )
        )

        normalized_spells = self._job_normalizer.replace_job_name_by_id(
            normalized_jobs=normalized_jobs,
            definition=spell_definition,
            field_name="job_id",
        )
        reports.append(
            self._batch_import_service.import_items(
                path=spell_definition.path,
                identifier_field=spell_definition.identifier,
                items=normalized_spells,
                params={"nature": "job"},
                label="job spells",
            )
        )

        return reports