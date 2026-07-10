import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.db import get_db, Base, engine
from models.employee import Employee, Attendance, Payroll

import models.employee  # Ensure tables created
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
# NOTE: This project should NOT crash if JWT/passlib aren't installed.
# The UI works without auth, so we gracefully degrade.
try:
    from jose import jwt  # type: ignore
except Exception:  # pragma: no cover
    jwt = None

try:
    import jwt as pyjwt  # type: ignore
except Exception:  # pragma: no cover
    pyjwt = None

try:
    from passlib.context import CryptContext  # type: ignore
except Exception:  # pragma: no cover
    CryptContext = None


from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Enterprise HRMS")

Base.metadata.create_all(bind=engine)

# Auth setup
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


if CryptContext is not None:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
else:
    pwd_context = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # json-serializable exp
    to_encode.update({"exp": expire})

    if jwt is not None:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if pyjwt is not None:
        return pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Fallback (will break auth, but avoids import crash)
    raise RuntimeError("JWT library not installed. Install python-jose or PyJWT.")


# Simple user for demo (in prod use DB users)
fake_users_db = {
    "admin": {
        "username": "admin",
        # If passlib isn't available, we won't use this field.
        "hashed_password": (pwd_context.hash("admin123") if pwd_context else "admin123"),
    }
}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)

    # If passlib isn't installed, allow demo login without password hashing
    if CryptContext is None:
        if not user or form_data.password != "admin123":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Employee Endpoints
@app.post("/employees/")
async def create_employee(employee: dict, db: Session = Depends(get_db)):
    # In full impl, use Pydantic model
    emp = Employee(**employee)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@app.get("/employees/", response_model=List[dict])
async def read_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [ { "id": e.id, "name": e.name, "email": e.email, "department": e.department } for e in employees ]

# Attendance with Face Rec placeholder
@app.post("/attendance/mark/")
async def mark_attendance(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    att = Attendance(
        employee_id=employee_id,
        status="present",
        time_in=datetime.now().strftime("%H:%M"),
        time_out=None,
    )
    db.add(att)
    db.commit()
    db.refresh(att)
    return {"status": "marked", "attendance_id": att.id}


# Payroll
@app.post("/payroll/process/")
async def process_payroll(month: str, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    for emp in employees:
        net = emp.salary * 0.9  # Simple calc
        payroll = Payroll(employee_id=emp.id, month=month, base_salary=emp.salary, net_salary=net)
        db.add(payroll)
    db.commit()
    return {"status": "processed"}

# AI Analytics endpoint placeholder
@app.get("/analytics/attrition/")
async def attrition_risk():
    # Placeholder AI
    return {"high_risk_employees": 5, "prediction_accuracy": 85.0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)