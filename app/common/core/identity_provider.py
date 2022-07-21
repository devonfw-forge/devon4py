import abc


class IdentityProvider(abc.ABC):
    @abc.abstractmethod
    def get_current_user(self, required_roles: list[str] | None = None):
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
        raise NotImplementedError
