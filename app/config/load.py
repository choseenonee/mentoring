import os
from pathlib import Path

from dotenv import load_dotenv

from .model import AppConfig, PostgresConfig


def load_env():
    """
    Загружает .env файл.
    Путь можно переопределить через ENV:
    CONFIG_PATH=/custom/path/.env
    """
    env_path = os.getenv("CONFIG_PATH", ".env")
    env_file = Path(env_path)

    if env_file.exists():
        load_dotenv(env_file)
    else:
        print(f"Config file not found: {env_file.resolve()}")


def load_config() -> AppConfig:
    load_env()

    data = {
        "host": os.environ["POSTGRES_HOST"],
        "port": int(os.environ["POSTGRES_PORT"]),
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "database": os.environ["POSTGRES_DATABASE"],
    }

    timeout = os.environ.get("POSTGRES_TIMEOUT")
    if timeout is not None:
        data["timeout"] = timeout

    postgres = PostgresConfig.model_validate(data)

    return AppConfig(postgres=postgres)
