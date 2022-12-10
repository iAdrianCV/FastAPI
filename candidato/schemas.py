from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from rich import print
from bson import ObjectId
from enum import Enum



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

class CandidatoBase(BaseModel):
    nombres:str
    apellidos:str
    dni:str
    rol:str
    partido_politico: str
    email: EmailStr

class CandidatoCreate(CandidatoBase):
    password: str
    pass

class Candidato(CandidatoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombres": "Diego ronaldo",
                "apellidos" : "Garcio Barco",
                "dni": "totales",
                "rol": "candidato",
                "partido_politico": "Somos Peru",
                "email" : "gerente@gmail.com",

            }
        }

class UpdateCandidato(BaseModel):
    nombres:Optional[str]
    apellidos:Optional[str]
    dni:Optional[str]
    rol:Optional[str]
    partido_politico: Optional[str]
    email: Optional[EmailStr]

    def dict(self):
        data={}
        if self.nombres:
            data["nombres"]=self.nombres
        if self.apellidos:
            data["apellidos"]=self.apellidos
        if self.dni:
            data["dni"]=self.dni
        if self.rol:
            data["rol"]=self.rol
        if self.partido_politico:
            data["partido_politico"]=self.partido_politico
        if self.email:
            data["email"]=self.email


        return data

