from database.db import SessionLocal, engine
from models.employee import Employee, Base
from datetime import date
import json

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Sample employees
employees = [
    {"name": "John Doe", "email": "john@example.com", "department": "IT", "position": "Developer", "salary": 75000, "face_encoding": json.dumps([0.1]*128)},
    {"name": "Jane Smith", "email": "jane@example.com", "department": "HR", "position": "Manager", "salary": 95000, "face_encoding": json.dumps([0.2]*128)},
]

for emp_data in employees:
    emp = Employee(**emp_data, join_date=date(2023,1,1))
    db.add(emp)

db.commit()
print("Sample data seeded.")