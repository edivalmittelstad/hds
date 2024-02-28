from pydantic import BaseModel

class ObjetoCreateInput(BaseModel):
    nome: str
    hd_id: int| None = None
    objeto_id: int

class ObjetoUpdateInput(BaseModel):
    nome: str | None = None
    hd_id: int| None = None
    objeto_id: int
    