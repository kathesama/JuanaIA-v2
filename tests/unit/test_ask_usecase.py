from orchestrator.schemas import OrchestratorResult
from usecases.ask import AskUseCase


class FakeOrchestrator:
    def __init__(self):
        self.called = False
        self.last_args = None

    def run_ask_flow(self, pregunta, context, extras, correlation_id):
        self.called = True
        self.last_args = {
            "pregunta": pregunta,
            "context": context,
            "extras": extras,
            "correlation_id": correlation_id,
        }
        return OrchestratorResult(
            respuesta_texto="ok",
            audio={"status": "generated"},
            contexto_usado=["a"],
            proyeccion=None,
        )


def test_ask_usecase_calls_orchestrator():
    fake = FakeOrchestrator()
    usecase = AskUseCase(fake)

    result = usecase.execute(
        pregunta="hola",
        aporte_mensual_usd=10.0,
        tasa_real_anual=0.05,
        anios=2,
        full=False,
        correlation_id="cid-9",
    )

    assert fake.called is True
    assert result.respuesta_texto == "ok"
    assert fake.last_args["extras"]["aporte_mensual_usd"] == 10.0
