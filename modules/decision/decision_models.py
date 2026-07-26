from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class Recommendation(Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    WATCH = "Watch"
    SELL = "Sell"
    REJECT = "Reject"


class ConvictionLevel(Enum):
    VERY_HIGH = "Very High"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    VERY_LOW = "Very Low"


class PriorityLevel(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"


@dataclass(slots=True)
class PositionSize:
    target_weight: float = 0.0
    max_weight: float = 0.0
    initial_weight: float = 0.0
    cash_required: float = 0.0


@dataclass(slots=True)
class DecisionReason:
    title: str
    description: str
    impact: str = "Neutral"


@dataclass(slots=True)
class DecisionResult:
    recommendation: Recommendation
    conviction: ConvictionLevel
    priority: PriorityLevel

    margin_of_safety: float = 0.0
    expected_return_3y: float = 0.0
    expected_return_5y: float = 0.0
    expected_return_10y: float = 0.0

    position_size: Optional[PositionSize] = None

    confidence: float = 0.0

    reasons: List[DecisionReason] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    required_actions: List[str] = field(default_factory=list)

    summary: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)