from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from cryptography.hazmat.primitives import serialization

import jwt
from sqlalchemy import String, cast, and_
from sqlalchemy.future import select
from sqlalchemy.orm import undefer
from fastapi.security import OAuth2PasswordBearer

from database.models import Usuario
from database.connection import async_session
from .schemas import UsuarioLoginInput, PayloadResponsoToken

private_key = open('.ssh/id_rsa', 'r').read()
public_key = open('.ssh/id_rsa.pub', 'r').read()
publickey = serialization.load_ssh_public_key(public_key.encode())
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')
crypt_context   = CryptContext(schemes=['sha256_crypt'])
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

class AuthService:
    async def login_usuario(_usuario: UsuarioLoginInput, expires_in: int = 300):
        async with async_session() as session:
            usuarios = await session.execute(select(Usuario).where(and_(Usuario.email==_usuario.email,  Usuario.deleted_at == None))
                .options(undefer(Usuario.senha))
            )
            for usuario in usuarios.scalars().all():
                if not crypt_context.verify(_usuario.senha, usuario.senha):
                    return 'Usuário ou senha inválido'
                exp = datetime.utcnow() + timedelta(minutes=expires_in)
                payload : PayloadResponsoToken = {
                    'uuid': str(usuario.uuid),
                    'nome': usuario.nome,
                    'sub': usuario.email,
                    'exp': exp
                }
                access_token = jwt.encode(payload, key, algorithm='RS256')
                return {
                    'dados': payload,
                    'token': access_token,
                    'exp': exp.isoformat()
                }
            return 'Usuário ou senha inválido'

    async def verify_token(token):
        try:
            data:PayloadResponsoToken = jwt.decode(token, public_key, algorithms=['RS256', ])
        except:
            raise HTTPException(400, detail=str("Acesso inválido / Sessão inspirada"))
        async with async_session() as session:
            usuarios = await session.execute(select(Usuario).where(and_(cast(Usuario.uuid, String)==data['uuid']), Usuario.deleted_at == None))
            for usuario in usuarios.scalars().all():
                return usuario
            raise HTTPException(400, detail=str("Acesso inválido / Sessão inspirada"))