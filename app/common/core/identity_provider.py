import abc
from typing import Protocol, Optional, List, Callable, Any, T

from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    uid: str
    email: Optional[str]
    roles: List[str]


class IdentityProvider(Protocol):
    def get_current_user(self, required_roles: list[str] | None = None) -> Callable[[Any], User]:
        """Function that checks the current user based on an access token in the HTTP-header. Optionally verifies
        roles are possessed by the user

        Args:
            required_roles List[str]: List of role names required for this endpoint

        Returns:
            OIDCUser: Decoded JWT content

        Raises:
            ExpiredSignatureError: If the token is expired (exp > datetime.now())
            JWTError: If decoding fails or the signature is invalid
            JWTClaimsError: If any claim is invalid
            HTTPException: If any role required is not contained within the roles of the users
        """
        ...

    @property
    def client(self) -> T:
        raise Exception

    def configure_api(self, api: FastAPI):
        """Function that configures the API adding extra controllers or features specifics for this IDP
        """
        ...
