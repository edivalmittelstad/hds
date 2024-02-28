from typing import Annotated
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Security,
    status,
)

from database.models import Usuario
from .schemas import ObjetoCreateInput, ObjetoUpdateInput
from .services import ObjetoService
from ..Auth.view import token_verify

objeto_router = APIRouter(prefix="/objeto")

@objeto_router.post("")
async def create(input: ObjetoCreateInput):
    try:
        res = await ObjetoService.create(input)
        return res
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@objeto_router.put("/{uuid}")
async def update(
    uuid: str,
    input: ObjetoUpdateInput,
    current_user: Annotated[Usuario, Depends(token_verify)],
):
    try:
        res = await ObjetoService.update(uuid, input)
        if res:
            return HTTPException(status.HTTP_200_OK, detail="Atualizado com sucesso!")
        return HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao atualizar!"
        )
    except Exception as error:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=str(error))

@objeto_router.get("")
async def listar(current_user: Annotated[Usuario, Depends(token_verify)]):
    try:
        res = await ObjetoService.listar()
        return res
    except Exception as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))

@objeto_router.get("/{uuid}")
async def pegar(uuid: str, current_user: Annotated[Usuario, Security(token_verify)]):
    try:
        res = await ObjetoService.pegar(uuid)
        return res
    except Exception as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))

@objeto_router.delete("/{uuid}")
async def excluir(uuid: str, current_user: Annotated[Usuario, Depends(token_verify)]):
    try:
        res = await ObjetoService.excluir(uuid)
        if res:
            return HTTPException(status.HTTP_200_OK, detail="Excluido com sucesso!")
        return HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao excluir!")
    except Exception:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail="Erro ao excluir!")
