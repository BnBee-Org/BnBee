from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable

from fastapi import HTTPException
from sqlalchemy.orm import Session

from webapp.models.organizations import Organization
from webapp.models.user import User
from webapp.repositories.notFoundError import NotFoundError


class OrganizationRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, name: str, logged_user_email: str) -> Organization:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == logged_user_email).first()
            if not logged_user.is_admin:
                raise HTTPException(status_code=403, detail="You are not admin.")
            organization = Organization(name=name, date_created=datetime.today())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return organization

    def delete_by_id(self, organization_id: int, logged_user_email: str) -> None:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == logged_user_email).first()
            if not logged_user.is_admin:
                raise HTTPException(status_code=403, detail="You are not admin.")
            entity: Organization = session.query(Organization).filter(Organization.id == organization_id).first()
            if not entity:
                raise OrganizationNotFoundError(organization_id)
            session.delete(entity)
            session.commit()


class OrganizationNotFoundError(NotFoundError):
    entity_name: str = "Organization"
