from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from webapp.models.apiary import Apiary
from webapp.models.user import User
from webapp.repositories.notFoundError import NotFoundError


class ApiaryRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self, email: str) -> Iterator[Apiary]:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            return session.query(Apiary).filter(Apiary.id == user.organization_id).all()

    def get_by_id(self, apiary_id: int, email: str) -> Apiary:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            apiary = session.query(Apiary).filter(
                Apiary.id == apiary_id and Apiary.organization_id == user.organization_id).first()
            if not apiary:
                raise ApiaryNotFoundError(apiary_id)
            return apiary

    def add(self, name: str, email: str) -> Apiary:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            apiary = Apiary(name=name, organization_id=user.organization_id)
            session.add(apiary)
            session.commit()
            session.refresh(apiary)
            return apiary

    def update(self, apiary_id: int, name: str, email: str) -> Apiary:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            apiary = session.get(Apiary, apiary_id)
            if not apiary or apiary.organization_id != user.organization_id:
                raise ApiaryNotFoundError(apiary_id)
            apiary.name = name
            session.add(apiary)
            session.commit()
            session.refresh(apiary)
            return apiary

    def delete_by_id(self, apiary_id: int, email: str) -> None:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            entity: Apiary = session.query(Apiary).filter(Apiary.id == apiary_id,
                                                          Apiary.organization_id == user.organization_id).first()
            if not entity:
                raise ApiaryNotFoundError(apiary_id)
            session.delete(entity)
            session.commit()


class ApiaryNotFoundError(NotFoundError):
    entity_name: str = "Apiary"
