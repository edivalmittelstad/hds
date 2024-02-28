from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

DATABASE_URL = getenv('DATABASE_URL')

DATABASE_URL="postgresql+asyncpg://postgres:acessosql@localhost:5432/fastapi"
DATABASE_URL_SYNC="postgresql://postgres:acessosql@localhost:5432/fastapi"

engine      = create_async_engine(DATABASE_URL)
engine_sync = create_engine(DATABASE_URL_SYNC)
# engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
  autocommit=False, 
  class_=AsyncSession, 
  autoflush=True, 
  bind=engine,
  expire_on_commit=False,
)

sync_session =  sessionmaker(
  autocommit=False, 
  autoflush=True, 
  bind=engine_sync,
  expire_on_commit=False,
)

async def teste_db():
  try:
    async with async_session() as session:
      sql = text('select * from usuario')
      res = await session.execute(sql)
      return res
  finally:
    pass

