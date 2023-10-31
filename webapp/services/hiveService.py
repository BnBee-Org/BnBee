from typing import Iterator

from webapp.models.hive import Hive
from webapp.repositories.hiveRepository import HiveRepository


class HiveService:

    def __init__(self, hive_repository: HiveRepository) -> None:
        self._repository: HiveRepository = hive_repository

    def get_hives(self, user_email: str) -> Iterator[Hive]:
        return self._repository.get_all(user_email=user_email)

    def get_hive_by_id(self, hive_id: int, user_email: str) -> Hive:
        return self._repository.get_by_id(hive_id, user_email=user_email)

    def create_hive(self, hive_name: str, is_active: bool, apiary_id: int, user_email: str) -> Hive:
        return self._repository.add(name=hive_name, is_active=is_active, apiary_id=apiary_id, user_email=user_email)

    def update_hive(self, hive_id: int, hive_name: str, bee_count: int, is_active: bool, lid_open: bool,
                    door_open: bool,
                    maintenance: bool, apiary_id: int, status: bool, user_email: str) -> Hive:
        return self._repository.update(hive_id=hive_id, name=hive_name, bee_count=bee_count, is_active=is_active,
                                       lid_open=lid_open, door_open=door_open, maintenance=maintenance,
                                       apiary_id=apiary_id, status=status, user_email=user_email)

    def delete_hive_by_id(self, hive_id: int, user_email: str) -> None:
        return self._repository.delete_by_id(hive_id, user_email)
