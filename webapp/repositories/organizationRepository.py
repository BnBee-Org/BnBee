import ipaddress
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable

from fastapi import HTTPException
from sqlalchemy.orm import Session

from webapp.models.organizations import Organization
from webapp.models.user import User
from webapp.models.whitelist import Whitelist
from webapp.repositories.notFoundError import NotFoundError


class OrganizationRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def tuple_to_string(self, address):
        result = ', '.join(map(str, address))
        result = result.replace('(', '').replace(')', '')
        return result

    def check_user_ip(self, user_ip: str, logged_user_id: int) -> bool:
        with self.session_factory() as session:
            ip_whitelist = session.query(Whitelist.ip_range).filter(Whitelist.user_id == logged_user_id).all()
            for ip in ip_whitelist:
                ip = self.tuple_to_string(ip)
                if '/' in ip:
                    try:
                        ip = ipaddress.ip_address(user_ip)
                        network = ipaddress.ip_network(ip, strict=False)
                        if ip in network:
                            return True
                    except ValueError:
                        raise HTTPException(status_code=403, detail="Invalid IP address.")
                elif user_ip == ip:
                    return True
            return False

    def add(self, name: str, logged_user_email: str, user_ip) -> Organization:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == logged_user_email).first()
            if not logged_user.is_admin:
                raise HTTPException(status_code=403, detail="You are not admin.")
            if self.check_user_ip(user_ip=user_ip, logged_user_id=logged_user.id) == False:
                raise HTTPException(status_code=403, detail="Invalid IP address.")
            organization = Organization(name=name, date_created=datetime.today())
            session.add(organization)
            session.commit()
            session.refresh(organization)
            return organization

    def delete_by_id(self, organization_id: int, logged_user_email: str, user_ip: str) -> None:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == logged_user_email).first()
            if not logged_user.is_admin:
                raise HTTPException(status_code=403, detail="You are not admin.")
            if self.check_user_ip(user_ip=user_ip, logged_user_id=logged_user.id) == False:
                raise HTTPException(status_code=403, detail="Invalid IP address.")
            entity: Organization = session.query(Organization).filter(Organization.id == organization_id).first()
            if not entity:
                raise OrganizationNotFoundError(organization_id)
            session.delete(entity)
            session.commit()


class OrganizationNotFoundError(NotFoundError):
    entity_name: str = "Organization"
