"""Token Service"""
from typing import List
from uuid import UUID

from tokenvaultapi.daos.tokens import TokenDAO
from tokenvaultapi.schemas.token import (RemoteFunctionTokenRequest,
                                         RemoteFunctionTokenResponse, Token,
                                         TokenCreate, TokenFind)

token_dao = TokenDAO()


class TokenService:
    """Token Service"""

    async def create_token(self, token_create: TokenCreate) -> Token:
        """Create a token."""
        return await token_dao.create(token_create)

    async def get_token(self, pk: UUID) -> Token:
        """Get a token."""
        return await token_dao.get(pk)

    async def list_tokens(self, identifier: str, identity: str) -> List[Token]:
        """List tokens."""
        return await token_dao.list(identifier, identity)

    async def delete_token(self, pk: UUID) -> UUID:
        """Delete a token."""
        return await token_dao.delete(pk)

    async def find_token(self, token_find: TokenFind) -> Token:
        """Find a token."""
        return await token_dao.find(token_find)

    async def remote_function_request(
        self, request: RemoteFunctionTokenRequest
    ) -> RemoteFunctionTokenResponse:
        """Remote function request. logic for different actions from userdefinedcontext \
        (DEIDENTIFY, REIDENTIFY, etc.)"""
        user_defined_context = request.userDefinedContext
        action = user_defined_context["action"]
        if action == "DEIDENTIFY":
            return await token_dao.deidentify(request)
        if action == "REIDENTIFY":
            return await token_dao.reidentify(request)
        return None
