from pydoc import describe
from database.connection import sync_session
from sqlalchemy import exc
from database.models import HD
from database.services import BaseService

from src.Hd.schemas import HDCreateInput

class HDImport(BaseService):
  def create_hd(_hd: HDCreateInput):
    data = HD(**_hd.model_dump())
    return super(HDImport).create_sync(HDImport, object_input=data)

HDImport.create_hd(
  HD(
    nome="HD2012-1", 
    descricao="Arquivos de 2012 copia 1", 
    status=True
  )
)

