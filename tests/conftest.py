from starlette.testclient import TestClient
from typing import Generator
import pytest
from httpx import AsyncClient
from asyncio import get_event_loop, get_event_loop_policy

# from tokenvaultapi.database import db
from tokenvaultapi.main import api

# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'

@pytest.fixture()
def client():
    with TestClient(api) as client:
        yield client


@pytest.fixture()
async def async_client() -> Generator:

    async with AsyncClient(app=api, base_url="http://testserver") as async_client:

        yield async_client

@pytest.fixture(scope="session")
async def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope="session", autouse=True)
# def event_loop():

#     loop = get_event_loop()
#     yield loop
#     loop.close()