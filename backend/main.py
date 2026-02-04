import math
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import CompanyModel, ExpenseModel, AggregatedDataModel
from backend.schemas import CompanyList, CompanySchema, ExpenseSchema, AggregatedDataSchema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/api/operadoras", response_model=CompanyList)
def get_companies(
    page: int = 1, 
    size: int = 10, 
    search: str | None = None, 
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size

    query = select(CompanyModel)

    if search:
        query = query.where(
            or_(
                CompanyModel.cnpj.ilike(f"%{search}%"),
                CompanyModel.company_name.ilike(f"%{search}%")
            )
        )

    count_query = select(func.count(CompanyModel.ans_id))
    if search:
         count_query = count_query.where(
            or_(
                CompanyModel.cnpj.ilike(f"%{search}%"),
                CompanyModel.company_name.ilike(f"%{search}%")
            )
        )
    
    total_records = db.scalar(count_query)

    query = query.offset(skip).limit(size)
    companies = db.execute(query).scalars().all()

    total_pages = math.ceil(total_records / size) if total_records > 0 else 0
    
    return {
        "data" : companies,
        "meta" : {
            "page": page,
            "size": size,
            "total_records": total_records,
            "total_pages": total_pages
        }
    }

@app.get("/api/operadoras/{cnpj}", response_model=CompanySchema)
def get_company_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    statement = select(CompanyModel).where(CompanyModel.cnpj == cnpj)

    company = db.execute(statement).scalar_one_or_none()

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company

@app.get("/api/operadoras/{cnpj}/despesas", response_model=List[ExpenseSchema])
def get_company_expenses(cnpj: str, db: Session = Depends(get_db)):
    statement = (
        select(ExpenseModel)
        .join(CompanyModel)
        .where(CompanyModel.cnpj == cnpj)
    )

    expenses = db.execute(statement).scalars().all()

    if not expenses:
        raise HTTPException(status_code=404, detail="Expenses not found or invalid CNPJ")

    return expenses

@app.get("/api/estatisticas", response_model=List[AggregatedDataSchema])
def get_statistics(db: Session = Depends(get_db)):
    stats = db.execute(select(AggregatedDataModel)).scalars().all()
    return stats




    