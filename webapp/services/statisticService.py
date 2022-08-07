from typing import Iterator

from webapp.models.statistics import Statistics
from webapp.repositories.statisticRepository import StatisticRepository


class StatisticService:

    def __init__(self, statistic_repository: StatisticRepository) -> None:
        self._repository: StatisticRepository = statistic_repository

    def get_statistic(self) -> Iterator[Statistics]:
        return self._repository.get_all()

    def get_statistic_by_hive_id(self, hive_id: int) -> Statistics:
        return self._repository.get_by_hive_id(hive_id)

    def get_statistic_by_date_range(self, hive_id: int, date_range: str) -> Statistics:
        return self._repository.get_by_date_range(hive_id, date_range)

    def get_latest_stat_by_apiary_id(self, apiary_id: int) -> Statistics:
        return self._repository.get_latest_stat_by_apiary_id(apiary_id)

    def get_latest_stat_by_hive_id(self, hive_id: int) -> Statistics:
        return self._repository.get_latest_stat_by_hive_id(hive_id)

    def create_statistic(self, hive_id: int, temperature: float, humidity: float, weight: float, avr_sound: float,
                         pressure: float) -> Statistics:
        return self._repository.add(hive_id=hive_id, temperature=temperature, humidity=humidity, weight=weight,
                                    avr_sound=avr_sound, pressure=pressure)

    def delete_statistic_by_id(self, stat_id: int) -> None:
        return self._repository.delete_by_id(stat_id)
