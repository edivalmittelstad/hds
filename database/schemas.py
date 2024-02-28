from pydantic import BaseModel

class StandardOutput(BaseModel):
  message: str

class ErrorOutput(BaseModel):
  detail: str
  teste: str | None = None
