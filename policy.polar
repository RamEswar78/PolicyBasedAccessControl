# Role-based access on records
allow(employee: Employee, "read", _record: Record) if
    employee.role = "manager";

allow(employee: Employee, "read", record: Record) if
    employee.role = "lead" and
    employee.dept = record.dept;

allow(employee: Employee, "read", record: Record) if
    employee.role != "manager" and
    employee.role != "lead" and
    employee.id = record.owner_id;

# Role-based access on employees
allow(employee: Employee, "read", _target: Employee) if
    employee.role = "manager";

allow(employee: Employee, "read", target: Employee) if
    employee.role = "lead" and
    employee.dept = target.dept;

allow(employee: Employee, "read", target: Employee) if
    employee.role != "manager" and
    employee.role != "lead" and
    employee.id = target.id;
