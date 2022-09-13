import logging

from fastapi import APIRouter, Depends
from fastapi_keycloak import OIDCUser, UsernamePassword, FastAPIKeycloak
from starlette.responses import RedirectResponse

from app.common import get_user, idp as _idp

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

idp: FastAPIKeycloak = _idp.client

#################################
# Basic Authentication Router
#################################


@router.get("/")  # Unprotected
def root():
    return 'Hello World'


@router.get("/user")  # Requires logged in
def current_users(user: OIDCUser = Depends(get_user())):
    return user


@router.get("/current_user/roles")
def get_current_users_roles(user: OIDCUser = Depends(get_user())):
    return user.roles


@router.get("/admin")  # Requires the admin role
def company_admin(user: OIDCUser = Depends(get_user(required_roles=["admin"]))):
    return f'Hi admin {user}'


@router.get("/login")
def login_redirect():
    return RedirectResponse(idp.login_uri)


@router.get("/login-oauth")
def login(user: UsernamePassword = Depends()):
    return idp.user_login(username=user.username, password=user.password.get_secret_value())


@router.get("/callback")
def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


@router.get("/logout")
def logout():
    return idp.logout_uri
