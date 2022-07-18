import abc
from enum import Enum
from fastapi_keycloak import FastAPIKeycloak
from app.common.infra.firebase import FirebaseSettings, get_firebase_settings, FirebaseService
from app.common.infra.keycloak import KeycloakSettings, get_keycloak_settings, KeycloakService


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


class IDPType(Enum):
    KEYCLOAK = 0
    FIREBASE = 1


def __get_idp(keycloak_settings: KeycloakSettings | None, firebase_settings: FirebaseSettings | None) -> \
        (IdentityProvider, IDPType):
    """Factory that creates the instance of the Identity Provider given the app configuration"""
    print("Loading IDP Configuration")
    # Check if configuration is defined to use Keycloak IDP
    if keycloak_settings is not None and keycloak_settings.auth_server is not None \
            and keycloak_settings.realm is not None:
        try:
            # Configure Keycloak Authentication
            idp_local = KeycloakService(keycloak_settings)
            print("Using Keycloak as IDP")
            return idp_local, IDPType.KEYCLOAK
        except Exception:
            print("Error configuring Keycloak")
            pass
    # Check if configuration is defined to use Firebase IDP
    if firebase_settings is not None and firebase_settings.credentials_file is not None:
        try:
            # Configure Firebase Service
            idp_local = FirebaseService(settings=firebase_settings)
            print("Using Firebase as IDP")
            return idp_local, IDPType.FIREBASE
        except Exception:
            print("Error configuring Firebase")
            pass
    return None, None


idp_configuration = __get_idp(
    keycloak_settings=get_keycloak_settings(),
    firebase_settings=get_firebase_settings()
)

idp: IdentityProvider | FastAPIKeycloak | FirebaseService = idp_configuration[0]
idp_type: IDPType = idp_configuration[1]
