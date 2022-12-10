from fastapi import HTTPException, status 


def riesgos_exception(status_code,detail:str,headers:dict={}):
    return HTTPException(status_code=status_code,
                        detail=detail,
                        headers=headers)


diferent_passwords_exception=HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The passwords are not equals")

credentials_exception = HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"})

access_token_exception=HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials,Send access token",
                        headers={"WWW-Authenticate": "Bearer"})

refresh_token_exception=HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials,Send refresh token",
                        headers={"WWW-Authenticate": "Bearer"})

incorrect_email_or_password_exception=HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password ",
                            headers={"WWW-Authenticate": "Bearer"})


email_not_found_exception=HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Email not found",
                        headers={"WWW-Authenticate": "Bearer"})


user_not_found_exception=HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found",
                            headers={"WWW-Authenticate": "Bearer"})

invalid_code_exception= HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid code",
                        headers={"WWW-Authenticate": "Bearer"})

inactive_user_exception=HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Inactive user")

registred_email_exception=HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="The email is already registred")

