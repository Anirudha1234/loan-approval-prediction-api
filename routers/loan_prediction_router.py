from fastapi import APIRouter, UploadFile, File, Depends
from services.loan_prediction_service import predict_loan, predict_loan_file, predict_past_history
from schemas import LoanFeatures
from auth import get_current_user
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/predict")
def predict(data: LoanFeatures, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return predict_loan(data,db,current_user)

@router.post("/predict-file")
async def predict_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    return await predict_loan_file(file)

@router.get("/prediction-history")
def predict_history(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return predict_past_history(db,current_user)