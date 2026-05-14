from typing import Any

from fabula_helper.utils.json_loader import load_json_array
from fabula_helper.normalizers.common import replace_field_name_by_id
from fabula_helper.definitions.request_definitions import ImportDefinition


class JobNormalizer:
    def replace_job_name_by_id(
        self,
        normalized_jobs: dict[str, Any],
        definition: ImportDefinition,
        field_name: str,
    ) -> list[dict[str, Any]]:
        items = load_json_array(definition.json_file)

        return replace_field_name_by_id(
            normalized_map=normalized_jobs,
            items=items,
            field_name=field_name,
            error_label="Classe",
        )

    def replace_job_names_by_ids(
        self,
        normalized_jobs: dict[str, Any],
        definition: ImportDefinition,
        field_name: str,
    ) -> list[dict[str, Any]]:
        items = load_json_array(definition.json_file)

        for index, item in enumerate(items):
            job_names = item.get(field_name)

            if not isinstance(job_names, list):
                raise RuntimeError(
                    f"{field_name} inválido, esperado array.\n"
                    f"Índice do item no JSON: {index}\n"
                    f"Valor recebido: {job_names!r}\n"
                    f"Item completo: {item}"
                )

            normalized_job_ids = []

            for job_name in job_names:
                if not isinstance(job_name, str):
                    raise RuntimeError(
                        f"{field_name} inválido dentro do array.\n"
                        f"Índice do item no JSON: {index}\n"
                        f"Valor recebido: {job_name!r}\n"
                        f"Item completo: {item}"
                    )

                job_id = normalized_jobs.get(job_name)

                if job_id is None:
                    raise RuntimeError(
                        f"Classe não encontrada no mapa de jobs.\n"
                        f"Valor procurado: {job_name}\n"
                        f"Índice do item no JSON: {index}\n"
                        f"Item completo: {item}"
                    )

                normalized_job_ids.append(job_id)

            item[field_name] = normalized_job_ids

        return items