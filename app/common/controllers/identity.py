from typing import Optional, List

from fastapi import APIRouter, Depends, Body, Query
from fastapi_keycloak import HTTPMethod, KeycloakUser
from pydantic import SecretStr
from app.common import get_user, idp

router = APIRouter(prefix="/idp", dependencies=[Depends(get_user())])  # Protect all the paths with user authentication

#################################
# IDP Admin Router
#################################


@router.post("/proxy", tags=["admin-cli"])
def proxy_admin_request(relative_path: str, method: HTTPMethod, additional_headers: dict = Body(None),
                        payload: dict = Body(None)):
    return idp.proxy(
        additional_headers=additional_headers,
        relative_path=relative_path,
        method=method,
        payload=payload
    )


@router.get("/identity-providers", tags=["admin-cli"])
def get_identity_providers():
    return idp.get_identity_providers()


@router.get("/idp-configuration", tags=["admin-cli"])
def get_idp_config():
    return idp.open_id_configuration


# User Management

@router.get("/users", tags=["user-management"])
def get_users():
    return idp.get_all_users()


@router.get("/user", tags=["user-management"])
def get_user_by_query(query: str = None):
    return idp.get_user(query=query)


@router.post("/users", tags=["user-management"])
def create_user(first_name: str, last_name: str, email: str, password: SecretStr, id: str = None):
    return idp.create_user(first_name=first_name, last_name=last_name, username=email, email=email,
                           password=password.get_secret_value(), id=id)


@router.get("/user/{user_id}", tags=["user-management"])
def get_user(user_id: str = None):
    return idp.get_user(user_id=user_id)


@router.put("/user", tags=["user-management"])
def update_user(user: KeycloakUser):
    return idp.update_user(user=user)


@router.delete("/user/{user_id}", tags=["user-management"])
def delete_user(user_id: str):
    return idp.delete_user(user_id=user_id)


@router.put("/user/{user_id}/change-password", tags=["user-management"])
def change_password(user_id: str, new_password: SecretStr):
    return idp.change_password(user_id=user_id, new_password=new_password)


@router.put("/user/{user_id}/send-email-verification", tags=["user-management"])
def send_email_verification(user_id: str):
    return idp.send_email_verification(user_id=user_id)


# Role Management

@router.get("/roles", tags=["role-management"])
def get_all_roles():
    return idp.get_all_roles()


@router.get("/role/{role_name}", tags=["role-management"])
def get_role(role_name: str):
    return idp.get_roles([role_name])


@router.post("/roles", tags=["role-management"])
def add_role(role_name: str):
    return idp.create_role(role_name=role_name)


@router.delete("/roles", tags=["role-management"])
def delete_roles(role_name: str):
    return idp.delete_role(role_name=role_name)


# Group Management

@router.get("/groups", tags=["group-management"])
def get_all_groups():
    return idp.get_all_groups()


@router.get("/group/{group_name}", tags=["group-management"])
def get_group(group_name: str):
    return idp.get_groups([group_name])


@router.get("/group-by-path/{path: path}", tags=["group-management"])
def get_group_by_path(path: str):
    return idp.get_group_by_path(path)


@router.post("/groups", tags=["group-management"])
def add_group(group_name: str, parent_id: Optional[str] = None):
    return idp.create_group(group_name=group_name, parent=parent_id)


@router.delete("/groups", tags=["group-management"])
def delete_groups(group_id: str):
    return idp.delete_group(group_id=group_id)


# User Roles

@router.post("/users/{user_id}/roles", tags=["user-roles"])
def add_roles_to_user(user_id: str, roles: Optional[List[str]] = Query(None)):
    return idp.add_user_roles(user_id=user_id, roles=roles)


@router.get("/users/{user_id}/roles", tags=["user-roles"])
def get_user_roles(user_id: str):
    return idp.get_user_roles(user_id=user_id)


@router.delete("/users/{user_id}/roles", tags=["user-roles"])
def delete_roles_from_user(user_id: str, roles: Optional[List[str]] = Query(None)):
    return idp.remove_user_roles(user_id=user_id, roles=roles)


# User Groups

@router.post("/users/{user_id}/groups", tags=["user-groups"])
def add_group_to_user(user_id: str, group_id: str):
    return idp.add_user_group(user_id=user_id, group_id=group_id)


@router.get("/users/{user_id}/groups", tags=["user-groups"])
def get_user_groups(user_id: str):
    return idp.get_user_groups(user_id=user_id)


@router.delete("/users/{user_id}/groups", tags=["user-groups"])
def delete_groups_from_user(user_id: str, group_id: str):
    return idp.remove_user_group(user_id=user_id, group_id=group_id)
