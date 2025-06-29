from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.bot.services import BaseService
from app.core.config import AppConfig


class CrudService(BaseService):
    session_pool: async_sessionmaker[AsyncSession]
    config: AppConfig
    # TODO: Implement caching of database data using Redis

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        config: AppConfig,
    ) -> None:
        super().__init__()
        self.session_pool = session_pool
        self.config = config
