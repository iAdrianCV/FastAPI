from bson import ObjectId
from fastapi import HTTPException, status, Form, Depends
from votante.schemas import Votante, VotanteCreate

def list_votante(db_depends):
    collection_name=db_depends["votante"]
    votantees=list(collection_name.find())
    return votantees


def create_votante(votante: VotanteCreate, db_depends):
    collection_name=db_depends["votante"]
    votante_dict = votante.dict()
    collection_name.insert_one(votante_dict)
    return votante_dict



# async def save_company(company: CompanyCreate, db_depends):
#     collection_name=db_depends["companies"]
#     collection_name.insert_one(company)

#     await simple_send(email=[company["email"]])
#     return company


def get_votante_by_email(db_depends,email_votante:str):
    collection_name=db_depends["votante"]
    votante=collection_name.find_one({'email':email_votante})
    return votante