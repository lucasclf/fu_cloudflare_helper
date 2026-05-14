import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    token: str | None = None
    request_timeout_seconds: int = 30
    request_delay_seconds: float = 0.1


def load_settings() -> Settings:
    load_dotenv()

    api_base_url = os.getenv("API_BASE_URL")
    if not api_base_url:
        raise RuntimeError("Variável de ambiente API_BASE_URL não configurada.")

    token = os.getenv("TOKEN")

    return Settings(
        api_base_url=api_base_url.rstrip("/"),
        token=token,
    )
