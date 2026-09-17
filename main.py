from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import loan_prediction_router, auth_router
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loan_prediction_router.router)
app.include_router(auth_router.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Loan Prediction API",
            "status": 200,
            "description": "This API predicts loan status based on various features."}


