import os
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

URI = '/api/v1'

# -------------------------------------------------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod    
    def hash_password(password: str):
        return pwd_context.hash(password)
# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
# OAuth2 para manejar la autenticacion con JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URI}/token")

class JWT_Authentication():
    # Configuracion de secret key para JWT
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_Authentication.SECRET_KEY, algorithm=JWT_Authentication.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, JWT_Authentication.SECRET_KEY, algorithms=[JWT_Authentication.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
# -------------------------------------------------------------------------------------------------------------------