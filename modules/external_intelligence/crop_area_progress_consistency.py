"""Fail-closed temporal consistency checks for cumulative crop-area reports."""

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview


@dataclass(frozen=True)
class CropAreaProgressChange:
    crop: str
    earlier_current_area: float
    later_current_area: float
    earlier_prior_year_gap: float
    later_prior_year_gap: float
    gap_change: float


@dataclass(frozen=True)
class CropAreaProgressPreview:
    earlier_period: str
    later_period: str
    shared_crop_count: int
    changes: tuple[CropAreaProgressChange, ...]
    decision: str
    reason_codes: tuple[str, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


class CropAreaProgressConsistencyService:
    FORMATS = ("%Y-%m-%d", "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y")

    def compare(self, earlier, later):
        if not isinstance(earlier, PublicCropAreaPreview) or not isinstance(later, PublicCropAreaPreview):
            raise ValueError("crop progress comparison requires PublicCropAreaPreview inputs")
        if self._date(later.period_label) <= self._date(earlier.period_label):
            raise ValueError("later crop-area period must follow earlier period")
        left, right = self._unique(earlier), self._unique(later)
        shared = sorted(set(left).intersection(right))
        if not shared:
            raise ValueError("crop-area reports contain no shared crops")
        reasons, changes = [], []
        for crop in shared:
            first, second = left[crop], right[crop]
            if second.current_area + 0.02 < first.current_area:
                reasons.append(f"CUMULATIVE_AREA_DECLINE:{crop}")
            if abs(second.normal_area - first.normal_area) > 0.02:
                reasons.append(f"NORMAL_AREA_DEFINITION_CHANGED:{crop}")
            changes.append(CropAreaProgressChange(
                crop, first.current_area, second.current_area,
                first.difference_from_prior_year, second.difference_from_prior_year,
                round(second.difference_from_prior_year - first.difference_from_prior_year, 2),
            ))
        return CropAreaProgressPreview(
            earlier.period_label, later.period_label, len(shared), tuple(changes),
            "BLOCK" if reasons else "PASS", tuple(reasons),
        )

    @staticmethod
    def _unique(preview):
        result = {}
        for record in preview.records:
            if record.crop in result: raise ValueError(f"duplicate crop record: {record.crop}")
            result[record.crop] = record
        return result

    @classmethod
    def _date(cls, value):
        for date_format in cls.FORMATS:
            try: return datetime.strptime(value, date_format).date()
            except ValueError: pass
        raise ValueError("unsupported crop-area period format")


__all__ = ["CropAreaProgressChange", "CropAreaProgressPreview", "CropAreaProgressConsistencyService"]
