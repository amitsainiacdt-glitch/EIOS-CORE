"""Build a deterministic, non-decisioning coverage map from the causal registry."""
from collections import defaultdict
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry

def build_sector_catalyst_coverage(registry=None):
    registry=registry or SectorCausalIndicatorRegistry.initial_library(); groups=defaultdict(list)
    for item in registry.all():
        for sector in item.sector_ids:
            groups[sector].append({'indicatorId':item.indicator_id,'name':item.name,'eventTypes':list(item.applicable_event_types),
                'economicVariable':item.economic_variable,'expectedDirection':item.expected_direction.value,
                'leadTimeQuarters':[item.lead_time_quarters_min,item.lead_time_quarters_max],
                'earningsChannels':list(item.earnings_channels),'companyArchetypes':list(item.company_archetypes),
                'preferredPrimarySourceTypes':list(item.preferred_primary_source_types),
                'corroboratingSourceTypes':list(item.corroborating_source_types),
                'minimumIndependentGroups':item.minimum_independence_groups,
                'minimumPersistentObservations':item.minimum_persistent_observations,
                'expectedPersistenceDays':item.expected_persistence_days,
                'falsePositiveConditions':list(item.known_false_positive_conditions),
                'contradictionTests':list(item.contradiction_tests),'killTests':list(item.kill_tests),
                'requiredUpstreamIndicators':list(item.required_upstream_indicator_ids)})
    sectors=[{'sectorId':sector,'indicatorCount':len(items),'indicators':sorted(items,key=lambda x:x['indicatorId'])}
             for sector,items in sorted(groups.items())]
    return {'schemaVersion':1,'registryVersion':'2026-09-08','sectorCount':len(sectors),
            'indicatorCount':len(registry.all()),'sectors':sectors,'createsCatalyst':False,
            'changesVerdict':False,'authorizesTrade':False}

__all__=['build_sector_catalyst_coverage']
