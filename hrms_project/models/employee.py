from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import date

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    position = Column(String)
    salary = Column(Float)
    join_date = Column(Date, default=date.today)
    face_encoding = Column(String)  # Stored as JSON string of encoding
    is_active = Column(Boolean, default=True)
    
    attendances = relationship("Attendance", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, default=date.today)
    status = Column(String)  # 'present', 'absent', etc.
    time_in = Column(String)
    time_out = Column(String)
    
    employee = relationship("Employee", back_populates="attendances")

class Payroll(Base):
    __tablename__ = "payrolls"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month = Column(String)
    base_salary = Column(Float)
    deductions = Column(Float, default=0.0)
    bonuses = Column(Float, default=0.0)
    net_salary = Column(Float)
    
    employee = relationship("Employee", back_populates="payrolls")