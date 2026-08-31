from dataclasses import replace

from modules.external_intelligence.crop_area_progress_consistency import CropAreaProgressConsistencyService
from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview, PublicCropAreaRecord


def _record(crop, current, gap, normal=100.0):
    return PublicCropAreaRecord(crop, crop, "unused", "LAKH_HECTARE", normal, current, current-gap, gap, crop, "A", "a" * 64, "https://example.test")


def test_progress_comparison_quantifies_gap_recovery():
    earlier = PublicCropAreaPreview("A", "E", "17.07.2026", (_record("Rice", 166.41, -1.41),))
    later = PublicCropAreaPreview("B", "F", "2026-08-21", (_record("Rice", 405.10, -13.19),))
    result = CropAreaProgressConsistencyService().compare(earlier, later)
    assert result.decision == "PASS" and result.shared_crop_count == 1
    assert result.changes[0].gap_change == -11.78
    assert not result.creates_observation


def test_cumulative_area_decline_blocks_timeline():
    earlier = PublicCropAreaPreview("A", "E", "07.08.2026", (_record("Rice", 400, -5),))
    later = PublicCropAreaPreview("B", "F", "14.08.2026", (_record("Rice", 399, -4),))
    result = CropAreaProgressConsistencyService().compare(earlier, later)
    assert result.decision == "BLOCK"
    assert result.reason_codes == ("CUMULATIVE_AREA_DECLINE:Rice",)


def test_changed_normal_definition_is_not_silently_compared():
    earlier = PublicCropAreaPreview("A", "E", "07.08.2026", (_record("Rice", 300, -5),))
    later_record = replace(_record("Rice", 350, -4), normal_area=110)
    later = PublicCropAreaPreview("B", "F", "14.08.2026", (later_record,))
    assert CropAreaProgressConsistencyService().compare(earlier, later).decision == "BLOCK"
