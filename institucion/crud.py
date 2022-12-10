from bson import ObjectId
from fastapi import HTTPException, status, Form, Depends
from institucion.schemas import Institucion, InstitucionCreate

def list_institucion(db_depends):
    collection_name=db_depends["institucion"]
    instituciones=list(collection_name.find())
    return instituciones


def create_institucion(institucion: InstitucionCreate, db_depends):
    collection_name=db_depends["institucion"]
    institucion_dict = institucion.dict()
    collection_name.insert_one(institucion_dict)
    return institucion_dict



# async def save_company(company: CompanyCreate, db_depends):
#     collection_name=db_depends["companies"]
#     collection_name.insert_one(company)

#     await simple_send(email=[company["email"]])
#     return company


def get_institucion_by_email(db_depends,email_institucion:str):
    collection_name=db_depends["institucion"]
    institucion=collection_name.find_one({'email':email_institucion})
    return institucion