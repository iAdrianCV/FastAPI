from bson import ObjectId
from fastapi import HTTPException, status, Form, Depends
from candidato.schemas import Candidato, CandidatoCreate

def list_candidato(db_depends):
    collection_name=db_depends["candidato"]
    candidatos=list(collection_name.find())
    return candidatos


def create_candidato(candidato: CandidatoCreate, db_depends):
    collection_name=db_depends["candidato"]
    candidato_dict = candidato.dict()
    collection_name.insert_one(candidato_dict)
    return candidato_dict



def get_candidato_by_email(db_depends,email_candidato:str):
    collection_name=db_depends["candidato"]
    candidato=collection_name.find_one({'email':email_candidato})
    return candidato


# async def save_company(company: CompanyCreate, db_depends):
#     collection_name=db_depends["companies"]
#     collection_name.insert_one(company)

#     await simple_send(email=[company["email"]])
#     return company