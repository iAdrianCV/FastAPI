from database.client import get_database
from candidato.schemas import ObjectId
from typing import List

from candidato.crud import list_candidato, create_candidato
from candidato.schemas import Candidato, CandidatoCreate
from votante.schemas import Votante
from votante.auth import get_current_votante

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)


candidato_routs = APIRouter()

@candidato_routs.get(
    path="/api/candidato",
    tags=["candidato"],
    status_code=status.HTTP_200_OK,
    response_model=List[Candidato]
)
async def get_candidatos(
    votante:Votante=Depends(get_current_votante),
    db=Depends(get_database)):
    return list_candidato(db)

@candidato_routs.get(path="/api/candidato/{candidato_dni}",
                tags=["candidato"],
                response_model=Candidato
                )
async def get_candidato(candidato_dni:str,
                votante:Votante=Depends(get_current_votante),
                db=Depends(get_database)):
    collection_name=db["candidato"]
    candidato=collection_name.find_one({'dni':candidato_dni})
    if candidato:
        return candidato
    else:
        return "the item is not found"
