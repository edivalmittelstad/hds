from asyncio import run
from database.init_db import create_database

async def createDB():
    await create_database()
    
run(createDB())
