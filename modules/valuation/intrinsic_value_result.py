from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass(slots=True)
class IntrinsicValueResult:
    """
    Institutional intrinsic value result.

    This office combines multiple valuation methodologies
    into a single investment-ready intrinsic value estimate.

    No calculations occur here.
    This object only carries results.
    """

    intrinsic_value: Optional[float] = None

    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

    confidence: float = 0.0

    methodology: str = "Weighted Composite"

    assumptions: Dict[str, Any] = field(default_factory=dict)

    supporting_values: Dict[str, float] = field(default_factory=dict)

    notes: list[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)