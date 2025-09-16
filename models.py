from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app2.db import Base


# class Employee(Base):
#     __tablename__ = "employees"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     role = Column(String)  # "admin", "manager", "employee"
#     department_id = Column(Integer)
#     manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

#     manager = relationship("Employee", remote_side=[id], backref="team")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    grade = Column(String, nullable=True)  # Full-time grade, e.g., C1, C2
    contractual_grade = Column(String, nullable=True)  # Contractual grade, e.g., CON1
    department = Column(String, nullable=True)  # e.g., Life Science, AI
    project = Column(String, nullable=True)  # e.g., J&J, RBS


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(String)  # "pending", "approved", "draft"

    employee = relationship("Employee", backref="leaves")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String)
    action = Column(String)
    role = Column(String)
    dept_access = Column(String)
    contractual_grade = Column(String)
    project_access = Column(String)
    condition = Column(JSON)
    is_active = Column(Boolean, default=True)
