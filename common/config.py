import os
from dataclasses import dataclass

@dataclass(frozen=True)
class ServiceConfig:
    name: str
    base_url: str

@dataclass(frozen=True)
class AppConfig:
    env: str
    log_level: str
    timeout_seconds: float
    llm: ServiceConfig
    memory: ServiceConfig
    finanzas: ServiceConfig
    tts: ServiceConfig


def load_config() -> AppConfig:
    env = os.getenv("APP_ENV", "dev")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    timeout_seconds = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10"))

    llm_url = os.getenv("LLM_URL", "http://llm:8001")
    mem_url = os.getenv("MEM_URL", "http://memory:8002")
    fin_url = os.getenv("FIN_URL", "http://finanzas:8003")
    tts_url = os.getenv("TTS_URL", "http://tts:8004")

    return AppConfig(
        env=env,
        log_level=log_level,
        timeout_seconds=timeout_seconds,
        llm=ServiceConfig(name="llm", base_url=llm_url),
        memory=ServiceConfig(name="memory", base_url=mem_url),
        finanzas=ServiceConfig(name="finanzas", base_url=fin_url),
        tts=ServiceConfig(name="tts", base_url=tts_url),
    )
