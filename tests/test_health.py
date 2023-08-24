#from starlette.testclient import TestClient
import pytest
from httpx import AsyncClient
from tokenvaultapi.main import api

#def test_healthcheck(client: TestClient):
#@pytest.fixture(scope="module", autouse=True)
@pytest.mark.anyio
#async def test_healthcheck(async_client: AsyncClient):
async def test_healthcheck():
    async with AsyncClient(app=api, base_url="http://test") as async_client:
        request = await async_client.get("/healthcheck")
    response = request.json()
    assert response.get("message") == "healthy"
    assert response.get("version")
    assert response.get("time")
