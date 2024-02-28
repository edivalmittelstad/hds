from typing import Annotated
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Security,
    status,
)

from database.connection import async_session
from database.models import Usuario, HD
from .schemas import HDCreateInput, HDUpdateInput
from .services import HDService
from ..Auth.view import token_verify

hd_router = APIRouter(prefix="/hd")

@hd_router.post("")
async def create(input: HDCreateInput):
    try:
        # res = await HDService.create(HD, input)
        res = await HD.create(HD, async_session, input)
        return res
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@hd_router.put("/{uuid}")
async def update(
    uuid: str,
    input: HDUpdateInput,
    current_user: Annotated[Usuario, Depends(token_verify)],
):
    try:
        res = await HDService.update(uuid, input)
        if res:
            return HTTPException(status.HTTP_200_OK, detail="Atualizado com sucesso!")
        return HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao atualizar!"
        )
    except Exception as error:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=str(error))

@hd_router.get("")
async def listar(current_user: Annotated[Usuario, Depends(token_verify)]):
    try:
        res = await HDService.listar()
        return res
    except Exception as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))

@hd_router.get("/{uuid}")
async def pegar(uuid: str, current_user: Annotated[Usuario, Security(token_verify)]):
    try:
        res = await HDService.pegar(uuid)
        return res
    except Exception as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))

@hd_router.delete("/{uuid}")
async def excluir(uuid: str, current_user: Annotated[Usuario, Depends(token_verify)]):
    try:
        res = await HDService.excluir(uuid)
        if res:
            return HTTPException(status.HTTP_200_OK, detail="Excluido com sucesso!")
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao excluir!")
    except Exception:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail="Erro ao excluir!")
