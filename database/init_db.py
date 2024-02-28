from asyncio import run
# from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine

from database.models import Base

engine = create_async_engine('postgresql+asyncpg://postgres:acessosql@localhost:5432/fastapi', echo=True,)

async def create_database():
    async with engine.begin() as connection:
        print('Creating Database')
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        print('Database created successfully')

if __name__ == '__main__':
    run(create_database())
