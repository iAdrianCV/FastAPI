from database.client import get_database
from votante.schemas import ObjectId
from datetime import datetime, date
from pydantic import EmailStr
from app.exceptions import diferent_passwords_exception, registred_email_exception, riesgos_exception
from app.utils import validation_email_candidato_exist
from votante.crud import list_votante, create_votante
from votante.schemas import Votante, VotanteCreate
from app.auth import get_password_hash

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)


votante_routs = APIRouter()

@votante_routs.get(path="/api/votante/{votante_id}",
                tags=["Votante"],
                response_model=Votante
                )
async def get_votante(votante_id:str,db=Depends(get_database)):
    collection_name=db["votante"]
    votante=collection_name.find_one({'_id':ObjectId(votante_id)})
    if votante:
        return votante
    else:
        return "the item is not found"

@votante_routs.post(
    path="/api/votante/",
    tags=["Votante"],
    status_code=status.HTTP_201_CREATED,
    response_model=Votante
)
async def save_votante(nombres: str = Form(...,example="Alejandro"),
                    apellidos: str = Form(...,example="Merino Bardales"),
                    dni: str = Form(..., example="75845636"),
                    fecha_nacimiento: str = Form(...,example="2022-10-15"),
                    fecha_emision: str = Form(...,example="2022-10-15"),
                    fecha_vencimiento: str = Form(...,example="2022-10-15"),
                    email: EmailStr = Form(...,example="diego@gmail.com"),
                    password: str = Form(...,example="1234"),
                    password_confirmation: str = Form(...,example="1234"),
                    db=Depends(get_database)):
    if not password.__eq__(password_confirmation):
        raise diferent_passwords_exception

    votante_apto_exist = db["votantes_aptos"].find_one({'dni':dni})

    if not votante_apto_exist:
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="No estas autorizado a votar")

    votante_exist = db["votante"].find_one({'dni': dni})
    if votante_exist:
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="Ya estas registrado con el dni")

    email_exist = validation_email_candidato_exist(db, email, "votante")
    if email_exist:
        raise registred_email_exception

   

    print(dni)
    

    print(fecha_nacimiento)
    print(votante_apto_exist["fecha_nacimiento"])
    print("**")
    print(fecha_emision)
    print(votante_apto_exist["fecha_emision"])
    print("**")
    print(fecha_vencimiento)
    print(votante_apto_exist["fecha_vencimiento"])

    if not fecha_nacimiento.__eq__(votante_apto_exist["fecha_nacimiento"]) and fecha_emision.__eq__(votante_apto_exist["fecha_emision"]) and fecha_vencimiento.__eq__(votante_apto_exist["fecha_vencimiento"]):
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="Datos erroneos")

    votante = {
        "nombres": nombres,
        "apellidos" :apellidos,
        "dni": dni,
        "fecha_nacimiento": fecha_nacimiento,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento,
        "email": email,
        "password": get_password_hash(password)
    }

    collection_name=db["votante"]
    collection_name.insert_one(votante)
    return votante




