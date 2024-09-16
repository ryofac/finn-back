from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, registry, sessionmaker

from finn.settings import Settings

table_registry = registry()


class BaseModelMixin:
    id: Mapped[int] = mapped_column(init=False, primary_key=True)


engine = create_async_engine(Settings().database_url, echo=False)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session() as session:
        yield session
