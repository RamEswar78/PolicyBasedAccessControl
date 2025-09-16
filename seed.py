# seed.py
from app2.db import Base, engine, SessionLocal
from app2.models import Employee, Leave, Policy


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    employees = [
        Employee(
            name="Alice",
            grade="C2",
            contractual_grade=None,
            department=None,
            project=None,
        ),
        Employee(
            name="Bob",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project=None,
        ),
        Employee(
            name="Carol",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project="J&J",
        ),
        Employee(
            name="Dave",
            grade=None,
            contractual_grade=None,
            department=None,
            project=None,
        ),
        Employee(
            name="Eve",
            grade="C2",
            contractual_grade="CON1",
            department=None,
            project=None,
        ),
        Employee(
            name="Frank",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project="RBS",
        ),
        Employee(
            name="Grace",
            grade="C2",
            contractual_grade=None,
            department="AI",
            project="J&J",
        ),
        Employee(
            name="Heidi",
            grade="C2",
            contractual_grade=None,
            department="AI",
            project="RBS",
        ),
        Employee(
            name="Ivan",
            grade="C1",
            contractual_grade="CON1",
            department=None,
            project=None,
        ),
        Employee(
            name="Judy",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project="J&J",
        ),
        Employee(
            name="Mallory",
            grade=None,
            contractual_grade=None,
            department=None,
            project=None,
        ),
        Employee(
            name="Niaj",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project="RBS",
        ),
        Employee(
            name="Olivia",
            grade=None,
            contractual_grade=None,
            department=None,
            project=None,
        ),
        Employee(
            name="Peggy",
            grade="C2",
            contractual_grade="CON1",
            department=None,
            project=None,
        ),
        Employee(
            name="Sybil",
            grade="C1",
            contractual_grade="CON1",
            department="AI",
            project=None,
        ),
        Employee(
            name="Trent",
            grade="C2",
            contractual_grade=None,
            department="Life Science",
            project="J&J",
        ),
        Employee(
            name="Victor",
            grade=None,
            contractual_grade=None,
            department=None,
            project=None,
        ),
        Employee(
            name="Walter",
            grade="C2",
            contractual_grade=None,
            department="AI",
            project="RBS",
        ),
        Employee(
            name="Yvonne",
            grade="C2",
            contractual_grade="CON1",
            department="Life Science",
            project="RBS",
        ),
        Employee(
            name="Zara",
            grade="C1",
            contractual_grade="CON1",
            department="AI",
            project="J&J",
        ),
        Employee(
            name="Sureman",
            grade="C1",
            contractual_grade="CON1",
            department="Life Science",
            project=None,
        ),
    ]

    db.add_all(employees)
    db.commit()

    # Updated policies compatible with PolicyEvaluator
    policies = [
        # Scenario 1: Full-time C2, or contractual_grade exists
        Policy(
            module="employee",
            action="view",
            role="employee",
            dept_access=None,
            contractual_grade=None,
            project_access=None,
            condition={
                "type": "or",
                "clauses": [
                    {"lhs": "resource.grade", "op": "<=", "rhs": "principal.grade"},
                    {"lhs": "resource.contractual_grade", "op": "exists", "rhs": True},
                ],
            },
            is_active=True,
        ),
        # Scenario 2: Dept restriction (Life Science)
        Policy(
            module="employee",
            action="view",
            role="employee",
            condition={
                "type": "or",
                "clauses": [
                    {
                        "type": "and",
                        "clauses": [
                            {
                                "lhs": "resource.grade",
                                "op": "<=",
                                "rhs": "principal.grade",
                            },
                            {
                                "lhs": "resource.department",
                                "op": "in",
                                "rhs": ["Life Science"],
                            },
                        ],
                    },
                    {
                        "type": "and",
                        "clauses": [
                            {
                                "lhs": "resource.contractual_grade",
                                "op": "exists",
                                "rhs": True,
                            },
                            {
                                "lhs": "resource.department",
                                "op": "in",
                                "rhs": ["Life Science"],
                            },
                        ],
                    },
                ],
            },
            is_active=True,
        ),
        # Scenario 3: Dept + Project restriction (Life Science + J&J)
        Policy(
            module="employee",
            action="view",
            role="employee",
            dept_access="Life Science",
            contractual_grade=None,
            project_access="J&J",
            condition={
                "type": "and",
                "clauses": [
                    {"lhs": "resource.grade", "op": "<=", "rhs": "principal.grade"},
                    {"lhs": "resource.department", "op": "in", "rhs": ["Life Science"]},
                    {"lhs": "resource.project", "op": "in", "rhs": ["J&J"]},
                ],
            },
            is_active=True,
        ),
        # Scenario 4: Always allow (no restrictions)
        Policy(
            module="employee",
            action="view",
            role="employee",
            dept_access=None,
            contractual_grade=None,
            project_access=None,
            condition={"type": "always_allow"},
            is_active=True,
        ),
        # Scenario 5: Full-time + Contractual grade restriction (C2 + CON1)
        Policy(
            module="employee",
            action="view",
            role="employee",
            dept_access=None,
            contractual_grade="CON1",
            project_access=None,
            condition={
                "type": "or",
                "clauses": [
                    {"lhs": "resource.grade", "op": "<=", "rhs": "principal.grade"},
                    {
                        "lhs": "resource.contractual_grade",
                        "op": "<=",
                        "rhs": "principal.contractual_grade",
                    },
                ],
            },
            is_active=True,
        ),
        # Scenario 6: Dept OR, Project OR (Life Science/AI + J&J/RBS)
        Policy(
            module="employee",
            action="view",
            role="employee",
            dept_access="Life Science,AI",  # multiple departments
            contractual_grade=None,
            project_access="J&J,RBS",  # multiple projects
            condition={
                "type": "and",
                "clauses": [
                    {"lhs": "resource.grade", "op": "<=", "rhs": "principal.grade"},
                    {
                        "lhs": "resource.department",
                        "op": "in",
                        "rhs": ["Life Science", "AI"],
                    },
                    {"lhs": "resource.project", "op": "in", "rhs": ["J&J", "RBS"]},
                ],
            },
            is_active=True,
        ),
    ]

    db.add_all(policies)
    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully ✅")
