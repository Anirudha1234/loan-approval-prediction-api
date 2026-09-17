from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Prediction_history(Base):
    __tablename__ = "prediction_history"
    Loan_ID = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,  ForeignKey("users.user_id") ,nullable=False)
    ApplicantIncome = Column(Float, nullable=False)
    LoanAmount = Column(Float, nullable=False)
    Credit_History = Column(Float, nullable=False)
    loan_status = Column(String, nullable=False)
    approval_probability = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)



