from sqlalchemy.orm import Session
from app2 import models, schemas

from app2.oso import oso


# -------- User Services --------
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


# -------- Employee Services --------
def create_employee(db: Session, emp: schemas.EmployeeCreate):
    db_emp = models.Employee(**emp.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()


def get_employees(db: Session):
    return db.query(models.Employee).all()


def delete_employee(db: Session, emp_id: int):
    emp = get_employee(db, emp_id)
    if emp:
        db.delete(emp)
        db.commit()
    return emp


# -------- Record Services --------
def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_record(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def get_records(db: Session):
    return db.query(models.Record).all()


def delete_record(db: Session, record_id: int):
    record = get_record(db, record_id)
    if record:
        db.delete(record)
        db.commit()
    return record


def get_records_for_employee(db: Session, employee: models.Employee):
    # Instead of filtering manually, let Oso rewrite query
    query = oso.authorized_query(employee, "read", models.Record)
    return db.execute(query).scalars().all()


def get_employees_for_employee(db: Session, employee: models.Employee):
    query = oso.authorized_query(employee, "read", models.Employee)
    return db.execute(query).scalars().all()
