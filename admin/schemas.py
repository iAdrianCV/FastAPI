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

