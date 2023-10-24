from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide
from webapp.auth.auth_bearer import JWTBearer
from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError

from webapp.services.hiveService import HiveService

hive_router = APIRouter()


@hive_router.get("/hives", dependencies=[Depends(JWTBearer())],)
@inject
def get_list(
        hive_service: HiveService = Depends(Provide[Container.hive_service]),
):
    return hive_service.get_hives()


@hive_router.get("/hives/{hive_id}", dependencies=[Depends(JWTBearer())])
@inject
def get_by_id(
        hive_id: int,
        hive_service: HiveService = Depends(Provide[Container.hive_service]),
):
    try:
        return hive_service.get_hive_by_id(hive_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@hive_router.post("/hives", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
@inject
def add(
        hive_name: str,
        is_active: bool,
        apiary_id: int,
        user: str = Depends(JWTBearer()),
        hive_service: HiveService = Depends(Provide[Container.hive_service]),
):
    return hive_service.create_hive(hive_name, is_active, apiary_id, user)


@hive_router.patch("/hives/{hive_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
@inject
def update(
        hive_id: int,
        apiary_id: int,
        bee_count: int | None = None,
        is_active: bool | None = None,
        lid_open: bool | None = None,
        door_open: bool | None = None,
        maintenance: bool | None = None,
        status: bool | None = None,
        hive_name: str | None = None,
        hive_service: HiveService = Depends(Provide[Container.hive_service]),
):
    return hive_service.update_hive(hive_id, hive_name, bee_count, is_active, lid_open, door_open, maintenance,
                                    apiary_id, status)


@hive_router.delete("/hives/{hive_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        hive_id: int,
        hive_service: HiveService = Depends(Provide[Container.hive_service]),
):
    try:
        hive_service.delete_hive_by_id(hive_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
