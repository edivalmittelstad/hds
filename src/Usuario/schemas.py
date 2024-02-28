from pydantic import BaseModel
from typing import List

from database.models import Roles

class UsuarioCreateInput(BaseModel):
    nome: str
    email: str
    senha: str
    cpf: str
    foto: str | None = None
    status: bool
    roles: List[Roles]

class UsuarioUpdateInput(BaseModel):
    nome: str | None = None
    email: str | None = None
    senha: str | None = None
    foto: str | None = None
    status: bool | None = None
    roles: List[Roles]
