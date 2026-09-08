"""Strict company-to-sector/archetype routing for causal catalyst research."""
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry

@dataclass(frozen=True)
class CompanyCatalystProfile:
    ticker:str; entity:str; sector_ids:tuple[str,...]; company_archetypes:tuple[str,...]
    source_ids:tuple[str,...]; as_of:str; exposure_status:str; uncertainty:str

class CompanyCatalystProfileRegistry:
    STATUSES={'PUBLIC_EVIDENCE_PARTIAL','GOVERNED_EXPOSURE_READY','REGISTERED_UNVERIFIED'}
    def __init__(self,profiles=()):
        self._items={}
        for profile in profiles:self.register(profile)
    def register(self,profile):
        if not isinstance(profile,CompanyCatalystProfile):raise ValueError('profile must be CompanyCatalystProfile')
        ticker=self._text(profile.ticker,'ticker').upper()
        if ticker in self._items:raise ValueError('duplicate company catalyst ticker')
        sectors=self._texts(profile.sector_ids,'sector_ids'); archetypes=self._texts(profile.company_archetypes,'company_archetypes'); sources=self._texts(profile.source_ids,'source_ids')
        if not sectors or not archetypes or not sources:raise ValueError('company catalyst profile requires sector, archetype and source routing')
        date.fromisoformat(profile.as_of)
        if profile.exposure_status not in self.STATUSES:raise ValueError('invalid exposure status')
        normalized=CompanyCatalystProfile(ticker,self._text(profile.entity,'entity'),sectors,archetypes,sources,profile.as_of,profile.exposure_status,self._text(profile.uncertainty,'uncertainty'))
        self._items[ticker]=normalized;return normalized
    def get(self,ticker):
        item=self._items.get(self._text(ticker,'ticker').upper())
        if item is None:raise ValueError('company catalyst profile is not registered')
        return item
    def all(self):return tuple(self._items[key] for key in sorted(self._items))
    @classmethod
    def load(cls,path):
        raw=json.loads(Path(path).read_text(encoding='utf-8'))
        if raw.get('schema_version')!=1 or not isinstance(raw.get('profiles'),list):raise ValueError('unsupported company catalyst profile schema')
        fields=CompanyCatalystProfile.__dataclass_fields__
        profiles=[]
        for item in raw['profiles']:
            if set(item)!=set(fields):raise ValueError('company catalyst profile fields are incomplete or unknown')
            profiles.append(CompanyCatalystProfile(**{**item,'sector_ids':tuple(item['sector_ids']),'company_archetypes':tuple(item['company_archetypes']),'source_ids':tuple(item['source_ids'])}))
        registry=cls(profiles); registry.collector_readiness=raw.get('collector_readiness',{})
        unknown=set(registry.collector_readiness)-{p.ticker for p in registry.all()}
        if unknown:raise ValueError('collector readiness references an unknown company')
        return registry
    @staticmethod
    def _text(value,name):
        if not isinstance(value,str) or not value.strip():raise ValueError(f'{name} must not be empty')
        return value.strip()
    @classmethod
    def _texts(cls,values,name):
        if not isinstance(values,(list,tuple)):raise ValueError(f'{name} must be a list')
        result=tuple(cls._text(x,name) for x in values)
        if len(result)!=len(set(result)):raise ValueError(f'{name} must be unique')
        return result

def build_company_catalyst_onboarding(profile_registry,sector_registry=None):
    sector_registry=sector_registry or SectorCausalIndicatorRegistry.initial_library(); companies=[]
    all_indicators=sector_registry.all()
    for profile in profile_registry.all():
        selected=[]
        for indicator in all_indicators:
            sectors=sorted(set(profile.sector_ids)&set(indicator.sector_ids)); archetypes=sorted(set(profile.company_archetypes)&set(indicator.company_archetypes))
            if not sectors or not archetypes:continue
            readiness=getattr(profile_registry,'collector_readiness',{}).get(profile.ticker,{}).get(indicator.indicator_id,'NOT_CONNECTED')
            selected.append({'indicatorId':indicator.indicator_id,'name':indicator.name,'matchedSectors':sectors,'matchedArchetypes':archetypes,
                'collectorReadiness':readiness,'preferredPrimarySourceTypes':list(indicator.preferred_primary_source_types),
                'minimumIndependentGroups':indicator.minimum_independence_groups,'minimumPersistentObservations':indicator.minimum_persistent_observations})
        connected=sum(item['collectorReadiness']!='NOT_CONNECTED' for item in selected)
        companies.append({'ticker':profile.ticker,'entity':profile.entity,'exposureStatus':profile.exposure_status,'uncertainty':profile.uncertainty,
            'sourceIds':list(profile.source_ids),'selectedIndicatorCount':len(selected),'connectedIndicatorCount':connected,'indicators':selected,
            'activeCoverageClaim':profile.exposure_status=='GOVERNED_EXPOSURE_READY' and connected==len(selected)})
    return {'schemaVersion':1,'companyCount':len(companies),'companies':companies,'createsCatalyst':False,'changesVerdict':False,'authorizesTrade':False}

__all__=['CompanyCatalystProfile','CompanyCatalystProfileRegistry','build_company_catalyst_onboarding']
