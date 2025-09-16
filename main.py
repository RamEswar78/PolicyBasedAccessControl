# app2/main.py

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app2.db import get_db
from app2.models import Leave, Employee, Policy
from app2.policy_service import enforce_policies
from app2.schemas import (
    LeaveResponse,
    LeaveCreate,
    LeaveUpdate,
    EmployeeResponse,
    EmployeeCreate,
    EmployeeUpdate,
    PolicyResponse,
    PolicyCreate,
    PolicyUpdate,
)

app = FastAPI(title="PBAC Demo")


# --- Dependency: Simulated Logged-in User (principal) ---
def get_current_user(
    employee_id: int = Query(...),
    roles: List[str] = Query(...),
    grade: Optional[str] = Query(None),
    contractual_grade: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    project: Optional[str] = Query(None),
):
    """
    Simulate principal. Example:
    /employees?employee_id=2&roles=manager&grade=C2&department=Life Science
    """
    return {
        "employee_id": employee_id,
        "roles": roles,
        "grade": grade,
        "contractual_grade": contractual_grade,
        "department": department,
        "project": project,
    }


# ---------------------- Leave Endpoints ----------------------


@app.get("/leaves", response_model=List[LeaveResponse])
def get_leaves(
    db: Session = Depends(get_db), principal: dict = Depends(get_current_user)
):
    query = db.query(Leave)
    query = enforce_policies(db, principal, query, Leave, module="leave", action="view")
    return query.all()


@app.post("/leaves", response_model=LeaveResponse)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Leave)
    query = enforce_policies(
        db, principal, query, Leave, module="leave", action="create"
    )
    allowed = query.all()
    if not allowed and "admin" not in principal.get("roles", []):
        raise HTTPException(status_code=403, detail="Not authorized")

    leave_obj = Leave(**leave.dict())
    db.add(leave_obj)
    db.commit()
    db.refresh(leave_obj)
    return leave_obj


@app.put("/leaves/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,  # ✅ path param: no Query()
    new_data: LeaveUpdate,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Leave).filter(Leave.id == leave_id)
    query = enforce_policies(
        db, principal, query, Leave, module="leave", action="update"
    )
    leave_obj = query.first()
    if not leave_obj:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this leave"
        )

    for k, v in new_data.dict().items():
        setattr(leave_obj, k, v)

    db.commit()
    db.refresh(leave_obj)
    return leave_obj


@app.delete("/leaves/{leave_id}")
def delete_leave(
    leave_id: int,  # ✅ path param: no Query()
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Leave).filter(Leave.id == leave_id)
    query = enforce_policies(
        db, principal, query, Leave, module="leave", action="delete"
    )
    leave_obj = query.first()
    if not leave_obj:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this leave"
        )

    db.delete(leave_obj)
    db.commit()
    return {"deleted": leave_id}


# ---------------------- Employee Endpoints ----------------------


@app.get("/employees", response_model=List[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db), principal: dict = Depends(get_current_user)
):
    print(principal)
    query = db.query(Employee)
    query = enforce_policies(
        db, principal, query, Employee, module="employee", action="view"
    )
    return query.all()


@app.post("/employees", response_model=EmployeeResponse)
def create_employee(
    emp: EmployeeCreate,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Employee)
    query = enforce_policies(
        db, principal, query, Employee, module="employee", action="create"
    )
    emp_obj = Employee(**emp.dict())
    db.add(emp_obj)
    db.commit()
    db.refresh(emp_obj)
    return emp_obj


@app.put("/employees", response_model=EmployeeResponse)
def update_employee(
    updates: EmployeeUpdate,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Employee).filter(Employee.id == principal["employee_id"])
    query = enforce_policies(
        db, principal, query, Employee, module="employee", action="update"
    )
    emp_obj = query.first()
    if not emp_obj:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this employee"
        )

    for k, v in updates.dict(exclude_unset=True).items():
        setattr(emp_obj, k, v)

    db.commit()
    db.refresh(emp_obj)
    return emp_obj


@app.delete("/employees")
def delete_employee(
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_user),
):
    query = db.query(Employee).filter(Employee.id == principal["employee_id"])
    query = enforce_policies(
        db, principal, query, Employee, module="employee", action="delete"
    )
    emp_obj = query.first()
    if not emp_obj:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this employee"
        )

    db.delete(emp_obj)
    db.commit()
    return {"deleted": principal["employee_id"]}


# ---------------------- Policy Endpoints ----------------------


@app.get("/policies", response_model=List[PolicyResponse])
def list_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()


@app.post("/policies", response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    policy_obj = Policy(**policy.dict())
    db.add(policy_obj)
    db.commit()
    db.refresh(policy_obj)
    return policy_obj


@app.put("/policies/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: int,  # ✅ path param: no Query()
    updates: PolicyUpdate,
    db: Session = Depends(get_db),
):
    policy_obj = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy_obj:
        raise HTTPException(status_code=404, detail="Policy not found")

    for k, v in updates.dict(exclude_unset=True).items():
        setattr(policy_obj, k, v)

    db.commit()
    db.refresh(policy_obj)
    return policy_obj


@app.delete("/policies/{policy_id}")
def delete_policy(
    policy_id: int,  # ✅ path param: no Query()
    db: Session = Depends(get_db),
):
    policy_obj = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy_obj:
        raise HTTPException(status_code=404, detail="Policy not found")

    db.delete(policy_obj)
    db.commit()
    return {"deleted": policy_id}
