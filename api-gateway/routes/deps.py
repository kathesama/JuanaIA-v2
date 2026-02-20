from uuid import uuid4

from fastapi import Request

from usecases.ask import AskUseCase


def get_ask_usecase(request: Request) -> AskUseCase:
    return request.app.state.ask_usecase


def get_correlation_id(request: Request) -> str:
    correlation_id = request.headers.get("X-Correlation-Id")
    return correlation_id or str(uuid4())
