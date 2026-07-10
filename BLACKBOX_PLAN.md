## Information gathered
- backend/main.py is the FastAPI server, but it imports several symbols that are not imported (FastAPI, Depends, HTTPException, status, create_engine is missing in db.py).
- database/db.py uses `create_engine(...)` but never imports it, causing `NameError: create_engine is not defined`.
- models/employee.py defines SQLAlchemy models for Employee, Attendance, Payroll.
- frontend/app.py calls backend endpoints:
  - POST http://localhost:8000/attendance/mark/?employee_id={emp_id}

## Plan
1) Fix database layer (database/db.py)
   - Add `from sqlalchemy import create_engine`.
   - Ensure Base/engine/session are correctly created.
2) Fix backend imports and runtime errors (backend/main.py)
   - Add missing imports: `from fastapi import FastAPI, Depends, HTTPException` and `from fastapi import status`.
   - Ensure JWT config doesn’t crash when env vars are missing (provide safe defaults).
3) Fix attendance marking endpoint for robustness
   - Validate `employee_id` exists; return 404 if not.
   - Save attendance with current date and time.
4) Run backend and verify attendance endpoint works using curl/requests.

## Dependent files to edit
- hrms_project/database/db.py
- hrms_project/backend/main.py

## Followup steps
- Start backend: `uvicorn backend.main:app --reload`
- Open Streamlit UI and try Attendance -> Mark Attendance.

<ask_followup_question>
Proceed to apply these code fixes (db.py + main.py) to remove the runtime error and make /attendance/mark work?
</ask_followup_question>

