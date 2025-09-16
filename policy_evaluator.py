# policy_evaluator.py
import logging
from typing import Any, Dict, Optional, Union
from sqlalchemy import and_, or_
from sqlalchemy.orm import InstrumentedAttribute, Query

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PolicyEvaluator:
    """Safely evaluate JSON-based PBAC policies into SQLAlchemy filters."""

    OP_SQL = {
        "==": lambda col, val: col == val,
        "!=": lambda col, val: col != val,
        ">": lambda col, val: col > val,
        "<": lambda col, val: col < val,
        ">=": lambda col, val: col >= val,
        "<=": lambda col, val: col <= val,
        "in": lambda col, val: col.in_(
            val if isinstance(val, (list, tuple)) else [val]
        ),
        "not_in": lambda col, val: ~col.in_(
            val if isinstance(val, (list, tuple)) else [val]
        ),
        "like": lambda col, val: col.like(val),
        "exists": lambda col, val: col != None
        if val
        else col == None,  # handle exists operator
    }

    def __init__(self, principal: Dict[str, Any]):
        self.principal = principal or {}

    def _resolve_rhs(self, rhs: Any) -> Any:
        """Replace principal.* references with values from principal dict."""
        if isinstance(rhs, str) and rhs.startswith("principal."):
            _, key = rhs.split(".", 1)
            return self.principal.get(key)
        return rhs

    def _resolve_column(self, model_cls, lhs: str) -> Optional[InstrumentedAttribute]:
        """Resolve 'resource.something' into SQLAlchemy column."""
        if lhs == "always_allow":
            return "always_allow"  # special case
        if not lhs.startswith("resource."):
            logger.error(f"Invalid LHS (must start with resource.): {lhs}")
            return None

        path = lhs.split(".")[1:]
        col = model_cls
        try:
            for attr in path:
                if isinstance(col, InstrumentedAttribute):
                    col = getattr(col.property.mapper.class_, attr)
                else:
                    col = getattr(col, attr)
        except AttributeError:
            logger.error(f"Invalid resource path: {lhs}")
            return None
        return col

    def _clause_to_filter(self, clause: Dict[str, Any], model_cls) -> Optional[Any]:
        lhs = clause.get("lhs")
        op = clause.get("op")
        rhs = clause.get("rhs")

        if lhs == "always_allow":
            return True

        col = self._resolve_column(model_cls, lhs)
        if col is None:
            return None

        rhs_val = self._resolve_rhs(rhs)

        # Skip clause if principal value is missing
        if rhs_val is None and lhs.startswith("resource.contractual_grade"):
            return None

        # Handle exists operator
        if op == "exists":
            return col != None if rhs_val else col == None

        if op not in self.OP_SQL:
            logger.error(f"Unsupported operator: {op}")
            return None

        try:
            return self.OP_SQL[op](col, rhs_val)
        except Exception as e:
            logger.error(f"Error building filter for {clause}: {e}")
            return None

    def condition_to_filter(self, condition: Union[Dict[str, Any], str], model_cls):
        if not condition:
            return None

        import json

        if isinstance(condition, str):
            try:
                condition = json.loads(condition)
            except Exception as e:
                logger.error(f"Failed to parse condition JSON: {e}")
                return None

        # Handle always_allow
        if condition.get("type") == "always_allow":
            return True

        cond_type = condition.get("type", "and").lower()
        clauses = condition.get("clauses", [])

        filters = []
        for clause in clauses:
            if "clauses" in clause:
                f = self.condition_to_filter(clause, model_cls)
            else:
                f = self._clause_to_filter(clause, model_cls)
            if f is not None:
                filters.append(f)

        if not filters:
            return None

        return and_(*filters) if cond_type == "and" else or_(*filters)

    def apply_policy(
        self, query: Query, condition: Union[Dict[str, Any], str], model_cls
    ) -> Query:
        filter_expr = self.condition_to_filter(condition, model_cls)
        if filter_expr is True:
            return query  # always_allow
        if filter_expr is not None:
            return query.filter(filter_expr)
        return query.filter(False)  # deny by default
