from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# import services.loan_prediction_service as loan_service
from datetime import datetime, timedelta, timezone
import models
from database import get_db
import os
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    # try:
    #    print("current_user",loan_service.current_user)
    #    user = db.query(models.User).filter(models.User.username == loan_service.current_user).first()
    #    if user is None:
    #        raise HTTPException(status_code=401, detail="Could not validate credentials")
    #    return user
    # except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"User authentication failed: {str(e)}")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.username == username).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user



