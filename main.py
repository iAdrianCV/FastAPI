from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from admin.router import admin_routs 
from candidato.router import candidato_routs
from institucion.router import institucion_routs
from votante.router import votante_routs
from voto.router import voto_routs
from estadisticas.router import estadisticas_routs
from app.router import app_routs


app = FastAPI(
    title="Api sistema de votacion",
    contact={
        "name": "Diego Bejar",
        "email": "diebejardelaguila@gmail.com"
    })

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}


origins = [
    # your frontend port
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:4200",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(app_routs)
app.include_router(admin_routs)
app.include_router(candidato_routs)
app.include_router(institucion_routs)
app.include_router(votante_routs)
app.include_router(voto_routs)
app.include_router(estadisticas_routs)
