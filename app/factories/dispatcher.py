from __future__ import annotations

from typing import TYPE_CHECKING

from app.factories.services import create_services

if TYPE_CHECKING:
    from app.core.config import AppConfig

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from app.bot.filters import IsPrivate
from app.bot.models import AppContainer
from app.bot.routers import routers
from app.core import mjson

from .middlewares import create_middlewares
from .redis import create_redis
from .remnawave import create_remnawave
from .session_pool import create_session_pool


def create_dispatcher(bot: Bot, config: AppConfig) -> Dispatcher:
    key_builder = DefaultKeyBuilder(with_destiny=True)
    redis: Redis = create_redis(url=config.redis.dsn())

    middlewares = create_middlewares(config)
    i18n_middleware = middlewares.inner[0]  # I18nMiddleware is the first in inner middlewares

    session_pool = create_session_pool(config)
    remnawave = create_remnawave(config)
    services = create_services(
        bot=bot,
        config=config,
        session_pool=session_pool,
        redis=redis,
        i18n=i18n_middleware,
    )

    container = AppContainer(
        config=config,
        i18n=i18n_middleware,
        session_pool=session_pool,
        redis=redis,
        remnawave=remnawave,
        services=services,
    )

    dispatcher = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            key_builder=key_builder,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        container=container,
    )

    # request -> outer -> filter -> inner -> handler #
    setup_dialogs(router=dispatcher)

    for mw in middlewares.outer:
        mw.setup_outer(router=dispatcher)

    for mw in middlewares.inner:
        mw.setup_inner(router=dispatcher)

    dispatcher.message.filter(IsPrivate())
    dispatcher.include_routers(*routers)
    return dispatcher
