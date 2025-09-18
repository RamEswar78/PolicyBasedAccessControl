# # from pydantic import BaseModel
# # from typing import Optional, Any
# # from datetime import date


# # # ---------------------- Leave ----------------------
# # class LeaveBase(BaseModel):
# #     employee_id: int
# #     status: str  # "pending", "approved", "draft"


# # class LeaveCreate(LeaveBase):
# #     pass


# # class LeaveUpdate(BaseModel):
# #     status: str


# # class LeaveResponse(LeaveBase):
# #     id: int

# #     class Config:
# #         from_attributes = True  # Pydantic v2


# # # ---------------------- Employee ----------------------
# # class EmployeeBase(BaseModel):
# #     name: str
# #     role: str  # "admin", "manager", "employee"
# #     department_id: int
# #     manager_id: Optional[int] = None


# # class EmployeeCreate(EmployeeBase):
# #     pass


# # class EmployeeUpdate(BaseModel):
# #     name: Optional[str] = None
# #     role: Optional[str] = None
# #     department_id: Optional[int] = None
# #     manager_id: Optional[int] = None


# # class EmployeeResponse(EmployeeBase):
# #     id: int

# #     class Config:
# #         from_attributes = True

# from pydantic import BaseModel
# from typing import Optional


# class EmployeeBase(BaseModel):
#     name: str
#     grade: Optional[str]
#     contractual_grade: Optional[str]
#     department: Optional[str]
#     project: Optional[str]


# class EmployeeResponse(EmployeeBase):
#     id: int

#     class Config:
#         orm_mode = True


# # ---------------------- Policy ----------------------
# class PolicyBase(BaseModel):
#     module: str
#     action: str
#     role: str
#     condition: Any
#     is_active: Optional[bool] = True


# class PolicyCreate(PolicyBase):
#     pass


# class PolicyUpdate(BaseModel):
#     module: Optional[str] = None
#     action: Optional[str] = None
#     role: Optional[str] = None
#     condition: Optional[Any] = None
#     is_active: Optional[bool] = None


# class PolicyResponse(PolicyBase):
#     id: int

#     class Config:
#         from_attributes = True
# app2/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from typing import Any


# ---------------------- Leave Schemas ----------------------


class LeaveBase(BaseModel):
    employee_id: int
    status: Optional[str] = "pending"  # default pending
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class LeaveResponse(LeaveBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------- Employee Schemas ----------------------


class EmployeeBase(BaseModel):
    name: str
    grade: Optional[str] = None  # Full-time grade e.g., C2
    contractual_grade: Optional[str] = None  # Contractual grade e.g., CON1
    department: Optional[str] = None  # e.g., Life Science, AI
    project: Optional[str] = None  # e.g., J&J, RBS


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------- Policy Schemas ----------------------


# ---------------------- Policy Schemas ----------------------


class PolicyBase(BaseModel):
    module: str  # e.g., leave, employee
    action: str  # e.g., view, create, update, delete
    role: str  # role name e.g., manager, employee
    grade:str

    # Access restriction fields
    dept_access: Optional[str] = None  # Department restriction
    contractual_grade: Optional[str] = None  # Contractual grade restriction
    project_access: Optional[str] = None  # Project restriction

    condition: Optional[Any] = None  # JSON/dict conditions
    is_active: Optional[bool] = True


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    module: Optional[str] = None
    action: Optional[str] = None
    role: Optional[str] = None
    dept_access: Optional[str] = None
    contractual_grade: Optional[str] = None
    project_access: Optional[str] = None
    condition: Optional[Any] = None
    is_active: Optional[bool] = None


class PolicyResponse(PolicyBase):
    id: int

    class Config:
        orm_mode = True
