from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from rich import print
from bson import ObjectId
from enum import Enum
from datetime import date


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class AdminBase(BaseModel):
    nombre:str
    puesto:str
    privilegios: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str
    pass

class Admin(AdminBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombre": "Diego ronaldo",
                "puesto" : "Gerente municipal",
                "privilegios": "totales",
                "email": "ronaldo@gmail.com"
            }
        }

class UpdateAdmin(BaseModel):
    nombre:Optional[str]
    puesto:Optional[str]
    privilegios: Optional[str]
    email: Optional[EmailStr]

    def dict(self):
        data={}
        if self.nombre:
            data["nombre"]=self.nombre
        if self.puesto:
            data["ciclo"]=self.puesto
        if self.privilegios:
            data["horas"]=self.privilegios
        if self.email:
            data["email"]=self.email

        return data







class VotanteAptoBase(BaseModel):
    nombres:str
    apellidos:str
    dni:str
    fecha_nacimiento: date 
    fecha_emision: date
    fecha_vencimiento: date

class VotanteAptoCreate(VotanteAptoBase):
    pass

class VotanteApto(VotanteAptoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombres": "Diego ronaldo",
                "apellidos" : "Arellano Bardales",
                "dni": "75847852",
                "fecha_nacimiento": "1995-11-05",
                "fecha_emision": "2005-11-05",
                "fecha_vencimiento": "2023-11-05",
            }
        }