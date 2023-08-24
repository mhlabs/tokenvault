import hashlib
import string
from random import choice, randint, random
from typing import Any, List
from uuid import UUID

from google.cloud.firestore_v1.base_query import (BaseCompositeFilter,
                                                  FieldFilter)
from google.cloud.firestore_v1.types import StructuredQuery

from tokenvaultapi.database import db
from tokenvaultapi.schemas.token import (RemoteFunctionTokenRequest,
                                         RemoteFunctionTokenResponse, Token,
                                         TokenCreate, TokenFind)


def format_preserving_token(input_string) -> str:
    """Create a token that preserves the format of the input string."""
    token = ""
    last_index = len(input_string) - 1
    for index, char in enumerate(input_string):
        if char.islower() and char.isalpha():
            token += choice(string.ascii_lowercase)
        elif char.isupper() and char.isalpha():
            token += choice(string.ascii_uppercase)
        elif char.isdigit() and index in (0, last_index):
            token += choice("123456789")
        elif char.isdigit():
            token += choice(string.digits)
        else:
            token += char
    return token


def tokenize_value(method: str, data_type: str, val: Any) -> str:
    """Tokenize a value."""
    if method == "FORMAT_PRESERVING" and data_type in ["STRING", "INT", "FLOAT"]:
        return format_preserving_token(val)
    if method == "RANDOM":
        if data_type == "INT":
            return str(randint(0, 1000000))
        if data_type == "FLOAT":
            return str(random())
        if data_type == "STRING":
            hex_string = hashlib.md5(str(val).encode("UTF-8")).hexdigest()
            return str(UUID(hex=hex_string))
        else:
            hex_string = hashlib.md5(str(val).encode("UTF-8")).hexdigest()
            return str(UUID(hex=hex_string))


def create_uuid_from_list(li: list) -> str:
    """Create a UUID from a list of values."""
    val = " ".join(map(str, li))
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(UUID(hex=hex_string))


def typed_token(token: Token) -> Token:
    """Convert token to correct type."""
    if token.type == "INT":
        token.token = int(token.token)
        token.value = int(token.value)
    elif token.type == "FLOAT":
        token.token = float(token.token)
        token.value = float(token.value)
    return token
    

class TokenDAO:
    """Data access object for tokens."""

    collection_name = "tokens"

    async def find(self, token_find: TokenFind) -> Token:
        identities_ref = db.collection(self.collection_name)
        composite_filter = BaseCompositeFilter(
            operator=StructuredQuery.CompositeFilter.Operator.AND,
            filters=[
                FieldFilter("identifier", "==", token_find.identifier),
                FieldFilter("identity_token", "==", token_find.identity_token),
                FieldFilter("token", "==", token_find.token),
                FieldFilter("field", "==", token_find.field),
            ],
        )
        composite_query = identities_ref.where(filter=composite_filter)
        tokens = [
            typed_token(Token(**doc.to_dict()))
            async for doc in composite_query.stream()
            if doc.to_dict()
        ]
        if len(tokens) > 1:
            raise Exception("More than one token found.")
        if len(tokens) == 0:
            return
        else:
            return tokens[0]

    async def create(self, token_create: TokenCreate) -> Token:
        """Create a token."""
        identity_pk = create_uuid_from_list(
            [token_create.identifier, token_create.identity, token_create.identity]
        )
        identity = await self.get(identity_pk)
        if not identity:
            identity_token = tokenize_value("RANDOM", "STRING", token_create.identity)
            identity_data = Token(
                pk=identity_pk,
                identifier=token_create.identifier,
                identity=token_create.identity,
                identity_token=identity_token,
                type="STRING",
                created_at=token_create.created_at,
                token=identity_token,
                value=token_create.identity,
            ).dict()
            await db.collection(self.collection_name).document(identity_pk).create(
                identity_data
            )
            identity = await self.get(identity_pk)
        if identity.pk == token_create.pk:
            return identity
        token_create.token = tokenize_value(
            token_create.method, token_create.type, token_create.value
        )
        data = token_create.dict()
        data["identity_token"] = identity.identity_token
        await db.collection(self.collection_name).document(token_create.pk).create(data)
        return await self.get(token_create.pk)

    async def get(self, pk: str) -> Token:
        """Get a token."""
        doc_ref = db.collection(self.collection_name).document(pk)
        doc = await doc_ref.get()
        if doc.exists:
            return typed_token(Token(**doc.to_dict()))
        return

    async def get_or_create(self, token_create: TokenCreate) -> Token:
        """Get or create a token if doesn't exists."""
        token = await self.get(token_create.pk)
        if not token:
            token = await self.create(token_create)
        return token

    async def list(self, identifier: str, identity: str) -> List[Token]:
        """List tokens."""
        identities_ref = db.collection(self.collection_name)
        composite_filter = BaseCompositeFilter(
            operator=StructuredQuery.CompositeFilter.Operator.AND,
            filters=[
                FieldFilter("identifier", "==", identifier),
                FieldFilter("identity", "==", identity),
            ],
        )
        composite_query = identities_ref.where(filter=composite_filter)
        return [
            typed_token(Token(**doc.to_dict()))
            async for doc in composite_query.stream()
            if doc.to_dict()
        ]

    async def delete(self, pk: str) -> str:
        """Delete a token."""
        await db.collection(self.collection_name).document(pk).delete()
        return pk

    async def deidentify(
        self, batch: RemoteFunctionTokenRequest
    ) -> RemoteFunctionTokenResponse:
        """Deidentify a batch of tokens."""
        calls = batch.calls
        replies = []
        for call in calls:
            pk = create_uuid_from_list(call)
            token_create = TokenCreate(
                pk=pk,
                identifier=call[0],
                identity=call[1],
                value=call[2],
                field=dict(enumerate(call)).get(3, ""),
                type=batch.userDefinedContext["tokenType"],
            )
            token = await self.get_or_create(token_create)
            replies.append(token.token)
        response = {"replies": replies}
        return RemoteFunctionTokenResponse(**response)

    async def reidentify(
        self, batch: RemoteFunctionTokenRequest
    ) -> RemoteFunctionTokenResponse:
        """Reidentify a batch of tokens."""
        calls = batch.calls
        replies = []
        for call in calls:
            token_find = TokenFind(
                identifier=call[0], identity_token=call[1], token=call[2]
            )
            token = await self.find(token_find)
            if not token:
                replies.append(None)
            else:
                replies.append(token.value)
        response = {"replies": replies}
        return RemoteFunctionTokenResponse(**response)
