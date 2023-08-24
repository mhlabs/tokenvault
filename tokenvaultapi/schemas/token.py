"""Token schemas."""
from datetime import datetime
from typing import Any, Union

from pydantic import BaseModel, Field, StrictFloat, StrictInt


class TokenBase(BaseModel):
    """Base token."""

    identity: str
    identifier: str
    value: str
    type: str = "STRING"
    field: str = ""


class TokenCreate(TokenBase):
    """Create a token."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    pk: Union[str, None]
    token: Union[str, None] = None
    method: str = "FORMAT_PRESERVING"

    class Config:
        """Config for token create."""

        schema_extra = {
            "example": {
                "identifier": "CUSTOMER_ID",
                "identity": "12345",
                "type": "STRING",
                "field": "email",
                "value": "john.doe@example.com",
                "method": "FORMAT_PRESERVING",
            }
        }


class TokenFind(BaseModel):
    """Find a token."""

    identity_token: str
    identifier: str
    field: str = ""
    token: str

    class Config:
        """Config for token find."""

        schema_extra = {
            "example": {
                "identifier": "CUSTOMER_ID",
                "identity_token": "437389b6-3ca3-07f2-500b-8b031957a824",
                "field": "email",
                "token": "8eb1b522-f60d-11fa-897d-e1dc6351b7e8",
            }
        }


class TokenResponse(TokenBase):
    """Token response."""

    token: Any

    class Config:
        """Config for token response."""

        schema_extra = {
            "example": {
                "identifier": "CUSTOMER_ID",
                "identity": "12345",
                "token": "8eb1b522-f60d-11fa-897d-e1dc6351b7e8",
            }
        }


class Token(TokenBase):
    """Token."""

    created_at: datetime
    token: Any
    identity_token: str
    pk: str

    class Config:
        """Config for token."""

        orm_mode = True


class RemoteFunctionTokenRequest(BaseModel):
    """Remote function token request."""

    requestId: str
    caller: str
    sessionUser: str
    userDefinedContext: dict[str, str] = None
    calls: list[list[Union[None, StrictInt, StrictFloat, str]]]

    class Config:
        """Config for remote function token request."""

        schema_extra = {
            "example": {
                "requestId": "124ab1c",
                "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.\
                bquxjob_5b4c112c_17961fafeaf",
                "sessionUser": "test-user@test-company.com",
                "userDefinedContext": {
                    "action": "DEIDENTIFY",
                    "tokenType": "STRING",
                },
                "calls": [
                    ["CUSTOMER_ID", "12345", "john.doe@example.com"],
                    ["CUSTOMER_ID", "12345", "+46(0)701020304"],
                ],
            }
        }


class RemoteFunctionTokenResponse(BaseModel):
    """Remote function token response."""

    replies: list[Any]

    class Config:
        """Config for remote function token response."""

        schema_extra = {"example": {"replies": [1, 0]}}
