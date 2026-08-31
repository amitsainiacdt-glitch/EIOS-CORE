"""Offline checks for cross-period rainfall data collisions."""

from dataclasses import replace

from modules.external_intelligence.public_rainfall_record import PublicRainfallRecord, PublicRainfallRecordPreview
from modules.external_intelligence.rainfall_period_consistency import RainfallPeriodConsistencyService


def main():
    record = PublicRainfallRecord("R1", "COUNTRY : INDIA", "Daily", -26, 5.2, 7.1, "passage", 1, 2, "A1", "a" * 64, "https://imd.example")
    daily = PublicRainfallRecordPreview("A1", "E1", "Daily", (record,))
    weekly_collision = PublicRainfallRecordPreview("A2", "E2", "Weekly", (replace(record, record_id="R2", period_label="Weekly", acquisition_id="A2"),))
    blocked = RainfallPeriodConsistencyService().compare(daily, weekly_collision)
    assert blocked.decision == "BLOCK" and blocked.reason_codes == ("PERIOD_VIEW_DATA_COLLISION",)
    assert not blocked.usable_as_independent_corroboration
    weekly_changed = PublicRainfallRecordPreview("A3", "E3", "Weekly", (replace(record, record_id="R3", period_label="Weekly", actual_mm=20.0, acquisition_id="A3"),))
    passed = RainfallPeriodConsistencyService().compare(daily, weekly_changed)
    assert passed.decision == "PASS" and passed.usable_as_independent_corroboration
    print("RAINFALL PERIOD CONSISTENCY: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
