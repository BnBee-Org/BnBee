from fastapi import APIRouter, Depends, Response, status, Query
from dependency_injector.wiring import inject, Provide

from webapp.auth.auth_bearer import JWTBearer
from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError
from webapp.services.statisticService import StatisticService

statistic_router = APIRouter()


@statistic_router.get("/statistic", dependencies=[Depends(JWTBearer())])
@inject
def get_list(
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    return statistic_service.get_statistic()


@statistic_router.get("/statistic/{hive_id}", dependencies=[Depends(JWTBearer())])
@inject
def get_by_id(
        hive_id: int,
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    try:
        return statistic_service.get_statistic_by_hive_id(hive_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@statistic_router.get("/statistic/latest/{apiary_id}", dependencies=[Depends(JWTBearer())])
@inject
def get_by_id(
        apiary_id: int,
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    try:
        return statistic_service.get_latest_stat_by_apiary(apiary_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@statistic_router.get("/statistic/{hive_id}/{date_range}", dependencies=[Depends(JWTBearer())])
@inject
def get_by_date_range(
        hive_id: int,
        date_range: str,
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    try:
        return statistic_service.get_statistic_by_date_range(hive_id, date_range)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@statistic_router.post("/statistic", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
@inject
def add(
        hive_id: int,
        temperature: float,
        humidity: float,
        weight: float,
        avr_sound: float,
        pressure: float,
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    return statistic_service.create_statistic(hive_id, temperature, humidity, weight,
                                              avr_sound, pressure)


@statistic_router.delete("/statistic/{statistic_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        stat_id: int,
        statistic_service: StatisticService = Depends(Provide[Container.statistic_service]),
):
    try:
        statistic_service.delete_statistic_by_id(stat_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
