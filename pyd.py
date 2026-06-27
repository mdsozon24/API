from pydantic import BaseModel, Field
from fastapi import FastAPI
app = FastAPI()
class LoanApp(BaseModel):
    age: int
    income: float
    loan_amount: float
@app.post("/predict")
def predict_loan(loan_data: LoanApp):
    if loan_data.age < 18:
        return {"prediction": "Rejected", "reason": "Applicant is underage."}
    elif loan_data.income < 20000:
        return {"prediction": "Rejected", "reason": "Income is too low."}
    elif loan_data.loan_amount > (loan_data.income * 5):
        return {"prediction": "Rejected", "reason": "Loan amount exceeds allowable limit."}
    else:
        return {"prediction": "Approved", "reason": "Loan application meets the criteria."}