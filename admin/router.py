from database.client import get_database
from admin.schemas import ObjectId
from typing import List
from candidato.crud import list_candidato, create_candidato
from admin.crud import list_admin, create_admin
from admin.schemas import Admin, AdminCreate, VotanteApto, VotanteCreate
from candidato.schemas import Candidato, CandidatoCreate
from institucion.crud import list_institucion, create_institucion
from institucion.schemas import Institucion, InstitucionCreate
from admin.auth import get_current_admin
from votante.crud import list_votante, create_votante
from datetime import datetime, date
from pydantic import EmailStr
from app.exceptions import diferent_passwords_exception, registred_email_exception
from app.utils import validation_email_candidato_exist
import pandas as pd


from votante.schemas import Votante, VotanteCreate

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)


admin_routs = APIRouter()

#Get list 
@admin_routs.get(
    path="/api/admin",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=List[Admin]
)
async def get_admins(
    admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)):
    return list_admin(db)

@admin_routs.get(
    path="/api/admin/candidatos",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=List[Candidato]
)
async def get_candidatos(
    admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)):
    return list_candidato(db)

@admin_routs.get(
    path="/api/institucion",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=List[Institucion]
)
async def get_institucions(
    admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)):
    return list_institucion(db)

@admin_routs.get(
    path="/api/votante",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=List[Votante]
)
async def get_votantes(
    admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)):
    return list_votante(db)


@admin_routs.get(path="/api/admin/{admin_id}",
                tags=["admin"],
                response_model=Admin
                )
async def get_admin(admin_id:str,
                admin:Admin=Depends(get_current_admin),
                db=Depends(get_database)):
    collection_name=db["admin"]
    admin=collection_name.find_one({'_id':ObjectId(admin_id)})
    if admin:
        return admin
    else:
        return "the item is not found"



#Crear Admin
@admin_routs.post(
    path="/api/admin/",
    tags=["admin"],
    status_code=status.HTTP_201_CREATED,
    response_model=Admin
)
async def save_admin(admin: AdminCreate,
                admin_user:Admin=Depends(get_current_admin),
                db=Depends(get_database)):
    collection_name=db["admin"]
    admin=admin.dict()
    collection_name.insert_one(admin)
    return admin

