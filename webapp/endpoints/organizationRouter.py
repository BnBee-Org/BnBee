from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Request

from webapp.auth.auth_bearer import JWTBearer
from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError
from webapp.services.organizationService import OrganizationService

organization_router = APIRouter()


@organization_router.post("/organizations", status_code=status.HTTP_201_CREATED, tags=['admin'])
@inject
def add(
        request: Request,
        organization_name: str,
        organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
        logged_user_email: str = Depends(JWTBearer()),
):
    return organization_service.create_organization(organization_name=organization_name,
                                                    logged_user_email=logged_user_email, user_ip=request.client.host)


@organization_router.delete("/organizations/{organization_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['admin'])
@inject
def remove(
        request: Request,
        organization_id: int,
        organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
        logged_user_email: str = Depends(JWTBearer()),
):
    try:
        organization_service.delete_organization_by_id(organization_id=organization_id,
                                                       logged_user_email=logged_user_email, user_ip=request.client.host)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
