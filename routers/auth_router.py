from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.loan_prediction_service import register_user, login_user
from schemas import UserCreate
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user,db)

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    return login_user(user,db)