#Create other entities
@admin_routs.post(
    path="/api/admin/candidato/",
    tags=["admin"],
    status_code=status.HTTP_201_CREATED,
    response_model=Candidato
)
async def save_candidato(nombres: str = Form(...,example="Alejandro"),
                    apellidos: str = Form(...,example="Merino Bardales"),
                    dni: str = Form(..., example="75845636"),
                    rol: str = Form(...,example="jne"),
                    partido_politico: str = Form(...,example="jne"),
                    email: EmailStr = Form(...,example="ronaldo@gmail.com"),
                    password: str = Form(...,example="1234"),
                    password_confirmation: str = Form(...,example="1234"),
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    if not password.__eq__(password_confirmation):
        raise diferent_passwords_exception

    email_exist = validation_email_candidato_exist(db, email, "candidato")
    if email_exist:
        raise registred_email_exception

    candidato = {
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": str(dni),
        "rol": rol,
        "partido_politico": partido_politico,
        "email": email,
        "password": password
    }

    collection_name=db["candidato"]
    collection_name.insert_one(candidato)
    return candidato


@admin_routs.post(
    path="/api/admin/institucion/",
    tags=["admin"],
    status_code=status.HTTP_201_CREATED,
    response_model=Institucion
)
async def save_institucion(nombres: str = Form(...,example="Alejandro"),
                    apellidos: str = Form(...,example="Merino Bardales"),
                    dni: str = Form(..., example="75845636"),
                    rol: str = Form(...,example="jne"),
                    cargo: str = Form(...,example="Directo"),
                    entidad: str = Form(...,example="jne"),
                    email: EmailStr = Form(...,example="ronaldo@gmail.com"),
                    password: str = Form(...,example="1234"),
                    password_confirmation: str = Form(...,example="1234"),
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    if not password.__eq__(password_confirmation):
        raise diferent_passwords_exception

    email_exist = validation_email_candidato_exist(db, email, "institucion")
    if email_exist:
        raise registred_email_exception

    institucion = {
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "rol": rol,
        "cargo": cargo,
        "entidad": entidad,
        "email": email,
        "password": password
    }

    collection_name=db["institucion"]
    collection_name.insert_one(institucion)
    return institucion


#Deletes
@admin_routs.delete(path="/api/admin/{admin_id}",
                    tags=["admin"])
async def delete_admin(admin_id:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["admin"]
    collection_name.delete_one({'_id':ObjectId(admin_id)})
    return "this item has been deleted"

@admin_routs.delete(path="/api/admin/candidato/{candidato_id}",
                    tags=["admin"])
async def delete_candidato(candidato_id:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["candidato"]
    collection_name.delete_one({'_id':ObjectId(candidato_id)})
    return "this item has been deleted"

@admin_routs.delete(path="/api/admin/institucion/{institucion_id}",
                    tags=["admin"])
async def delete_institucion(institucion_id:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["institucion"]
    collection_name.delete_one({'_id':ObjectId(institucion_id)})
    return "this item has been deleted"

@admin_routs.delete(path="/api/admin/votante/{votante_id}",
                    tags=["admin"])
async def delete_votante(votante_id:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["votante"]
    collection_name.delete_one({'_id':ObjectId(votante_id)})
    return "this item has been deleted"


#Crear Votantes mediante excel
@admin_routs.post(
    path="/api/admin/votantes_aptos",
    tags=["admin"],
    # status_code=status.HTTP_201_CREATED,
    # response_model=Admin
)
async def save_votantes_aptos(
    data_votantes: UploadFile = File(...) ,
    admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)
    
):
    collection_votantes_aptos = db["votantes_aptos"]
    votantes_create = []

    df = pd.read_excel(data_votantes.file.read())
    print(df)
    votantes_row = df.to_dict(orient='index')    

    dni_exist_list = []
    for votante_apto in list(votantes_row.values()):
        dni_exist = db["votantes_aptos"].find_one({
                "dni": votante_apto["dni"]
         })

        if dni_exist:
            dni_exist_list.append(dni_exist["dni"])
        else:
            votante_apto_create = {
                "nombres":votante_apto["nombres"],
                "apellidos":votante_apto["apellidos"],
                "dni": str(votante_apto["dni"]),
                "fecha_nacimiento": votante_apto["fecha_nacimiento"],
                "fecha_emision": votante_apto["fecha_emision"],
                "fecha_vencimiento": votante_apto["fecha_vencimiento"]
            }
            votantes_create.append(votante_apto_create)
        
    if len(votantes_create)>0:
        collection_votantes_aptos.insert_many(votantes_create)


    if len(dni_exist_list)>0:
        return f"La mayoria de datos fueron creados a excepcion de: {dni_exist_list}"

    return "Datos creados con exito"



@admin_routs.get(
    path="/api/votante_apto",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=List[VotanteApto]
)
async def get_votantes_aptops(
    # admin:Admin=Depends(get_current_admin),
    db=Depends(get_database)):

    collection_votantes_aptos = db["votantes_aptos"]
    list_votante = list(collection_votantes_aptos.find())

    if not list_votante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="votantes no encontrados")
    return list_votante


@admin_routs.get(
    path="/api/votante_apto/{dni_votante_apto}",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=VotanteApto
)
async def get_votante_aptop(
    dni_votante_apto:str,
    db=Depends(get_database)):

    collection_votantes_aptos = db["votantes_aptos"]
    votante_apto = collection_votantes_aptos.find_one({'dni':dni_votante_apto})
    if not votante_apto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="votante no encontrado")
    
    return votante_apto

















