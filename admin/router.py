
from database.client import get_database
from admin.schemas import ObjectId
from typing import List
from candidato.crud import list_candidato
from admin.crud import list_admin
from admin.schemas import Admin, AdminCreate, VotanteApto
from candidato.schemas import Candidato
from institucion.crud import list_institucion
from institucion.schemas import Institucion
from admin.auth import get_current_admin
from votante.crud import list_votante
from pydantic import EmailStr
from app.exceptions import diferent_passwords_exception, registred_email_exception
from app.utils import validation_email_candidato_exist
import pandas as pd
from app.auth import get_password_hash
from app.exceptions import riesgos_exception
from typing import Optional


from votante.schemas import Votante

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



@admin_routs.get(path="/api/admin/institucion/{institucion_dni}",
                tags=["admin"],
                response_model=Institucion
                )
async def get_institucion(
                institucion_dni:str,
                admin:Admin=Depends(get_current_admin),
                db=Depends(get_database)):
    collection_name=db["institucion"]
    institucion=collection_name.find_one({'dni': institucion_dni})
    if institucion:
        return institucion
    else:
        return "the item is not found"




@admin_routs.get(path="/api/admin/candidato/{candidato_dni}",
                tags=["admin"],
                response_model=Candidato
                )
async def get_candidato(candidato_dni:str,
                admin:Admin=Depends(get_current_admin),
                db=Depends(get_database)
):
    collection_name=db["candidato"]
    candidato=collection_name.find_one({'dni':candidato_dni})
    if candidato:
        return candidato
    else:
        return "the item is not found"

@admin_routs.get(path="/api/admin/votante-apto/{votante_dni}",
                tags=["admin"],
                response_model=Votante
                )
async def get_votante(votante_dni:str,db=Depends(get_database)):
    collection_name=db["votantes_aptos"]
    votante=collection_name.find_one({'dni':votante_dni})
    if votante:
        return votante
    else:
        return "the item is not found"




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
                db=Depends(get_database)):
    collection_name=db["admin"]
    admin = {
        "nombre": admin["nombre"],
        "puesto": admin["puesto"],
        "privilegios": admin["privilegios"],
        "email": admin["email"],
        "password": get_password_hash(admin["password"])
    }
    
    
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
        "password": get_password_hash(password)
    }

    collection_name=db["candidato"]
    collection_name.insert_one(candidato)
    return candidato




@admin_routs.post(
    path="/api/admin/votante-apto/",
    tags=["admin"],
    status_code=status.HTTP_201_CREATED,
    response_model=VotanteApto
)
async def save_votante_apto(nombres: str = Form(...,example="Alejandro"),
                    apellidos: str = Form(...,example="Merino Bardales"),
                    dni: str = Form(..., example="75845636"),
                    fecha_nacimiento: str = Form(...,example="2022-10-15"),
                    fecha_emision: str = Form(...,example="2022-10-15"),
                    fecha_vencimiento: str = Form(...,example="2022-10-15"),
                    db=Depends(get_database)):


    votante_apto_exist = db["votantes_aptos"].find_one({'dni':dni})

    if votante_apto_exist:
        raise riesgos_exception(status.HTTP_400_BAD_REQUEST, detail="No estas autorizado a votar")

    votante_apto = {
        "nombres": nombres,
        "apellidos" :apellidos,
        "dni": dni,
        "fecha_nacimiento": fecha_nacimiento,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento,
    }

    collection_name=db["votantes_aptos"]
    collection_name.insert_one(votante_apto)
    return votante_apto









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
        "password": get_password_hash(password)
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

@admin_routs.delete(path="/api/admin/candidato/{dni_candidato}",
                    tags=["admin"])
async def delete_candidato(dni_candidato:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["candidato"]
    collection_name.delete_one({'dni': dni_candidato})
    return "this item has been deleted"

@admin_routs.delete(path="/api/admin/institucion/{dni_institucion}",
                    tags=["admin"])
async def delete_institucion(dni_institucion:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["institucion"]
    collection_name.delete_one({'dni': dni_institucion})
    return "this item has been deleted"


@admin_routs.delete(path="/api/admin/votante-apto/{dni_votante_apto}",
                    tags=["admin"])
async def delete_institucion(dni_votante_apto:str,
                    admin:Admin=Depends(get_current_admin),
                    db=Depends(get_database)):
    collection_name=db["votantes_aptos"]
    collection_name.delete_one({'dni': dni_votante_apto})

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






#edits



@admin_routs.put(
    path="/api/admin/votante_apto/",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=VotanteApto
)
async def update_votante_apto(
                        admin:Admin=Depends(get_current_admin),
                        nombres: Optional[str] = Form(None, example="Alejandro"),
                        apellidos: Optional[str] = Form(None, example="Merino Bardales"),
                        dni: Optional[str] = Form(None, example="75845636"),
                        fecha_nacimiento: Optional[str] = Form(None, example="2022-10-15"),
                        fecha_emision: Optional[str] = Form(None, example="2022-10-15"),
                        fecha_vencimiento: Optional[str] = Form(None, example="2022-10-15"),
                        
                        db=Depends(get_database)):


    votante_apto_update = {
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha_nacimiento": fecha_nacimiento,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento
    }


    collection_name=db["votantes_aptos"]
    query={'dni': dni}
    new_values={'$set':votante_apto_update}
    collection_name.update_one(query, new_values)


    return collection_name.find_one({'dni': dni})




@admin_routs.put(
    path="/api/admin/candidato/",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=Candidato
)
async def update_candidato(
                        admin:Admin=Depends(get_current_admin),
                        nombres: Optional[str] = Form(None, example="Alejandro"),
                        apellidos: Optional[str] = Form(None, example="Merino Bardales"),
                        dni: Optional[str] = Form(None, example="77777777"),
                        rol : Optional[str] = Form(None, example="candidato"),
                        partido_politico : Optional[str] = Form(None, example="Somos Peru"),
                        email : Optional[str] = Form(None, example="candidato@gmail.com"),
                        
                        db=Depends(get_database)):


    candidato_update = {
        "nombres": nombres,
        "apellidos": apellidos,
        "rol": rol,
        "partido_politico": partido_politico,
        "email": email
    }


    collection_name=db["candidato"]
    query={'dni': dni}
    new_values={'$set':candidato_update}
    collection_name.update_one(query, new_values)


    return collection_name.find_one({'dni': dni})




@admin_routs.put(
    path="/api/admin/institucion/",
    tags=["admin"],
    status_code=status.HTTP_200_OK,
    response_model=Institucion
)
async def update_institucion(
                        admin:Admin=Depends(get_current_admin),
                        nombres: Optional[str] = Form(None, example="Alejandro"),
                        apellidos: Optional[str] = Form(None, example="Merino Bardales"),
                        dni: Optional[str] = Form(None, example="77777777"),
                        rol : Optional[str] = Form(None, example="institucion"),
                        cargo : Optional[str] = Form(None, example="onpe"),
                        entidad  : Optional[str] = Form(None, example="onpe"),
                        email   : Optional[str] = Form(None, example="onpe@gmail.com"),
                        db=Depends(get_database)):

    #asdas
    institucion_update = {
        "nombres": nombres,
        "apellidos": apellidos,
        "rol": rol,
        "cargo": cargo,
        "entidad": entidad,
        "email": email

    }


    collection_name=db["institucion"]
    query={'dni': dni}
    new_values={'$set':institucion_update}
    collection_name.update_one(query, new_values)


    return collection_name.find_one({'dni': dni})












