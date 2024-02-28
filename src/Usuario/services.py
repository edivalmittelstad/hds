from passlib.context import CryptContext

from database.models import Usuario
from sqlalchemy import String, Uuid, cast, and_
from sqlalchemy.future import select
from sqlalchemy.orm import load_only

from database.connection import async_session
from .schemas import UsuarioCreateInput, UsuarioUpdateInput

crypt_context   = CryptContext(schemes=['sha256_crypt'])

class UsuarioService:
    async def create_usuario(_usuario: UsuarioCreateInput):
        data = Usuario(**_usuario.model_dump())
        data.senha = crypt_context.hash(_usuario.senha)
        return await Usuario.create(Usuario, async_session, data)
    
    async def update_usuario(_uuid: Uuid,_usuario: UsuarioUpdateInput):
        async with async_session() as session:
            usuarios = await session.execute(select(Usuario)
                .where(and_(cast(Usuario.uuid, String)==_uuid), Usuario.deleted_at is None))
            for usuario in usuarios.scalars().all():
                usuario.nome = _usuario.nome if _usuario.nome is not None else usuario.nome 
                usuario.email = _usuario.email if _usuario.email is not None else usuario.email 
                usuario.foto = _usuario.foto if _usuario.foto is not None else usuario.foto 
                usuario.status = _usuario.status if _usuario.status is not None else usuario.status 
                if _usuario.senha is not None:
                    usuario.senha = crypt_context.hash(_usuario.senha)
                try:
                    await session.merge(usuario)
                    await session.commit()
                except Exception:
                    return 'Não foi possível alterar usuario'
                await session.refresh(usuario)
                return usuario
            return 'Não foi possível alterar usuário'
            
    
    async def listar_usuario():
        async with async_session() as session:
            result = await session.execute(select(Usuario)
                .where(Usuario.deleted_at is None)
                .options(load_only(
                    Usuario.uuid, 
                    Usuario.nome, 
                    Usuario.email,
                    Usuario.status,
                ))
            )
            return result.scalars().all()
    
    async def pegar_usuario(_uuid: Uuid):
        async with async_session() as session:
            result = await session.execute(
                select(Usuario).where(and_(cast(Usuario.uuid, String)==_uuid), Usuario.deleted_at is None)
                .options(load_only(
                    Usuario.uuid, 
                    Usuario.nome, 
                    Usuario.email,
                    Usuario.status,
                ))
            )
            for usuario in result.scalars().all():
                return usuario
            return {}
    
    async def excluir_usuario(_uuid: Uuid):
        return await Usuario.delete(Usuario, async_session, _uuid)