# import re
from pydantic import BaseModel, validator

class UsuarioLoginInput(BaseModel):
    email: str
    senha: str

    # @validator('email')
    # def validate_email(cls, value):
    #     if not re.match('^([a-z]|[0-9]|@)+$', value):
    #         raise ValueError('Email inválido')
    #     return value

class PayloadResponsoToken(BaseModel):
    uuid: str
    nome: str
    sub: str
    exp: str
