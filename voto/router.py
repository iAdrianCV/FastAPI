from database.client import get_database
from votante.schemas import ObjectId
from datetime import datetime, date
from pydantic import EmailStr
from app.exceptions import diferent_passwords_exception, registred_email_exception, riesgos_exception
from app.utils import validation_email_candidato_exist
from votante.crud import list_votante, create_votante
from votante.schemas import Votante, VotanteCreate
from voto.schemas import Voto, VotoCreate
from votante.auth import get_current_votante

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)

voto_routs = APIRouter()


@voto_routs.get(path="/api/voto/candidato/{candidato_dni}",
                tags=["Voto"],
                response_model=list[Voto]
                )
async def get_voto(candidato_dni:str,
            votante:Votante=Depends(get_current_votante),
            db=Depends(get_database)):
    collection_name=db["voto"]
    query = {"dni_candidato": {"$eq": candidato_dni}}
    voto=list(collection_name.find(query))

    if voto:
        return voto
    else:
        return "the item is not found"

@voto_routs.post(
    path="/api/voto/candidato",
    tags=["Voto"],
    status_code=status.HTTP_201_CREATED,
    response_model=Voto
)
async def save_voto(
                    dni_candidato: str = Form(...,example="72863971"),
                    votante:Votante=Depends(get_current_votante),
                    db=Depends(get_database)):

    candidato_exist = db["candidato"].find_one({'dni': dni_candidato})
    if not candidato_exist:
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="No existe candidato")


    voto_exist = db["voto"].find_one({'dni_votante': votante["dni"]})
    if voto_exist:
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="El votante ya voto")

    voto = {
        "dni_votante": votante["dni"],
        "dni_candidato": dni_candidato
    }

    collection_name=db["voto"]
    collection_name.insert_one(voto)
    return voto




@voto_routs.get(path="/api/voto/votante",
                tags=["Voto"],
              
                )
async def get_voto(
            votante:Votante=Depends(get_current_votante),
            db=Depends(get_database)):
    collection_name=db["voto"]
    voto=collection_name.find_one({'dni':votante["dni"]})
    voto_exitoso = False
    if voto:
        voto_exitoso = True
        return {
            "voto_exitoso": voto_exitoso
        }
    else:
        return {
            "voto_exitoso": voto_exitoso
        }




