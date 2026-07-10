# Enterprise HRMS + Payroll + Face Recognition + AI Analytics

## Overview
A professional-level Human Resource Management System with integrated Payroll, Face Recognition for attendance, and AI-driven Analytics.

## Features
- Employee Management (CRUD)
- Payroll Processing
- Face Recognition Attendance System
- AI Analytics (Employee Performance Prediction, Attrition Risk, etc.)
- User Authentication (JWT)
- Dashboard with visualizations

## Tech Stack
- Backend: FastAPI
- Database: SQLite (can switch to PostgreSQL)
- Frontend: Streamlit (simple UI) + basic HTML/JS if needed
- Face Rec: face_recognition + OpenCV
- AI: scikit-learn

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations if using Alembic (setup later)
5. Run the application (see below)

## Running the Project
- Backend: `uvicorn backend.main:app --reload`
- Frontend/Streamlit: `streamlit run frontend/app.py`
- Face Rec demo: `python utils/face_attendance.py`

For full integration, run backend and Streamlit separately.

## Structure
- backend/: FastAPI app
- frontend/: Streamlit UI
- database/: DB models and connection
- models/: Pydantic and SQLAlchemy models
- utils/: Utilities like face rec, payroll calc, AI models

Note: This is a complete but simplified professional demo. For production, add more security, scaling, etc.