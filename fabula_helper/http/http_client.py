import time
from typing import Any

import requests

from fabula_helper.http.api_result import ApiPostResult
from fabula_helper.config.config import Settings


class ApiClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._session = requests.Session()

    def post(
        self,
        path: str,
        body: dict[str, Any],
        identifier: str,
        params: dict[str, Any] | None = None,
    ) -> ApiPostResult:
        try:
            response = self._session.post(
                self._url(path),
                headers=self._headers(authenticated=True),
                json=body,
                params=params,
                timeout=self._settings.request_timeout_seconds,
            )

            if response.status_code in (200, 201, 204):
                return ApiPostResult(
                    status_code=response.status_code,
                    created=True,
                    already_exists=False,
                    error=False,
                )

            if response.status_code == 409:
                return ApiPostResult(
                    status_code=response.status_code,
                    created=False,
                    already_exists=True,
                    error=False,
                )

            message = (
                f"Falha ao importar {identifier}: "
                f"{response.status_code} - {response.text}"
            )

            return ApiPostResult(
                status_code=response.status_code,
                created=False,
                already_exists=False,
                error=True,
                error_message=message,
            )

        except requests.RequestException as error:
            return ApiPostResult(
                status_code=None,
                created=False,
                already_exists=False,
                error=True,
                error_message=f"Falha HTTP ao importar {identifier}: {error}",
            )

        finally:
            time.sleep(self._settings.request_delay_seconds)

    def get_public_items(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/items",
            label="items",
            authenticated=True,
        )

    def get_public_pcs(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/pcs/summary",
            label="pcs",
            authenticated=True,
        )

    def get_public_npcs(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/npcs/summary",
            label="npcs",
            authenticated=True,
        )

    def get_public_monsters(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/monsters/summary",
            label="monsters",
        )

    def get_public_arcanas(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/arcanas",
            label="arcanas",
        )

    def get_public_spells(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/spells",
            label="spells",
        )

    def get_public_monsters_actions(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/monsters/actions",
            label="monster actions",
            params={"include": "spell"},
        )

    def get_public_powers(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/powers",
            label="powers",
        )

    def get_public_jobs(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/jobs",
            label="jobs",
        )

    def get_public_locations(self) -> list[dict[str, Any]]:
        return self._get_public_list(
            path="public/locations",
            label="locations",
        )

    def _get_public_list(
        self,
        path: str,
        label: str,
        params: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> list[dict[str, Any]]:
        try:
            response = self._session.get(
                self._url(path),
                headers=self._headers(authenticated=authenticated),
                params=params,
                timeout=self._settings.request_timeout_seconds,
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Falha ao recuperar {label}: "
                    f"{response.status_code} - {response.text}"
                )

            response_json = response.json()
            data = response_json.get("data")

            if not isinstance(data, list):
                raise RuntimeError(
                    f"Resposta inválida ao recuperar {label}: campo 'data' não é uma lista."
                )

            return data

        except requests.RequestException as error:
            raise RuntimeError(f"Falha HTTP ao recuperar {label}.") from error

        finally:
            time.sleep(self._settings.request_delay_seconds)

    def _url(self, path: str) -> str:
        return f"{self._settings.api_base_url}/{path.lstrip('/')}"

    def _headers(self, authenticated: bool) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}

        if authenticated:
            if not self._settings.token:
                raise RuntimeError("TOKEN não configurado para chamada autenticada.")

            headers["Authorization"] = f"Bearer {self._settings.token}"

        return headers