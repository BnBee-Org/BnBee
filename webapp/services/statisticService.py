from typing import Iterator

from webapp.models.statistics import Statistics
from webapp.repositories.statisticRepository import StatisticRepository


class StatisticService:

    def __init__(self, statistic_repository: StatisticRepository) -> None:
        self._repository: StatisticRepository = statistic_repository

    def get_statistic(self, user_email: str) -> Iterator[Statistics]:
        return self._repository.get_all(user_email)

    def get_statistic_by_hive_id(self, hive_id: int, user_email: str) -> Statistics:
        return self._repository.get_by_hive_id(hive_id, user_email)

    def get_statistic_by_date_range(self, hive_id: int, date_range: str, user_email: str) -> Statistics:
        return self._repository.get_by_date_range(hive_id, date_range, user_email)

    def get_latest_stat_by_apiary_id(self, apiary_id: int, user_email: str) -> Statistics:
        return self._repository.get_latest_stat_by_apiary_id(apiary_id, user_email)

    def get_latest_stat_by_hive_id(self, hive_id: int, user_email: str) -> Statistics:
        return self._repository.get_latest_stat_by_hive_id(hive_id, user_email)

    def create_statistic(self, hive_id: int, temperature: float, humidity: float, weight: float, avr_sound: float,
                         pressure: float, user_email: str) -> Statistics:
        return self._repository.add(hive_id=hive_id, temperature=temperature, humidity=humidity, weight=weight,
                                    avr_sound=avr_sound, pressure=pressure, user_email=user_email)

    def delete_statistic_by_id(self, stat_id: int, user_email: str) -> None:
        return self._repository.delete_by_id(stat_id, user_email)
