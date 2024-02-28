import datetime
from sqlalchemy import cast, and_, exc
from sqlalchemy import String
from sqlalchemy.future import select
from sqlalchemy import update as update_query

from database.connection import async_session
from database.connection import sync_session

class BaseService:
  async def create(self, object_input):
    async with async_session() as session:
      try:
        session.add(object_input)
        await session.commit()
      except exc.SQLAlchemyError as exception:
        print("|||" + exception._sql_message() + "|||")
        return {}
      await session.refresh(object_input)
      return object_input
    
  def create_sync(self, object_input):
    with sync_session() as session:
      try:
        session.add(object_input)
        session.commit()
      except exc.SQLAlchemyError as exception:
        print("|||" + exception._sql_message() + "|||")
        return {}
      session.refresh(object_input)
      return object_input

  async def list(self, async_session):
    async with async_session() as session:
      result = await session.execute(select(self).where(self.deleted_at == None))
      return result.scalars().all()
  
  async def get(self, async_session, _uuid):
    async with async_session() as session:
      objects = await session.execute(select(self).where(and_(cast(self.uuid, String)==_uuid), self.deleted_at == None))
      for object in objects.scalars().all():
        return object
      return {}

  async def delete(self, async_session, _uuid):
    async with async_session() as session:
      objects = await session.execute(select(self)
        .where(and_(cast(self.uuid, String)==_uuid), self.deleted_at == None))
      for object in objects.scalars().all():
        object.deleted_at = datetime.datetime.now()
        await session.commit()
        return True
      return False
    
  async def update(self, async_session, _uuid, object_input):
    async with async_session() as session:
      try:
        query = update_query(self).where(and_(cast(self.uuid, String)==_uuid), self.deleted_at == None).values(**object_input.model_dump())
        res = await session.execute(query)
        await session.commit()
        if res.rowcount:
          return True
        return False
      except exc.SQLAlchemyError as exception:
          print("|||" + exception._sql_message() + "|||")
          return False
