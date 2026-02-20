import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest
import requests


@pytest.mark.integration
def test_docker_compose_smoke():
    if not shutil.which("docker"):
        pytest.skip("docker not available")

    repo_root = Path(__file__).resolve().parents[2]
    compose_file = repo_root / "docker-compose.yml"

    env = os.environ.copy()

    try:
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d", "--build"],
            check=True,
            env=env,
        )

        base_url = "http://localhost:8080"
        deadline = time.time() + 60
        while time.time() < deadline:
            try:
                resp = requests.get(f"{base_url}/health", timeout=2)
                if resp.status_code == 200:
                    break
            except requests.RequestException:
                time.sleep(1)
        else:
            pytest.fail("Gateway health check did not pass in time")

        ask_payload = {"pregunta": "Hola"}
        resp = requests.post(f"{base_url}/ask", json=ask_payload, timeout=5)
        assert resp.status_code == 200
        body = resp.json()
        assert "respuesta" in body or "respuesta_texto" in body
    finally:
        subprocess.run(["docker", "compose", "-f", str(compose_file), "down", "-v"], env=env)
