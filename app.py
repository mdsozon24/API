from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class loanApp(BaseModel):
    age : int
    income : float
    loan_amount : float
@app.post("/predict")
def predict_loan(loan_data: loanApp):
    if loan_data.age < 18:
        return {"prediction": "Rejected", "reason": "Applicant is underage."}
    elif loan_data.income < 20000:
        return {"prediction": "Rejected", "reason": "Income is too low."}
    elif loan_data.loan_amount > (loan_data.income * 5):
        return {"prediction": "Rejected", "reason": "Loan amount exceeds allowable limit."}
    else:
        return {"prediction": "Approved", "reason": "Loan application meets the criteria."}