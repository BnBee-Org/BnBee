# from uuid import uuid4
from typing import Iterator

from webapp.models.user import User
from webapp.repositories.userRepository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> Iterator[User]:
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._repository.get_by_id(user_id)

    def create_user(self, email: str, password: str, organization_id: int) -> User:
        # uid = uuid4()
        # return self._repository.add(email=f"{uid}@email.com", password="pwd")
        return self._repository.add(email=email, password=password, organization_id=organization_id)

    def login_user(self, email: str, password: str) -> str:
        return self._repository.login(email=email, password=password)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
