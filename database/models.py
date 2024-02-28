import enum
import datetime
import uuid
from typing import Optional, List
from sqlalchemy import Integer, DateTime, Uuid, String, Boolean, Enum, ForeignKey, Index
from sqlalchemy import update as update_query
from sqlalchemy.orm import Mapped, deferred, DeclarativeBase, mapped_column, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.future import select
from sqlalchemy import cast, and_, exc

class Base(DeclarativeBase):
  @declared_attr.directive
  def __tablename__(cls) -> str:
    return cls.__name__.lower()
  
  id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
  uuid: Mapped[Uuid]  = mapped_column(Uuid, unique=True, nullable=False, default=uuid.uuid4)
  fullsearch: Mapped[Optional[str]] = mapped_column(String(250), deferred=True, index=True, nullable=True)
  created_at = mapped_column(DateTime, default=datetime.datetime.utcnow, deferred=True, index=True)
  updated_at = mapped_column(DateTime, default=datetime.datetime.utcnow, deferred=True, index=True )
  deleted_at = mapped_column(DateTime, nullable=True, deferred=True, index=True)
  
  Index("idx_created_at_{}".format(__tablename__),created_at.asc())
  Index("idx_updated_at_{}".format(__tablename__),updated_at.asc())
  Index("idx_deleted_at_{}".format(__tablename__),deleted_at.asc())
  Index("idx_fullsearch_{}".format(__tablename__),fullsearch.asc())
  
  async def create(self, async_session, object_input):
    async with async_session() as session:
      try:
          session.add(object_input)
          await session.commit()
      except exc.SQLAlchemyError as exception:
          print("|||" + exception._sql_message() + "|||")
          return {}
      await session.refresh(object_input)
      return object_input
  
  def create_sync(self, sync_session, object_input):
    with sync_session() as session:
      try:
          session.add(object_input)
          session.commit()
      except exc.SQLAlchemyError as exception:
          print("|||" + exception._sql_message() + "|||")
          return {}
      session.refresh(object_input)
      return object_input
          
  async def listar(self, async_session):
    async with async_session() as session:
      result = await session.execute(select(self).where(self.deleted_at is None))
      return result.scalars().all()
  
  async def pegar(self, async_session, _uuid):
    async with async_session() as session:
      objects = await session.execute(select(self).where(and_(cast(self.uuid, String)==_uuid), self.deleted_at is None))
      for object in objects.scalars().all():
        return object
      return {}

  async def delete(self, async_session, _uuid):
    async with async_session() as session:
      objects = await session.execute(select(self)
        .where(and_(cast(self.uuid, String)==_uuid), self.deleted_at is None))
      for object in objects.scalars().all():
        object.deleted_at = datetime.datetime.now()
        await session.commit()
        return True
      return False
    
  async def update(self, async_session, _uuid, object_input):
    async with async_session() as session:
      try:
        query = update_query(self).where(and_(cast(self.uuid, String)==_uuid), self.deleted_at is None).values(**object_input.model_dump())
        res = await session.execute(query)
        await session.commit()
        if res.rowcount:
          return True
        return False
      except exc.SQLAlchemyError as exception:
          print("|||" + exception._sql_message() + "|||")
          return False


class Roles(enum.Enum):
  MASTER = 'MASTER'
  SUPER_ADMIN = 'SUPER_ADMIN'
  ADMIN_BASE = 'ADMIN_BASE'
  USUARIO_BASE = 'USUARIO_BASE'

class Modulo(enum.Enum):
  BASE = 'BASE'
  SITE = 'SITE'
  PORTAL = 'PORTAL'
  CIDADAO = 'CIDADAO'

class Usuario(Base):
  __allow_unmapped__ = True
  __tablename__ = 'usuario'
  nome: Mapped[str] = mapped_column(String(100))
  email: Mapped[str] = mapped_column(String(100))
  senha: Mapped[str] = deferred(mapped_column(String(255)))
  cpf: Mapped[str] = mapped_column(String(15))
  foto: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  status: Mapped[Boolean] = mapped_column(Boolean, default=True)
  roles: List[Roles] = mapped_column(ARRAY(Enum(Roles)),nullable=False,)
  
  Index("ix_usuario_nome", nome.asc())
  Index("ix_usuario_email", email.asc(), unique=True )
  Index("ix_usuario_cpf", cpf.asc() )
  

class HD(Base):
  __allow_unmapped__ = True
  __tablename__ = 'hd'
  nome: Mapped[str] = mapped_column(String(100))
  descricao: Mapped[str] = mapped_column(String(500))
  status: Mapped[Boolean] = mapped_column(Boolean, default=True)
  objetos: Mapped[List["Objeto"]] = relationship("Objeto", back_populates="hd")
  
  Index("ix_hd_nome", nome.asc())
  Index("ix_hd_descricao", descricao.asc())
  
class Objeto(Base):
  __allow_unmapped__ = True
  __tablename__ = 'objeto'
  nome: Mapped[str] = mapped_column(String(255))
  hd_id: Mapped[int] = mapped_column(ForeignKey("hd.id"), nullable=True)
  hd: Mapped["HD"] = relationship("HD", back_populates="objetos" )
  # objeto_id: Mapped[int] = mapped_column(ForeignKey("objeto.id"), nullable=True)
  # objetos: Mapped[List["Objeto"]] = relationship("Objeto", back_populates="objeto")
  # objeto: Mapped["Objeto"] = relationship("Objeto", back_populates="objetos")
  
  Index("ix_objeto_nome", nome.asc())
  
  