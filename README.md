# PolicyBasedAccessControl

A demo project implementing **Policy-Based Access Control (PBAC)** using **FastAPI** and **SQLAlchemy**.  
It provides endpoints to manage **Leaves**, **Employees**, and **Policies**, while enforcing access rules dynamically through policies stored in the database.

---

## 🚀 Setup Instructions

### Step 1: Install dependencies
```bash
pip install -r requirements.txt

python -m app2.seed

uvicorn app2.main:app --reload

http://localhost:8000/docs
```

Testing Policies

Try accessing the GET /employees or GET /leaves routes.

Based on the policies stored in the database, the results will change depending on the logged-in user's:

employee_id

roles

department_id


```
app2/
 ├── db.py               # Database connection & session
 ├── models.py           # SQLAlchemy models (Employee, Leave, Policy)
 ├── policy_evaluator.py # Core PBAC evaluator
 ├── policy_service.py   # Service layer to apply policies
 ├── main.py             # FastAPI entry point (routes & API setup)
 ├── seed.py             # Seed script to populate initial data
