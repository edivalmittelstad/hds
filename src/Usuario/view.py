from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Security

from database.models import Usuario

from .schemas import UsuarioCreateInput, UsuarioUpdateInput
from .services import UsuarioService
from ..Auth.view import token_verify

usuario_router = APIRouter(prefix="/usuario")

@usuario_router.post("")
async def usuario_create(usuario_input: UsuarioCreateInput):
  try:
    res = await UsuarioService.create_usuario(usuario_input)
    return res
  except Exception as error:
    raise HTTPException(400, detail=str(error))

@usuario_router.put("/{uuid}")
async def usuario_update(
  uuid: str,
  usuario_input: UsuarioUpdateInput,
  current_user: Annotated[Usuario, Depends(token_verify)],
):
  try:
    res = await UsuarioService.update_usuario(uuid, usuario_input)
    return res
  except Exception as error:
    raise HTTPException(400, detail=str(error))

@usuario_router.get("")
async def listar(current_user: Annotated[Usuario, Depends(token_verify)]):
  try:
    res = await UsuarioService.listar_usuario()
    return res
  except Exception as error:
    raise HTTPException(400, detail=str(error))

@usuario_router.get("/{uuid}")
async def pegar(uuid: str, current_user: Annotated[Usuario, Security(token_verify)]):
  try:
    res = await UsuarioService.pegar_usuario(uuid)
    return res
  except Exception as error:
    raise HTTPException(400, detail=str(error))

@usuario_router.delete("/{uuid}")
async def excluir(uuid: str, current_user: Annotated[Usuario, Depends(token_verify)]):
  try:
    res = await UsuarioService.excluir_usuario(uuid)
    return res
  except Exception as error:
    raise HTTPException(400, detail=str(error))
