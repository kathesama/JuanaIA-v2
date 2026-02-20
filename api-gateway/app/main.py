from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from common.config import load_config
from common.errors import AppError
from common.logging import configure_logging
from common.http_client import HttpClient
from orchestrator.engine import Orchestrator
from usecases.ask import AskUseCase
from clients.finanzas_client import FinanzasClient
from clients.llm_client import LLMClient
from clients.memory_client import MemoryClient
from clients.tts_client import TTSClient
from routes.ask import router as ask_router
from routes.health import router as health_router
from routes.memory import router as memory_router


def create_app() -> FastAPI:
    config = load_config()
    configure_logging("api-gateway")

    app = FastAPI(title="JuanaIA API Gateway")

    memory_client = MemoryClient(HttpClient(base_url=config.memory.base_url, timeout_seconds=config.timeout_seconds))
    llm_client = LLMClient(HttpClient(base_url=config.llm.base_url, timeout_seconds=config.timeout_seconds))
    finanzas_client = FinanzasClient(HttpClient(base_url=config.finanzas.base_url, timeout_seconds=config.timeout_seconds))
    tts_client = TTSClient(HttpClient(base_url=config.tts.base_url, timeout_seconds=config.timeout_seconds))

    orchestrator = Orchestrator(
        memory_client=memory_client,
        finanzas_client=finanzas_client,
        llm_client=llm_client,
        tts_client=tts_client,
    )

    app.state.ask_usecase = AskUseCase(orchestrator)

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception):
        err = AppError(code="internal_error", message="Unhandled error", status_code=500, details={"error": str(exc)})
        return JSONResponse(status_code=err.status_code, content=err.to_dict())

    app.include_router(health_router)
    app.include_router(ask_router)
    app.include_router(memory_router)

    return app


app = create_app()
