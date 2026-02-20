from common.config import AppConfig, load_config


def get_settings() -> AppConfig:
    return load_config()
