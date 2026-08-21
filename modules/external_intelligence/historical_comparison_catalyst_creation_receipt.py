"""Immutable receipt for one explicitly materialized governed Catalyst."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class HistoricalComparisonCatalystCreationReceipt:
 schema_version:int
 preview_fingerprint:str
 assessment_fingerprint:str
 promotion_fingerprint:str
 support_fingerprint:str
 catalyst_id:str
 catalyst_fingerprint:str
 signal_ids:tuple[str,...]
 promoted_signal_ids:tuple[str,...]
 primary_catalyst_id:str
 primary_family:str
 catalyst_score:float
 confidence:float
 creator:str
 rationale:str
 created_at:datetime

__all__=["HistoricalComparisonCatalystCreationReceipt"]
