import pandas as pd
import joblib
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import io
import models
from datetime import datetime, timezone
from auth import get_password_hash, verify_password, create_access_token


model = joblib.load("loan_prediction_model.joblib")
feature_names = model.feature_names_in_
users = []
current_user = None


# def get_current_user():
#     print("get_current_user",current_user)
#     for user in users:
#         if user["username"] == current_user:
#             return {"username": current_user,"status": 200}
#     raise HTTPException(status_code=401, detail="Not authenticated")

def register_user(user,db):
    try:
        # users.append(user.model_dump())
        # print(users)
        if db.query(models.User).filter(models.User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = get_password_hash(user.password)
        new_user = models.User(username=user.username, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully", "status": 200}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User registration failed: {str(e)}")

def login_user(user,db):
    try:
        # for u in users:
        #         if u["username"] == user.username and u["password"] == user.password:
        #             global current_user  
        #             current_user = user.username
        #             print(current_user)
        #             return {"username": user.username,"message": "Login successful", "status": 200}       

        form_user = db.query(models.User).filter(models.User.username == user.username).first()

        if not form_user or not verify_password(user.password, form_user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = create_access_token(data={"sub": form_user.username})
        return {"access_token": access_token, "token_type": "bearer", "status": 200}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
            
        

def predict_loan(data,db,current_user):
    try:
        features = pd.DataFrame(data.model_dump(), index=[0])
        prediction = model.predict(features)[0]
        Loan_Status = 'Yes' if prediction == 'Y' else 'No'
        # print(data.model_dump())
        # print(features)
        probablity = model.predict_proba(features)[0][1]
        print("current_user",current_user.user_id)

        predict_save = models.Prediction_history(user_id=current_user.user_id, ApplicantIncome=data.ApplicantIncome, LoanAmount=data.LoanAmount, Credit_History=data.Credit_History, loan_status=Loan_Status, approval_probability=f"{probablity:.2%}", created_at= datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        db.add(predict_save)
        db.commit()
        db.refresh(predict_save)
        return {"user_id": current_user.user_id,"prediction": Loan_Status, "approval_probability": f"{probablity:.2%}", "status": 200}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"prediction failed: {str(e)}")


async def predict_loan_file(file):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        predictions = model.predict(df)
        df["Loan_Status"] = predictions
        probablity = model.predict_proba(df)[:, 1]
        df["approval_probability"] = [f"{x:.2%}" for x in probablity]
        output = df.to_csv(index=False)

        return StreamingResponse(io.StringIO(output), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=predictions.csv"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}") 


def predict_past_history(db,current_user):
    try:
        predictions = db.query(models.Prediction_history).filter(models.Prediction_history.user_id == current_user.user_id).all()
        print(predictions)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"prediction failed: {str(e)}")