from pydantic import BaseModel

class HDCreateInput(BaseModel):
    nome: str
    descricao: str
    status: bool

class HDUpdateInput(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    status: bool | None = None
