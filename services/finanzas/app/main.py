from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="juana-finanzas")


class ProyeccionRequest(BaseModel):
    aporte_mensual_usd: float
    tasa_anual_real: float
    anios: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "finanzas"}


@app.post("/proyeccion")
def proyeccion(data: ProyeccionRequest):
    total = data.aporte_mensual_usd * 12 * data.anios * (1 + data.tasa_anual_real)
    return {
        "aporte_mensual_usd": data.aporte_mensual_usd,
        "tasa_anual_real": data.tasa_anual_real,
        "anios": data.anios,
        "monto_estimado_total_usd": total,
    }
