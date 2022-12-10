#Python
from rich import print
#FastAPI
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

#App
from app.schemas import AccessAndRefreshToken
from app.exceptions import email_not_found_exception,incorrect_email_or_password_exception

from app.settings import  get_tokens_config
from app.settings import AppSettings, get_app_config
from app.auth import verify_password

#Admin
from admin.auth import get_current_admin,create_admin_token
from admin.schemas import Admin
from admin.crud import get_admin_by_email

#Institucion
from institucion.auth import get_current_institucion,create_institucion_token
from institucion.schemas import Institucion
from institucion.crud import get_institucion_by_email

#Votante
from votante.auth import get_current_votante,create_votante_token
from votante.schemas import Votante
from votante.crud import get_votante_by_email


#Database
from database.client import get_database

app_routs=APIRouter()

@app_routs.get(path="/",include_in_schema=False)
async def redirect_to_documentation(app_settings:AppSettings=Depends(get_app_config)):
    return  RedirectResponse(url=f"{app_settings.BACKEND_HOST}/docs")


@app_routs.post(path="/api/login/",
                        response_model=AccessAndRefreshToken,
                        tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                tokens_config=Depends(get_tokens_config),
                                db=Depends(get_database)):

    user_type =""
    
    admin_db=get_admin_by_email(db,form_data.username)
    if admin_db:
        user_type = "admin"

    votante_db=get_votante_by_email(db,form_data.username)
    if votante_db:
        user_type = "votante"

    institucion_db=get_institucion_by_email(db,form_data.username)
    if institucion_db:
        user_type = "institucion"

    if user_type == "":
        raise email_not_found_exception

    else:
        if user_type=="admin":
            if not verify_password(form_data.password,admin_db["password"]):
                print("llega aqui")
                raise incorrect_email_or_password_exception
            data = {"email":admin_db["email"]}
            access_token = create_admin_token(data, tokens_config,access=True)
            refresh_token = create_admin_token(data, tokens_config, access=False)
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

        if user_type=="votante":
            if not verify_password(form_data.password,votante_db["password"]):
                raise incorrect_email_or_password_exception
            data = {"email":votante_db["email"]}
            access_token = create_votante_token(data, tokens_config,access=True)
            refresh_token = create_votante_token(data, tokens_config, access=False)
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        
        if user_type=="institucion":
            if not verify_password(form_data.password,institucion_db["password"]):
                raise incorrect_email_or_password_exception
            data = {"email":institucion_db["email"]}
            access_token = create_institucion_token(data, tokens_config,access=True)
            refresh_token = create_institucion_token(data, tokens_config, access=False)
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



