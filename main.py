from fastapi import FastAPI, APIRouter
import uvicorn

from database.connection import teste_db 
from src.Usuario.view import usuario_router
from src.Auth.view import auth_router
from src.Hd.view import hd_router
from src.Objeto.view import objeto_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
  "*",
]

app = FastAPI()
router = APIRouter()

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@router.get('/')
def index():
    return "TESTES"

@router.get('/testedb')
async def teste_dbdf():
  try:
      await teste_db()
      return "OK"
  except Exception:
      return "FAIL"

app.include_router(router)
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(hd_router)
app.include_router(objeto_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)