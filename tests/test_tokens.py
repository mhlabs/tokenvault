"""Test the tokens API."""
import urllib.parse
from uuid import uuid4
import pytest
from httpx import AsyncClient

from tokenvaultapi.main import api
from tokenvaultapi.schemas.token import RemoteFunctionTokenRequest, TokenCreate

pytestmark = pytest.mark.anyio

mock_create_token = TokenCreate.Config.schema_extra["example"]
mock_deidentiy_tokens = RemoteFunctionTokenRequest.Config.schema_extra["example"]
PK = None

IDENTIFIER = mock_create_token.get("identifier")
IDENTITY = mock_create_token.get("identity")

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    #async with LifespanManager(api):
    async with AsyncClient(app=api, base_url="http://test") as c:
        yield c

@pytest.mark.anyio
async def test_no_tokens_by_identifier(client: AsyncClient) -> None:
    """Test that there are no tokens."""
    #async with AsyncClient(app=api, base_url="http://testserver") as async_client:
    response = await client.get(f"/token/identifier/{IDENTIFIER}/identity/{IDENTITY}")
    assert response.status_code == 404

@pytest.mark.anyio
async def test_no_tokens_by_pk(client: AsyncClient) -> None:
    """Test that there are no tokens."""
    #async with AsyncClient(app=api, base_url="http://testserver") as async_client:
    response = await client.get(f"/token/{str(uuid4())}")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_token(client: AsyncClient) -> None:
    """Test that we can create a token."""
    global PK
    #async with AsyncClient(app=api, base_url="http://test") as async_client:
    response = await client.post("/token", json=mock_create_token)
    assert response.status_code == 200
    data = response.json()
    PK = data.get("pk")
    assert data.get("identifier") == IDENTIFIER
    assert data.get("created_at")
    assert data.get("identity") == IDENTITY
    assert data.get("pk")
    assert data.get("token")
    assert data.get("type") == "STRING"
    assert data.get("value")


# async def test_get_token(client: AsyncClient) -> None:
#     """Test that we can get an token."""
#     response = client.get(f"/token/{PK}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data.get("identifier") == "CUSTOMER_ID"
#     assert data.get("created_at")
#     assert data.get("identity") == "12345"
#     assert data.get("pk")
#     assert data.get("token")
#     assert data.get("type") == "STRING"
#     assert data.get("value")
#     print(data)

#     identifier = data.get("identifier")
#     identity = data.get("identity")
#     value = data.get("value")
#     field = data.get("field")
#     response = client.get(
#         f"/token/identifier/{identifier}/identity/{identity}"
#         f"/value/{urllib.parse.quote(value)}/field/{field}"
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data.get("identifier") == "CUSTOMER_ID"
#     assert data.get("created_at")
#     assert data.get("identity") == "12345"
#     assert data.get("pk")
#     assert data.get("token")
#     assert data.get("type") == "STRING"
#     assert data.get("value") == value


# async def test_delete_token() -> None:
#     """Test that we can delete an token."""
#     response = client.delete(f"/token/{PK}")
#     assert response.status_code == 204

@pytest.mark.anyio
async def test_deidentify() -> None:
    """Test that we can create an item."""
    async with AsyncClient(app=api, base_url="http://testserver") as async_client:
        response = await async_client.post("/", json=mock_deidentiy_tokens)
        assert response.status_code == 200
        data = response.json()
        assert data.get("replies")
        print(data)
