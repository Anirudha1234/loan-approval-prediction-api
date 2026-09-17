from pydantic import BaseModel, Field

class LoanFeatures(BaseModel):
    # Loan_ID: str = Field(description="Loan ID of the customer")
    Gender: str = Field(description="Gender of the customer")
    Married: str = Field(description="Married or not")
    Dependents: str = Field(description="Dependents of the customer")
    Education: str = Field(description="Education of the customer")
    Self_Employed: str = Field(description="Self Employed or not")
    ApplicantIncome: float = Field(description="Applicant Income of the customer")
    CoapplicantIncome: float = Field(description="Coapplicant Income of the customer")
    LoanAmount: float = Field(description="Loan Amount of the customer")
    Loan_Amount_Term: int = Field(description="Loan Amount Term of the customer")
    Credit_History: float = Field(description="Credit History of the customer")
    Property_Area: str = Field(description="Property Area of the customer")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Gender": "Male",
                "Married": "Yes",
                "Dependents": "1",
                "Education": "Graduate",
                "Self_Employed": "No",
                "ApplicantIncome": 4583,
                "CoapplicantIncome": 1508.0,
                "LoanAmount": 128.0,
                "Loan_Amount_Term": 360.0,
                "Credit_History": 1.0,
                "Property_Area": "Rural"
            }
        }
    }

    

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)