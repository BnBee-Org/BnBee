from contextlib import AbstractContextManager
from datetime import datetime, timedelta
from typing import Callable, Iterator

from pytz import timezone
from sqlalchemy import func
from sqlalchemy.orm import Session

from webapp.models.hive import Hive
from webapp.models.statistics import Statistics
from webapp.models.user import User
from webapp.repositories.notFoundError import NotFoundError

STATISTIC_DAYS_BACK = 10


class StatisticRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self, user_email: str) -> Iterator[Statistics]:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return session.query(Statistics).filter(Statistics.organization_id == user.organization_id).all()

    def get_by_hive_id(self, hive_id: int, user_email: str) -> Statistics:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            stat = session.query(Statistics).filter(Statistics.hive_id == hive_id,
                                                    Statistics.datetime > datetime.today() - timedelta(
                                                        days=STATISTIC_DAYS_BACK),
                                                    Statistics.organization_id == user.organization_id).all()
            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def get_by_date_range(self, hive_id: int, date_from: str, user_email: str) -> Statistics:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            date_split = date_from.split("&")
            start_date = datetime.strptime(date_split[0], '%d-%m-%Y %H:%M:%S')
            end_date = datetime.strptime(date_split[1], '%d-%m-%Y %H:%M:%S')
            stat = session.query(Statistics).filter(Statistics.hive_id == hive_id, Statistics.datetime >= start_date,
                                                    Statistics.datetime < end_date,
                                                    Statistics.organization_id == user.organization_id).all()
            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def get_latest_stat_by_apiary_id(self, apiary_id: int, user_email: str) -> Statistics:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            stat = session.query(Statistics, func.max(Statistics.datetime)) \
                .group_by(Statistics.hive_id) \
                .join(Hive).filter(Statistics.hive_id == Hive.id, Hive.apiary_id == apiary_id,
                                   Statistics.organization_id == user.organization_id).all()

            if not stat:
                raise StatisticsNotFoundError(apiary_id)
            return stat

    def get_latest_stat_by_hive_id(self, hive_id: int, user_email: str) -> Statistics:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            stat = session.query(Statistics, func.max(Statistics.datetime)) \
                .group_by(Statistics.hive_id).filter(Statistics.hive_id == hive_id,
                                                     Statistics.organization_id == user.organization_id).all()

            if not stat:
                raise StatisticsNotFoundError(hive_id)
            return stat

    def add(self, hive_id: int, temperature: float, humidity: float, weight: float, avr_sound: float,
            pressure: float, user_email: str) -> Statistics:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            stat = Statistics(hive_id=hive_id, temperature=temperature, humidity=humidity, weight=weight,
                              avr_sound=avr_sound, pressure=pressure,
                              datetime=datetime.now(tz=timezone('Europe/Kiev')),
                              organization_id=user.organization_id)
            session.add(stat)
            session.commit()
            session.refresh(stat)
            return stat

    def delete_by_id(self, stat_id: int, user_email: str) -> None:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            entity: Statistics = session.query(Statistics).filter(Statistics.id == stat_id,
                                                                  Statistics.organization_id == user.organization_id).first()
            if not entity:
                raise StatisticsNotFoundError(stat_id)
            session.delete(entity)
            session.commit()


class StatisticsNotFoundError(NotFoundError):
    entity_name: str = "Statistic"
