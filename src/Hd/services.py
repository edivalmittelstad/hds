from sqlalchemy import Uuid

from database.models import HD
from database.connection import async_session
from database.services import BaseService
from .schemas import HDCreateInput, HDUpdateInput

class HDService(BaseService):
  async def create_hd(_hd: HDCreateInput):
    data = HD(**_hd.model_dump())
    return await super(HDService).create(HDService, object_input=data)

  async def update(_uuid: Uuid, _hd: HDUpdateInput):
    return await HD.update(HD, async_session, _uuid, _hd)

  async def listar():
    return await HD.listar(HD, async_session)

  async def pegar(_uuid: Uuid):
    return await HD.pegar(HD, async_session, _uuid)

  async def excluir(_uuid: Uuid):
    return await HD.delete(HD, async_session, _uuid)

 