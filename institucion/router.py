from database.client import get_database
from institucion.schemas import ObjectId
from typing import List
from institucion.crud import list_institucion, create_institucion
from institucion.schemas import Institucion, InstitucionCreate
from admin.schemas import Admin, AdminCreate
from admin.auth import get_current_admin

from fastapi import (
    APIRouter, HTTPException, Depends, 
    status, File, UploadFile, Form
)


institucion_routs = APIRouter()

@institucion_routs.get(path="/api/institucion/{institucion_id}",
                tags=["Institucion"],
                response_model=Institucion
                )
async def get_institucion(
                institucion_id:str,
                admin:Admin=Depends(get_current_admin),
                db=Depends(get_database)):
    collection_name=db["institucion"]
    institucion=collection_name.find_one({'_id':ObjectId(institucion_id)})
    if institucion:
        return institucion
    else:
        return "the item is not found"



