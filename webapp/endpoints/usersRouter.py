from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from webapp.auth.auth_bearer import JWTBearer
from webapp.auth.auth_handler import sign_jwt
from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError
from webapp.services.userService import UserService

user_router = APIRouter()


@user_router.get("/users", dependencies=[Depends(JWTBearer())])
@inject
def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_users()


@user_router.get("/users/{user_id}", dependencies=[Depends(JWTBearer())])
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@user_router.post("/users", status_code=status.HTTP_201_CREATED)
@inject
def add(
        email: str,
        password: str,
        organization_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user(email, password, organization_id)


@user_router.post("/users/login", status_code=status.HTTP_200_OK)
@inject
def login(
        email: str,
        password: str,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return sign_jwt(user_service.login_user(email, password))


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
@inject
def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
