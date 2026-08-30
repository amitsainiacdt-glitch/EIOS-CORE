"""Validated registry for passive sector causal-indicator definitions."""

from modules.external_intelligence.sector_causal_indicator import CausalEffectDirection, SectorCausalIndicatorDefinition
from modules.external_intelligence.agri_climate_indicator_library import agri_climate_indicators


class SectorCausalIndicatorRegistry:
    def __init__(self, definitions=()):
        self._definitions = {}
        for definition in definitions: self.register(definition)

    def register(self, definition):
        if not isinstance(definition, SectorCausalIndicatorDefinition): raise ValueError("definition must be SectorCausalIndicatorDefinition")
        if definition.schema_version != 1: raise ValueError("unsupported causal-indicator schema")
        indicator_id = self._text(definition.indicator_id, "indicator_id")
        if indicator_id in self._definitions: raise ValueError("indicator_id already registered")
        if isinstance(definition.version, bool) or not isinstance(definition.version, int) or definition.version <= 0: raise ValueError("version must be positive")
        sectors = self._texts(definition.sector_ids, "sector_ids")
        events = self._texts(definition.applicable_event_types, "applicable_event_types")
        if not sectors or not events: raise ValueError("sector and event applicability must not be empty")
        minimum, maximum = definition.lead_time_quarters_min, definition.lead_time_quarters_max
        if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in (minimum, maximum)) or minimum > maximum: raise ValueError("lead-time range is invalid")
        for value, name in ((definition.minimum_independence_groups, "minimum_independence_groups"), (definition.minimum_persistent_observations, "minimum_persistent_observations"), (definition.expected_persistence_days, "expected_persistence_days")):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0: raise ValueError(f"{name} must be positive")
        direction = definition.expected_direction if isinstance(definition.expected_direction, CausalEffectDirection) else CausalEffectDirection(definition.expected_direction)
        normalized = SectorCausalIndicatorDefinition(
            1, indicator_id, definition.version, self._text(definition.name, "name"), sectors, events,
            self._text(definition.economic_variable, "economic_variable"), direction, minimum, maximum,
            self._text(definition.causal_mechanism, "causal_mechanism"), self._required_texts(definition.earnings_channels, "earnings_channels"),
            self._required_texts(definition.company_archetypes, "company_archetypes"),
            self._required_texts(definition.preferred_primary_source_types, "preferred_primary_source_types"),
            self._texts(definition.corroborating_source_types, "corroborating_source_types"),
            self._text(definition.independence_group_template, "independence_group_template"),
            definition.minimum_independence_groups, definition.minimum_persistent_observations,
            definition.expected_persistence_days, self._required_texts(definition.known_false_positive_conditions, "known_false_positive_conditions"),
            self._required_texts(definition.contradiction_tests, "contradiction_tests"), self._required_texts(definition.kill_tests, "kill_tests"), bool(definition.enabled),
            self._texts(definition.required_upstream_indicator_ids, "required_upstream_indicator_ids"),
        )
        self._definitions[indicator_id] = normalized
        return normalized

    def get(self, indicator_id):
        value = self._definitions.get(self._text(indicator_id, "indicator_id"))
        if value is None or not value.enabled: raise ValueError("causal indicator is not registered and enabled")
        return value

    def all(self): return tuple(self._definitions[key] for key in sorted(self._definitions) if self._definitions[key].enabled)

    def validate_dependencies(self):
        enabled = {item.indicator_id: item for item in self.all()}
        for item in enabled.values():
            missing = set(item.required_upstream_indicator_ids) - set(enabled)
            if missing: raise ValueError(f"causal indicator {item.indicator_id} has unknown upstream dependencies")
            if item.indicator_id in item.required_upstream_indicator_ids: raise ValueError("causal indicator cannot depend on itself")
        visiting, visited = set(), set()
        def visit(indicator_id):
            if indicator_id in visiting: raise ValueError("causal indicator dependencies contain a cycle")
            if indicator_id in visited: return
            visiting.add(indicator_id)
            for dependency in enabled[indicator_id].required_upstream_indicator_ids: visit(dependency)
            visiting.remove(indicator_id); visited.add(indicator_id)
        for indicator_id in enabled: visit(indicator_id)
        return True

    def missing_dependencies(self, indicator_ids):
        supplied = set(self._texts(tuple(indicator_ids), "indicator_ids"))
        missing = set()
        inspected = set()
        def inspect(current):
            if current in inspected: return
            inspected.add(current)
            for dependency in self.get(current).required_upstream_indicator_ids:
                if dependency not in supplied: missing.add(dependency)
                inspect(dependency)
        for current in supplied: inspect(current)
        return tuple(sorted(missing))

    def applicable(self, *, sector_id, event_type):
        sector_id, event_type = self._text(sector_id, "sector_id"), self._text(event_type, "event_type")
        return tuple(item for item in self.all() if sector_id in item.sector_ids and event_type in item.applicable_event_types)

    @classmethod
    def initial_library(cls):
        registry = cls((
            SectorCausalIndicatorDefinition(1, "INDUSTRIAL_ORDER_CONVERSION", 1, "Tender-to-order conversion", ("INDUSTRIALS",), ("TENDER", "ORDER_CONTRACT", "EXECUTION_UPDATE"), "Executable demand backlog", CausalEffectDirection.SUPPORTIVE, 1, 4, "Independent tender awards that convert into executable orders and subsequent execution may lead revenue recognition.", ("REVENUE", "OPERATING_LEVERAGE", "CASH_FLOW"), ("PROJECT_MANUFACTURER", "EPC_CONTRACTOR", "CAPITAL_GOODS_SUPPLIER"), ("EXCHANGE_FILING", "GOVERNMENT_TENDER_PORTAL"), ("CUSTOMER_DISCLOSURE", "EXECUTION_UPDATE"), "originating_authority_or_document", 2, 2, 180, ("Non-binding bid", "Framework order without committed quantity", "Repeated republication of one award"), ("Order cancellation", "Execution delay", "Customer funding unavailable"), ("Material cancellation", "Counterparty insolvency", "Company lacks execution capacity")),
            SectorCausalIndicatorDefinition(1, "LENDER_EARLY_CREDIT_STRESS", 1, "Early credit-stress migration", ("BANKING", "NBFC"), ("POLICY_REGULATION", "SUPPLIER_CUSTOMER"), "Borrower repayment stress before reported credit cost", CausalEffectDirection.ADVERSE, 1, 3, "Persistent early delinquency and collection deterioration may precede higher slippages and credit costs.", ("CREDIT_COST", "PROFIT", "CAPITAL"), ("RETAIL_LENDER", "SME_LENDER", "MICROFINANCE_LENDER"), ("REGULATORY_DATA", "COMPANY_FILING"), ("CREDIT_BUREAU", "COLLECTION_CHANNEL"), "dataset_origin_and_borrower_cohort", 2, 2, 90, ("Seasonal payment timing", "Temporary operational collection disruption"), ("Collections normalize", "Delinquency migration reverses"), ("Capital adequacy breach", "Liquidity access impairment")),
            SectorCausalIndicatorDefinition(1, "CHEMICAL_SPREAD_RECOVERY", 1, "Product spread recovery", ("CHEMICALS",), ("POLICY_REGULATION", "CAPACITY_CHANGE"), "Product realization less feedstock cost", CausalEffectDirection.CONTEXT_DEPENDENT, 1, 3, "A persistent product-feedstock spread improvement may lead gross-margin recovery if volumes and utilization hold.", ("GROSS_MARGIN", "EBITDA", "CASH_FLOW"), ("COMMODITY_CHEMICAL_PRODUCER", "SPECIALTY_CHEMICAL_PRODUCER"), ("CUSTOMS_DATA", "INDUSTRY_PRICE_DATA"), ("COMPETITOR_DISCLOSURE", "SUPPLIER_PRICING"), "underlying_price_dataset", 2, 3, 90, ("One-day price spike", "Currency-only movement", "Low-volume quoted price"), ("Feedstock cost catches up", "Utilization falls", "Inventory losses emerge"), ("Structural demand destruction", "Plant shutdown", "Loss of key customer")),
            SectorCausalIndicatorDefinition(1, "BUILDING_MATERIAL_UTILISATION", 1, "Utilisation and realization breadth", ("BUILDING_MATERIALS",), ("CAPACITY_CHANGE", "SUPPLIER_CUSTOMER"), "Regional volume, utilization, and realization", CausalEffectDirection.CONTEXT_DEPENDENT, 1, 4, "Broad utilization and realization improvement may lead operating leverage when new supply and input costs remain controlled.", ("VOLUME", "REALIZATION", "EBITDA_MARGIN"), ("CEMENT_PRODUCER", "CERAMICS_PRODUCER", "BUILDING_PRODUCTS_MANUFACTURER"), ("COMPANY_FILING", "GOVERNMENT_DISPATCH_DATA"), ("DEALER_CHANNEL", "COMPETITOR_DISCLOSURE"), "producer_or_dataset_origin", 2, 2, 120, ("Restocking without end demand", "Regional festival seasonality"), ("Price rollback", "Inventory rebuild", "New competing capacity"), ("Sustained demand contraction", "Input-cost shock", "Balance-sheet stress")),
            *agri_climate_indicators(),
        ))
        registry.validate_dependencies()
        return registry

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len(set(result)) != len(result): raise ValueError(f"{name} must be unique")
        return result
    @classmethod
    def _required_texts(cls, values, name):
        result = cls._texts(values, name)
        if not result: raise ValueError(f"{name} must not be empty")
        return result


__all__ = ["SectorCausalIndicatorRegistry"]
