from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel import SQLModel, create_engine

engine = AsyncEngine(
    create_engine(
        url=Config.database_uri,
        echo=True,
    )
)


async def init_db():
    async with engine.begin() as conn:
        # statement = text("SELECT 'Hello';")
        # result = await conn.execute(statement)
        # print(result.all())

        # explicitly it need to import where SQL MODEL
        from src.db.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db_session() -> AsyncSession:  # linter fault
    Session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
