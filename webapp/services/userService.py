# from uuid import uuid4
from typing import Iterator

from webapp.models.user import User
from webapp.repositories.userRepository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self, logged_user_email: str) -> Iterator[User]:
        return self._repository.get_all(logged_user_email)

    def get_user_by_id(self, user_id: int, logged_user_email: str) -> User:
        return self._repository.get_by_id(user_id, logged_user_email)

    def create_user(self, email: str, password: str, organization_id: int, logged_user_email: str,
                    user_ip: str) -> User:
        # uid = uuid4()
        # return self._repository.add(email=f"{uid}@email.com", password="pwd")
        return self._repository.add(logged_user_email=logged_user_email, user_ip=user_ip, email=email,
                                    password=password, organization_id=organization_id, )

    def login_user(self, email: str, password: str) -> str:
        return self._repository.login(email=email, password=password)

    def delete_user_by_id(self, user_id: int, logged_user_email: str, user_ip: str) -> None:
        return self._repository.delete_by_id(user_id=user_id, logged_user_email=logged_user_email, user_ip=user_ip)
