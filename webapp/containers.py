"""Containers module."""

from dependency_injector import containers, providers

from .database import Database
from .repositories.organizationRepository import OrganizationRepository
from .repositories.apiaryRepository import ApiaryRepository
from .repositories.hiveRepository import HiveRepository
from .repositories.statisticRepository import StatisticRepository
from .repositories.userRepository import UserRepository
from .services.organizationService import OrganizationService
from .services.apiaryService import ApiaryService
from .services.hiveService import HiveService
from .services.statisticService import StatisticService
from .services.userService import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".endpoints.statusRouter", ".endpoints.organizationRouter", ".endpoints.hiveRouter",
                 ".endpoints.usersRouter", ".endpoints.apiaryRouter", ".endpoints.statisticRouter"])

    config = providers.Configuration(yaml_files=["config.yml"])

    db = providers.Singleton(Database, db_url=config.db.url)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    apiary_repository = providers.Factory(
        ApiaryRepository,
        session_factory=db.provided.session,
    )

    apiary_service = providers.Factory(
        ApiaryService,
        apiary_repository=apiary_repository,
    )

    hive_repository = providers.Factory(
        HiveRepository,
        session_factory=db.provided.session,
    )

    hive_service = providers.Factory(
        HiveService,
        hive_repository=hive_repository,
    )

    statistic_repository = providers.Factory(
        StatisticRepository,
        session_factory=db.provided.session,
    )

    statistic_service = providers.Factory(
        StatisticService,
        statistic_repository=statistic_repository,
    )

    organization_repository = providers.Factory(
        OrganizationRepository,
        session_factory=db.provided.session,
    )

    organization_service = providers.Factory(
        OrganizationService,
        organization_repository=organization_repository,
    )
