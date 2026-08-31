"""Fail-closed consistency check across labelled observed-rainfall periods."""

from dataclasses import dataclass

from modules.external_intelligence.public_rainfall_record import PublicRainfallRecordPreview


@dataclass(frozen=True)
class RainfallPeriodConsistencyPreview:
    first_period: str
    second_period: str
    shared_area_count: int
    identical_record_count: int
    decision: str
    reason_codes: tuple[str, ...]
    usable_as_independent_corroboration: bool


class RainfallPeriodConsistencyService:
    def compare(self, first, second):
        if not isinstance(first, PublicRainfallRecordPreview) or not isinstance(second, PublicRainfallRecordPreview):
            raise ValueError("period comparison requires PublicRainfallRecordPreview inputs")
        if first.period_label == second.period_label:
            raise ValueError("period labels must differ")
        left = {item.area: (item.departure_percent, item.actual_mm, item.normal_mm) for item in first.records}
        right = {item.area: (item.departure_percent, item.actual_mm, item.normal_mm) for item in second.records}
        shared = sorted(set(left).intersection(right))
        identical = sum(left[area] == right[area] for area in shared)
        collision = bool(shared) and identical == len(shared)
        reasons = ("PERIOD_VIEW_DATA_COLLISION",) if collision else ()
        return RainfallPeriodConsistencyPreview(
            first.period_label, second.period_label, len(shared), identical,
            "BLOCK" if collision else "PASS", reasons, not collision,
        )


__all__ = ["RainfallPeriodConsistencyPreview", "RainfallPeriodConsistencyService"]
