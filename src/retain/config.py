import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.environ.get("RETAIN_DATABASE_URL", "sqlite:///./retain.db")


settings = Settings()
