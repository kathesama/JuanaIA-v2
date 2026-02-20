from schemas.downstream import FinanzasProyeccionResponse
from common.http_client import HttpClient


class FinanzasClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def proyeccion(
        self,
        *,
        correlation_id: str,
        aporte_mensual_usd: float,
        tasa_anual_real: float,
        anios: int,
    ) -> dict:
        payload = {
            "aporte_mensual_usd": aporte_mensual_usd,
            "tasa_anual_real": tasa_anual_real,
            "anios": anios,
        }
        resp = self._http.post("/proyeccion", correlation_id=correlation_id, json=payload)
        data = FinanzasProyeccionResponse.model_validate(resp)
        return data.model_dump()
