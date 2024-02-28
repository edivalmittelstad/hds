from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from .schemas import ( UsuarioLoginInput )
from .services import AuthService

auth_router = APIRouter(prefix='/auth')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

@auth_router.post('/login')
async def usuario_login(usuario_input: UsuarioLoginInput):
    try:
        res = await AuthService.login_usuario(usuario_input)
        return res
    except Exception as error:
        raise HTTPException(400, detail=str(error))

async def token_verify(token = Depends(oauth_scheme)):
    usuario = await AuthService.verify_token(token)
    return usuario