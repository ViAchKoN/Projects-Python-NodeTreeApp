from typing import Generator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.settings import settings

from app.db import models

engine = create_async_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception as err:
        print(err)
    finally:
        await db.close()
