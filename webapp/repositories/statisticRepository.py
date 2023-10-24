from contextlib import AbstractContextManager
from datetime import datetime, timedelta
from pytz import timezone
from typing import Callable, Iterator

from sqlalchemy import func
from sqlalchemy.orm import Session

from webapp.models.hive import Hive
from webapp.models.statistics import Statistics
from webapp.repositories.notFoundError import NotFoundError

STATISTIC_DAYS_BACK = 10


class StatisticRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Statistics]:
        with self.session_factory() as session:
            return session.query(Statistics).all()

    def get_by_hive_id(self, hive_id: int) -> Statistics:
        with self.session_factory() as session:
            stat = session.query(Statistics).filter(Statistics.hive_id == hive_id,
                                                    Statistics.datetime > datetime.today() - timedelta(
                                                        days=STATISTIC_DAYS_BACK)).all()
            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def get_by_date_range(self, hive_id: int, date_from: str) -> Statistics:
        with self.session_factory() as session:
            date_split = date_from.split("&")
            start_date = datetime.strptime(date_split[0], '%d-%m-%Y %H:%M:%S')
            end_date = datetime.strptime(date_split[1], '%d-%m-%Y %H:%M:%S')
            stat = session.query(Statistics).filter(Statistics.hive_id == hive_id, Statistics.datetime >= start_date,
                                                    Statistics.datetime < end_date).all()
            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def get_latest_stat_by_apiary_id(self, apiary_id: int) -> Statistics:
        with self.session_factory() as session:
            stat = session.query(Statistics, func.max(Statistics.datetime)) \
                .group_by(Statistics.hive_id) \
                .join(Hive).filter(Statistics.hive_id == Hive.id, Hive.apiary_id == apiary_id).all()

            if not stat:
                raise StatisticsNotFoundError(apiary_id)
            return stat

    def get_latest_stat_by_hive_id(self, hive_id: int) -> Statistics:
        with self.session_factory() as session:
            stat = session.query(Statistics, func.max(Statistics.datetime)) \
                .group_by(Statistics.hive_id).filter(Statistics.hive_id == hive_id).all()

            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def add(self, hive_id: int, temperature: float, humidity: float, weight: float, avr_sound: float,
            pressure: float) -> Statistics:
        with self.session_factory() as session:
            stat = Statistics(hive_id=hive_id, temperature=temperature, humidity=humidity, weight=weight,
                              avr_sound=avr_sound, pressure=pressure,
                              datetime=datetime.now(tz=timezone('Europe/Kiev')))
            session.add(stat)
            session.commit()
            session.refresh(stat)
            return stat

    def delete_by_id(self, stat_id: int) -> None:
        with self.session_factory() as session:
            entity: Statistics = session.query(Statistics).filter(Statistics.id == stat_id).first()
            if not entity:
                raise StatisticsNotFoundError(stat_id)
            session.delete(entity)
            session.commit()


class StatisticsNotFoundError(NotFoundError):
    entity_name: str = "Statistic"
