from datetime import datetime,timedelta
from app.settings import TokensConfig
from jose import JWTError,jwt
from passlib.context import CryptContext


from fastapi import Depends
from database.client import get_database
from app.auth import oauth2_scheme
from app.settings  import get_tokens_config
from app.exceptions import access_token_exception,credentials_exception
from app.schemas import TokenData
from institucion.crud import get_institucion_by_email

#FastAPI
from fastapi.security import OAuth2PasswordBearer

#App
from app.auth import verify_password
from app.auth  import TokensConfig
from app.settings import get_tokens_config
from app.auth import oauth2_scheme
from app.schemas import TokenData
from app.exceptions import (credentials_exception,
                            access_token_exception,
                            inactive_user_exception)


def authenticate_institucion(db, email: str, password: str,):
    institucion = get_institucion_by_email(db, email)
    if not institucion:
        return False
    if not verify_password(password, institucion.password):
        return False
    return institucion

def create_institucion_token(data: dict,tokens_config:TokensConfig, access=True):
    to_encode = data.copy()
    if access:
        expire = datetime.utcnow() + timedelta(days=3)
        scope = "access_token"
    else:
        expire = datetime.utcnow() + timedelta(days=2)
        scope = "refresh_token"
    to_encode.update({"user_type": "institucion"})
    to_encode.update({"exp": expire})
    to_encode.update({"scope": scope})
    encoded_jwt=jwt.encode(to_encode,
                            tokens_config.SECRET_KEY,
                            algorithm=tokens_config.JMV_ALGORITHM)
    return encoded_jwt

async def get_current_institucion(token: str = Depends(oauth2_scheme),
                                db=Depends(get_database),
                               tokens_config:TokensConfig=Depends(get_tokens_config)):

    try:
        payload=jwt.decode(token=token,
                            key=tokens_config.SECRET_KEY,
                            algorithms=[tokens_config.JMV_ALGORITHM])
        scope:str=payload.get("scope")
        if scope!="access_token":
            raise access_token_exception

        email: str = payload.get("email")
        
        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    institucion=get_institucion_by_email(db,token_data.email)
    if institucion is None:
        raise credentials_exception
    return institucion
