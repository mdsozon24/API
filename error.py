from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

students ={
    101 : {"name": "Alice", "roll": 101, "standard": 10, "score": 85.5},
    102 : {"name": "Bob", "roll": 102, "standard": 10, "score": 92.0},
    103 : {"name": "Charlie", "roll": 103, "standard": 10, "score": 78.0},
    104 : {"name": "David", "roll": 104, "standard": 10, "score": 88.5}
}

class mark(BaseModel):
    name: str
    roll: int
    standard: int
    score: float

@app.post("/submit")
def submit_mark(mark_data: mark):
    if mark_data.score < 0 or mark_data.score > 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100.")
    if mark_data.roll < 0:
        raise HTTPException(status_code=400, detail="Roll number must be a positive integer.")
    if mark_data.roll in students:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists.")
    if mark_data.standard < 1 or mark_data.standard > 12: #for a school student, standard must be between 1 and 12
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 12.")
    return {"message": "Mark submitted successfully.", "data": mark_data}

@app.get("/get/{roll}")
def get_mark(roll: int):
    if roll not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students[roll]