# policy_service.py
from sqlalchemy.orm import Session, Query
from app2.policy_evaluator import PolicyEvaluator
from sqlalchemy import text
from rich import print
from typing import Optional


def get_policies(
    db: Session,
    role: str,
    module: str,
    action: str,
    grade: Optional[str] = None,
    contractual_grade: Optional[str] = None,
    dept_access: Optional[str] = None,
    project_access: Optional[str] = None,
):
    stmt = text("""
        SELECT condition
        FROM policies
        WHERE role = :role
          AND module = :module
          AND action = :action
          AND grade = :grade
          AND is_active = TRUE
        
AND (
    (:contractual_grade IS NULL AND contractual_grade IS NULL)
    OR (:contractual_grade IS NOT NULL AND contractual_grade = :contractual_grade)
)
AND (
    (:dept_access IS NULL AND dept_access IS NULL)
    OR (:dept_access IS NOT NULL AND dept_access = :dept_access)
)
AND (
    (:project_access IS NULL AND project_access IS NULL)
    OR (:project_access IS NOT NULL AND project_access = :project_access)
)
    """)
    rows = db.execute(
        stmt,
        {
            "role": role,
            "module": module,
            "action": action,
            "grade": grade,
            "contractual_grade": contractual_grade,
            "dept_access": dept_access,
            "project_access": project_access,
        },
    ).fetchall()
    return [row[0] for row in rows]


def enforce_policies(
    db: Session, principal: dict, query: Query, model_cls, module: str, action: str
):
    evaluator = PolicyEvaluator(principal)
    applied_any = False

    for role in principal.get("roles", []):
        policies = get_policies(
            db,
            role,
            module,
            action,
            principal["grade"],
            principal["contractual_grade"],
            principal["department"],
            principal["project"],
        )
        print(policies)

        for condition in policies:
            applied_any = True
            query = evaluator.apply_policy(query, condition, model_cls)

    if not applied_any:
        # deny all by default
        query = query.filter(False)

    return query
