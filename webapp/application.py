"""Application module."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .containers import Container
from .endpoints.apiaryRouter import apiary_router
from .endpoints.hiveRouter import hive_router
from .endpoints.statisticRouter import statistic_router
from .endpoints.statusRouter import router
from .endpoints.usersRouter import user_router
from .endpoints.organizationRouter import organization_router


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_credentials=False,
                       allow_methods=["*"],
                       allow_headers=["*"], )
    app.container = container
    app.include_router(organization_router, tags=["organizations"])
    app.include_router(user_router, tags=["users"])
    app.include_router(apiary_router, tags=["apiaries"])
    app.include_router(hive_router, tags=["hives"])
    app.include_router(statistic_router, tags=["statistic"])
    app.include_router(router, tags=["default"])

    return app


app = create_app()
