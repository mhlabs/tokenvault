"""Token router."""
import hashlib
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse

from tokenvaultapi.schemas.token import (RemoteFunctionTokenRequest,
                                         RemoteFunctionTokenResponse, Token,
                                         TokenCreate, TokenFind)
from tokenvaultapi.services.token import TokenService

router = APIRouter()
token_service = TokenService()


def create_uuid_from_list(_list: list) -> str:
    """Create a UUID from a list of values."""
    val = " ".join(map(str, _list))
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(UUID(hex=hex_string))


def create_uuid_from_string(val: str) -> str:
    """Create a UUID from a string."""
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(UUID(hex=hex_string))


@router.post("/", response_model=RemoteFunctionTokenResponse, tags=["token"])
async def batch_token(
    batch: RemoteFunctionTokenRequest = Body(...),
) -> RemoteFunctionTokenResponse:
    """Batch tokenization."""
    try:
        return await token_service.remote_function_request(batch)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.post("/token", response_model=Token, tags=["token"])
async def create_token(token_create: TokenCreate = Body(...)) -> Token:
    """Create a multi-use token."""
    token_create.pk = create_uuid_from_list(
        [
            token_create.identifier,
            token_create.identity,
            token_create.value,
            token_create.field,
        ]
    )
    return await token_service.create_token(token_create)


@router.get("/token/{pk}", response_model=Token, tags=["token"])
async def get_token(pk: str) -> Token:
    """Get a token by primary key."""
    token = await token_service.get_token(pk)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    return token


@router.get(
    "/token/identifier/{identifier}/identity/{identity}/value/{value}",
    response_model=Token,
    tags=["token"],
)
async def get_token_by_value(identifier: str, identity: str, value: str) -> Token:
    """Get a token by identifier, identity, and value."""
    pk = create_uuid_from_list([identifier, identity, value])
    token = await token_service.get_token(pk)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    return token


@router.get(
    "/token/identifier/{identifier}/identity/{identity}/value/{value}/field/{field}",
    response_model=Token,
    tags=["token"],
)
async def get_token_by_value_field(
    identifier: str, identity: str, value: str, field: str
) -> Token:
    """Get a token by identifier, identity, value, and field."""
    pk = create_uuid_from_list([identifier, identity, value, field])
    token = await token_service.get_token(pk)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    return token


@router.post("/token/find", response_model=Token, tags=["token"])
async def get_token_by_identifier(token_find: TokenFind = Body(...)) -> Token:
    """Find a token by identifier, identity, and token."""
    token = await token_service.find_token(token_find)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    return token


@router.get(
    "/tokens/identifier/{identifier}/identity/{identity}",
    response_model=List[Token],
    tags=["token"],
)
async def list_tokens(identifier: str, identity: str) -> List[Token]:
    """List all tokens for an identifier and identity."""
    tokens = await token_service.list_tokens(identifier, identity)
    if not tokens:
        raise HTTPException(status_code=404, detail="Tokens not found.")
    return tokens


@router.delete(
    "/token/value/{value}/identifier/{identifier}/identity/{identity}",
    status_code=204,
    tags=["token"],
)
async def delete_token_by_value(identifier: str, identity: str, value: str):
    """Delete a token."""
    pk = create_uuid_from_list([identifier, identity, value])
    token = await token_service.get_token(pk)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    await token_service.delete_token(pk)


@router.delete("/token/{pk}", status_code=204, tags=["token"])
async def delete_token(pk: str):
    """Delete a token."""
    token = await token_service.get_token(pk)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    await token_service.delete_token(pk)


@router.delete(
    "/tokens/identifier/{identifier}/identity/{identity}",
    status_code=204,
    tags=["token"],
)
async def delete_tokens(identifier: str, identity: str):
    """Delete all tokens for an identifier and identity."""
    tokens = await token_service.list_tokens(identifier, identity)
    if not tokens:
        raise HTTPException(status_code=404, detail="Tokens not found.")
    for token in tokens:
        await token_service.delete_token(token.pk)
