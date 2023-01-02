from bson import ObjectId
from fastapi import HTTPException, status, Form, Depends
from admin.schemas import Admin, AdminCreate

def list_admin(db_depends):
    collection_name=db_depends["admin"]
    admins=list(collection_name.find())
    return admins


def create_admin(admin: AdminCreate, db_depends):
    collection_name=db_depends["admin"]
    admin_dict = admin.dict()
    collection_name.insert_one(admin_dict)
    return admin_dict



# async def save_company(company: CompanyCreate, db_depends):
#     collection_name=db_depends["companies"]
#     collection_name.insert_one(company)

#     await simple_send(email=[company["email"]])
#     return company

def get_admin_by_email(db_depends,email_admin:str):
    collection_name=db_depends["admin"]
    admin=collection_name.find_one({'email':email_admin})
    return admin


def edit_votante_apto(dni_votante_apto: str, votante_apto_data: UpdateVotanteApto, db_depends):
    collection_name=db_depends["votantes_aptos"]
    query={'dni': dni_votante_apto}
    new_values={'$set':votante_apto_data.dict()}
    collection_name.update_one(query, new_values)
    return collection_name.find_one(query)
