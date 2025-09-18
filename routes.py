from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app2 import services, schemas, db
from app2 import models

router = APIRouter()


# Dependency
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


# -------- User Routes --------
@router.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db, user)


@router.get("/users/", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db)):
    return services.get_users(db)


@router.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=schemas.UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = services.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------- Employee Routes --------
@router.post("/employees/", response_model=schemas.EmployeeRead)
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return services.create_employee(db, emp)


@router.get("/employees/", response_model=list[schemas.EmployeeRead])
def read_employees(db: Session = Depends(get_db)):
    return services.get_employees(db)


@router.get("/employees/{emp_id}", response_model=schemas.EmployeeRead)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = services.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/employees/{emp_id}", response_model=schemas.EmployeeRead)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = services.delete_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# -------- Record Routes --------
@router.post("/records/", response_model=schemas.RecordRead)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    return services.create_record(db, record)


@router.get("/records/", response_model=list[schemas.RecordRead])
def read_records(db: Session = Depends(get_db)):
    return services.get_records(db)


@router.get("/records/{record_id}", response_model=schemas.RecordRead)
def read_record(record_id: int, db: Session = Depends(get_db)):
    record = services.get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.delete("/records/{record_id}", response_model=schemas.RecordRead)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record = services.delete_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


# -------- Records by User ID --------
@router.get("/records/by-user/{user_id}", response_model=list[schemas.RecordRead])
def get_records_by_user(user_id: int, db: Session = Depends(get_db)):
    records = db.query(services.models.Record).all()
    if not records:
        raise HTTPException(
            status_code=404, detail=f"No records found for user ID {user_id}"
        )
    return records


@router.get("/records-all/me")
def my_records(
    user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)
):
    employee = (
        db.query(models.Employee).filter(models.Employee.user_id == user_id).first()
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return services.get_records_for_employee(db, employee)


@router.get("/employees-all/me")
def my_employees(
    user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)
):
    employee = (
        db.query(models.Employee).filter(models.Employee.user_id == user_id).first()
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return services.get_employees_for_employee(db, employee)
