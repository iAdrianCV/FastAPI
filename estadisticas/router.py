from database.client import get_database
from votante.schemas import ObjectId
from datetime import datetime, date
from pydantic import EmailStr
from app.exceptions import diferent_passwords_exception, registred_email_exception, riesgos_exception
from app.utils import validation_email_candidato_exist
from votante.crud import list_votante, create_votante
from votante.schemas import Votante, VotanteCreate
from estadisticas.schemas import Estadisticas, EstadisticasCreate, EstadisticasTotales
from institucion.auth import get_current_institucion
from institucion.schemas import Institucion

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)

estadisticas_routs = APIRouter()

@estadisticas_routs.get(path="/api/estadisticas/candidato/{dni_candidato}",
                tags=["Estadisticas"],
                response_model=Estadisticas
                )
async def get_votos_candidato(
    dni_candidato: str, 
    institucion:Institucion=Depends(get_current_institucion),
    db=Depends(get_database)):
    collection_name=db["voto"]
    query = {"dni_candidato": {"$eq": dni_candidato}}
    votos=len(list(collection_name.find(query)))

    if not institucion["rol"]=="onpe":
        raise riesgos_exception(status.HTTP_401_UNAUTHORIZED, "No eres usuario onpe")
        
    estadisticas = {
        "dni_candidato": dni_candidato,
        "cantidad_votos" : votos,
    }

    if estadisticas:
        return estadisticas
    else:
        return "the item is not found"

@estadisticas_routs.get(path="/api/estadisticas/",
                tags=["Estadisticas"],
                response_model=EstadisticasTotales
                )
async def get_votos(
    institucion:Institucion=Depends(get_current_institucion),
    db=Depends(get_database)):
    collection_name=db["voto"]
    votos=len(list(collection_name.find()))

    if not institucion["rol"]=="onpe":
        raise riesgos_exception(status.HTTP_401_UNAUTHORIZED, "No eres usuario onpe")
    
    estadisticas = {
        "cantidad_votos" : votos,
    }

    if estadisticas:
        return estadisticas
    else:
        return "the item is not found"


