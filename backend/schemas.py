from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date

class CompanySchema(BaseModel):
    ans_id: int
    cnpj: str
    company_name: Optional[str] = None
    modality: Optional[str] = None
    state: Optional[str] = None

    class Config:
        from_attributes = True

class ExpenseSchema(BaseModel):
    ans_id: int
    amount: Decimal
    year: int
    quarter: int
    reference_date: date

    class Config:
        from_attributes=True

class AggregatedDataSchema(BaseModel):
    company_name: str
    state: str
    total_amount: Decimal
    avg_amount: Decimal
    stddev_amount: Optional[Decimal] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    page: int
    size: int
    total_records: int
    total_pages: int

class CompanyList(BaseModel):
    data: List[CompanySchema]
    meta: PaginationMeta

