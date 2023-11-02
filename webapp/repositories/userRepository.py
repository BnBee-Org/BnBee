from contextlib import AbstractContextManager
from typing import Callable, Iterator

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from webapp.models.organizations import Organization
from webapp.models.user import User


class UserRepository:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self, user_email) -> Iterator[User]:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return session.query(User).filter(User.organization_id == user.organization_id).all()

    def get_by_id(self, user_id: int, user_email: str) -> User:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == user_email).first()
            user = session.query(User).filter(User.organization_id == logged_user.organization_id,
                                              User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found.")
            return user

    def add(self, email: str, password: str, organization_id: int,
            is_active: bool = True) -> User:
        with self.session_factory() as session:
            organization = session.query(Organization).filter(Organization.id == organization_id).first()
            if not organization:
                raise HTTPException(status_code=404, detail="Organization not found.")
            user = User(email=email, hashed_password=self.get_password_hash(password), organization_id=organization_id,
                        is_active=is_active)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def login(self, email: str, password: str) -> str:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            elif self.verify_password(password, user.hashed_password):
                return email
            else:
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

    def delete_by_id(self, user_id: int, user_email) -> None:
        with self.session_factory() as session:
            logged_user = session.query(User).filter(User.email == user_email).first()
            entity: User = session.query(User).filter(
                User.id == user_id, User.organization_id == logged_user.organization_id).first()
            if not entity:
                raise HTTPException(status_code=404, detail="User not found.")
            session.delete(entity)
            session.commit()

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
