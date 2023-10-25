from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from webapp.auth.auth_bearer import JWTBearer
from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError
from webapp.services.organizationService import OrganizationService

organization_router = APIRouter()


@organization_router.post("/organizations", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
@inject
def add(
        organization_name: str,
        organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
):
    return organization_service.create_organization(organization_name)


@organization_router.delete("/organizations/{organization_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        organization_id: int,
        organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
):
    try:
        organization_service.delete_organization_by_id(organization_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
