from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Optional


class ValidationLevel(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    TODO_CONTRACT = "TODO-CONTRACT"
    CONTRACT_ADDITIVE_REQUIRED = "CONTRACT-ADDITIVE-REQUIRED"


@dataclass
class ValidationResult:
    level: ValidationLevel
    rule_id: str
    title: str
    description: str
    evidence: Optional[Any] = None
    impact: Optional[str] = None
    recommendation: Optional[str] = None
    proposed_contract_additive: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["level"] = self.level.value
        return data
