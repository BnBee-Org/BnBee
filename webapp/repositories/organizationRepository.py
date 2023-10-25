from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable

from sqlalchemy.orm import Session

from webapp.models.organizations import Organization
from webapp.repositories.notFoundError import NotFoundError


class OrganizationRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, name: str) -> Organization:
        with self.session_factory() as session:
            organization = Organization(name=name, date_created=datetime.today())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return organization

    def delete_by_id(self, organization_id: int) -> None:
        with self.session_factory() as session:
            entity: Organization = session.query(Organization).filter(Organization.id == organization_id).first()
            if not entity:
                raise OrganizationNotFoundError(organization_id)
            session.delete(entity)
            session.commit()


class OrganizationNotFoundError(NotFoundError):
    entity_name: str = "Organization"
