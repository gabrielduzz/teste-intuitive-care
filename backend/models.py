from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class CompanyModel(Base):
    __tablename__ = "dim_companies"

    ans_id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String, index=True)
    company_name = Column(String)
    modality = Column(String)
    state = Column(String)
    expenses = relationship("ExpenseModel", back_populates="company")


class ExpenseModel(Base):
    __tablename__ = "fact_expenses"

    ans_id = Column(Integer, ForeignKey("dim_companies.ans_id"), primary_key=True, index=True)
    reference_date = Column(Date, primary_key=True)
    quarter = Column(Integer)
    amount = Column(DECIMAL, index=True)
    year = Column(Integer)
    company = relationship("CompanyModel", back_populates="expenses")

class AggregatedDataModel(Base):
    __tablename__ = "aggregated_data" 

    company_name = Column(String, primary_key=True)
    state = Column(String, primary_key=True)
    
    total_amount = Column(DECIMAL)
    avg_amount = Column(DECIMAL)
    stddev_amount = Column(DECIMAL, nullable=True)