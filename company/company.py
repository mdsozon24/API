from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Company API", version="1.0.0")


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., min_length=2, max_length=100)
    salary: float = Field(..., gt=0)


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    industry: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    employees: List[Employee] = []


companies_db: List[Company] = [
    Company(
        id=1,
        name="TechNova",
        industry="Software",
        location="Dhaka",
        employees=[
            Employee(id=1, name="Asha", position="Engineer", salary=80000),
            Employee(id=2, name="Rahim", position="Manager", salary=120000),
        ],
    )
]


@app.get("/", tags=["Root"])
def home():
    return {"message": "Company API is running"}


@app.get("/companies", response_model=List[Company], tags=["Companies"])
def get_companies():
    return companies_db


@app.post("/companies", response_model=Company, status_code=status.HTTP_201_CREATED, tags=["Companies"])
def create_company(company: CompanyCreate):
    new_company = Company(id=len(companies_db) + 1, **company.model_dump(), employees=[])
    companies_db.append(new_company)
    return new_company


@app.get("/companies/{company_id}", response_model=Company, tags=["Companies"])
def get_company(company_id: int):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.put("/companies/{company_id}", response_model=Company, tags=["Companies"])
def update_company(company_id: int, company: CompanyCreate):
    comp = next((c for c in companies_db if c.id == company_id), None)
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    comp.name = company.name
    comp.industry = company.industry
    comp.location = company.location
    return comp


@app.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Companies"])
def delete_company(company_id: int):
    global companies_db
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    companies_db = [c for c in companies_db if c.id != company_id]
    return None


@app.get("/companies/{company_id}/employees", response_model=List[Employee], tags=["Employees"])
def get_employees(company_id: int):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company.employees


@app.post("/companies/{company_id}/employees", response_model=Employee, status_code=status.HTTP_201_CREATED, tags=["Employees"])
def create_employee(company_id: int, employee: EmployeeCreate):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    new_employee = Employee(id=len(company.employees) + 1, **employee.model_dump())
    company.employees.append(new_employee)
    return new_employee


@app.get("/companies/{company_id}/employees/{employee_id}", response_model=Employee, tags=["Employees"])
def get_employee(company_id: int, employee_id: int):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    employee = next((e for e in company.employees if e.id == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/companies/{company_id}/employees/{employee_id}", response_model=Employee, tags=["Employees"])
def update_employee(company_id: int, employee_id: int, employee: EmployeeCreate):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    existing = next((e for e in company.employees if e.id == employee_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")
    existing.name = employee.name
    existing.position = employee.position
    existing.salary = employee.salary
    return existing


@app.delete("/companies/{company_id}/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Employees"])
def delete_employee(company_id: int, employee_id: int):
    company = next((c for c in companies_db if c.id == company_id), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    employee = next((e for e in company.employees if e.id == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    company.employees = [e for e in company.employees if e.id != employee_id]
    return None
