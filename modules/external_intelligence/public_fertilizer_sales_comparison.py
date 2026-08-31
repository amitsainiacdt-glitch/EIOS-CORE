"""Comparable-period aggregate fertilizer consumption from a public release."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFertilizerSalesComparison:
    comparison_id: str
    current_period_label: str
    prior_period_label: str
    current_consumption_lmt: float
    prior_consumption_lmt: float
    year_over_year_percent: float
    source_passage: str
    passage_start: int
    passage_end: int
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicFertilizerSalesComparisonPreview:
    acquisition_id: str
    extraction_id: str
    comparison: PublicFertilizerSalesComparison
    creates_observation: bool = False
    requires_human_review: bool = True


__all__=["PublicFertilizerSalesComparison","PublicFertilizerSalesComparisonPreview"]
