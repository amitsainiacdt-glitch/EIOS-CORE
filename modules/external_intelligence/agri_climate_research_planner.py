"""Expand research targets and fail closed on missing coverage before Meta."""

from modules.external_intelligence.agri_climate_company_exposure_registry import AgriClimateCompanyExposureRegistry
from modules.external_intelligence.agri_climate_research_plan import AgriClimateResearchCoveragePreview, AgriClimateResearchPlan, AgriClimateResearchTarget
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


class AgriClimateResearchPlanner:
    NON_AUTHORITY = "Research coverage only; not a causal conclusion, Evidence item, Signal, Opportunity, recommendation, or trade authority."
    ROOTS = {
        AgriClimateResearchTarget.FERTILIZER_EARNINGS: ("RAINFALL_FERTILIZER_RESPONSE_CURVE", "CROP_SWITCH_AND_INPUT_MIX", "FOOD_POLICY_INTERVENTION_SUPPRESSOR", "FERTILIZER_GLOBAL_INPUT_STRESS"),
        AgriClimateResearchTarget.FOOD_COMPANY_EARNINGS: ("SATELLITE_CROP_HEALTH_DIVERGENCE", "CROP_SWITCH_AND_INPUT_MIX", "FOOD_POLICY_INTERVENTION_SUPPRESSOR", "AGRI_SUPPLY_CHAIN_AMPLIFICATION", "RABI_WATER_CARRYOVER"),
        AgriClimateResearchTarget.FOOD_STOCK_AND_PRICE: ("SATELLITE_CROP_HEALTH_DIVERGENCE", "CROP_SWITCH_AND_INPUT_MIX", "FOOD_POLICY_INTERVENTION_SUPPRESSOR", "AGRI_SUPPLY_CHAIN_AMPLIFICATION", "RABI_WATER_CARRYOVER"),
        AgriClimateResearchTarget.RURAL_DEMAND_AND_CREDIT: ("RAINFALL_RURAL_DEMAND_TRANSMISSION", "IRRIGATION_DROUGHT_SHIELD", "FOOD_POLICY_INTERVENTION_SUPPRESSOR"),
    }
    SOURCE_REQUIREMENTS = {
        "AGRICULTURAL_DROUGHT_COMPOSITE": ("IMD", "NRSC", "AGRI_MINISTRY"),
        "CROP_STAGE_WATER_STRESS": ("IMD", "AGRI_MINISTRY"),
        "IRRIGATION_DROUGHT_SHIELD": ("CWC", "CGWB", "NRSC"),
        "RABI_WATER_CARRYOVER": ("CWC", "IMD", "AGRI_MINISTRY"),
        "FERTILIZER_APPLICATION_TIMING": ("FERTILIZERS_DEPARTMENT", "AGRI_MINISTRY"),
        "NUTRIENT_MIX_SUBSTITUTION": ("FERTILIZERS_DEPARTMENT",),
        "RAINFALL_FERTILIZER_RESPONSE_CURVE": ("FERTILIZERS_DEPARTMENT", "IMD"),
        "CROP_SWITCH_AND_INPUT_MIX": ("AGRI_MINISTRY", "ISRO"),
        "SATELLITE_CROP_HEALTH_DIVERGENCE": ("NRSC", "ISRO"),
        "FOOD_POLICY_INTERVENTION_SUPPRESSOR": ("FOOD_DISTRIBUTION_DEPARTMENT", "DGFT"),
        "AGRI_SUPPLY_CHAIN_AMPLIFICATION": ("AGMARKNET",),
        "RAINFALL_RURAL_DEMAND_TRANSMISSION": ("RBI", "AGRI_MINISTRY"),
        "FERTILIZER_GLOBAL_INPUT_STRESS": ("FERTILIZERS_DEPARTMENT", "DGFT"),
    }

    def __init__(self, indicator_registry, exposure_registry):
        if not isinstance(indicator_registry, SectorCausalIndicatorRegistry): raise ValueError("indicator_registry must be SectorCausalIndicatorRegistry")
        if not isinstance(exposure_registry, AgriClimateCompanyExposureRegistry): raise ValueError("exposure_registry must be AgriClimateCompanyExposureRegistry")
        self.indicators, self.exposures = indicator_registry, exposure_registry

    def plan(self, *, plan_id, target, entity, season, crop_ids, geography_ids):
        target = target if isinstance(target, AgriClimateResearchTarget) else AgriClimateResearchTarget(target)
        roots = self.ROOTS[target]
        required = self._closure(roots)
        sources = tuple(sorted({source for indicator_id in required for source in self.SOURCE_REQUIREMENTS[indicator_id]}))
        return AgriClimateResearchPlan(1, self._text(plan_id), target, self._text(entity), self._text(season), self._texts(crop_ids), self._texts(geography_ids), required, sources, target != AgriClimateResearchTarget.FOOD_STOCK_AND_PRICE)

    def coverage(self, plan, *, covered_indicator_ids, covered_source_ids):
        if not isinstance(plan, AgriClimateResearchPlan): raise ValueError("plan must be AgriClimateResearchPlan")
        covered_indicators, covered_sources = self._texts(covered_indicator_ids), self._texts(covered_source_ids)
        unknown = set(covered_indicators) - {item.indicator_id for item in self.indicators.all()}
        if unknown: raise ValueError("covered indicators contain unknown identities")
        missing_indicators = tuple(sorted(set(plan.required_indicator_ids) - set(covered_indicators)))
        missing_sources = tuple(sorted(set(plan.required_source_ids) - set(covered_sources)))
        exposures = self.exposures.for_entity(plan.entity) if plan.company_exposure_required else ()
        reasons = []
        if missing_indicators: reasons.append("AGRI_CLIMATE_INDICATOR_COVERAGE_INCOMPLETE")
        if missing_sources: reasons.append("AGRI_CLIMATE_SOURCE_COVERAGE_INCOMPLETE")
        if plan.company_exposure_required and not exposures: reasons.append("AGRI_CLIMATE_COMPANY_EXPOSURE_MISSING")
        return AgriClimateResearchCoveragePreview(plan.plan_id, not reasons, tuple(sorted(set(covered_indicators) & set(plan.required_indicator_ids))), missing_indicators, tuple(sorted(set(covered_sources) & set(plan.required_source_ids))), missing_sources, tuple(item.exposure_id for item in exposures), tuple(reasons), self.NON_AUTHORITY)

    def _closure(self, roots):
        result = set()
        def add(indicator_id):
            if indicator_id in result: return
            definition = self.indicators.get(indicator_id); result.add(indicator_id)
            for dependency in definition.required_upstream_indicator_ids: add(dependency)
        for root in roots: add(root)
        return tuple(sorted(result))

    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values):
        if not isinstance(values, (tuple, list)): raise ValueError("values must be a list")
        result = tuple(cls._text(item) for item in values)
        if len(set(result)) != len(result): raise ValueError("values must be unique")
        return result


__all__ = ["AgriClimateResearchPlanner"]
