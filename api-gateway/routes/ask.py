from fastapi import APIRouter, Depends, Query, Request

from routes.deps import get_ask_usecase, get_correlation_id
from schemas.ask import AskRequest, AskResponse, AskResponseFull
from usecases.ask import AskUseCase

router = APIRouter()


@router.post("/ask", response_model=AskResponse | AskResponseFull)
def ask(
    request: Request,
    data: AskRequest,
    full: bool = Query(default=False),
    usecase: AskUseCase = Depends(get_ask_usecase),
):
    correlation_id = get_correlation_id(request)
    result = usecase.execute(
        pregunta=data.pregunta,
        aporte_mensual_usd=data.aporteMensualUSD,
        tasa_real_anual=data.tasaRealAnual,
        anios=data.anios,
        full=full,
        correlation_id=correlation_id,
    )

    if full:
        return AskResponseFull(
            respuesta_texto=result.respuesta_texto,
            audio=result.audio or {},
            contexto_usado=result.contexto_usado,
            proyeccion=result.proyeccion,
        )

    return AskResponse(respuesta=result.respuesta_texto)
