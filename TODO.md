# HRMS Project - TODO

## Plan summary (Attendance marks error)
- Fix backend import/implementation issues causing Attendance/mark API to fail. ✅
- Fix `database/db.py` missing `create_engine` import. ✅
- Fix `backend/main.py` missing FastAPI imports (FastAPI, Depends, HTTPException, status). ✅
- Add robust `/attendance/mark/` behavior (404 if employee not found). ✅
- Make backend importable even if JWT/passlib libs are missing (prevents UI crashing). ✅
- Verified backend now imports and `/attendance/mark/` works after creating employee via `/employees/`. ✅


