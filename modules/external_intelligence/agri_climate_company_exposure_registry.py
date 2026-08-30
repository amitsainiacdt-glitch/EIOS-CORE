"""Validated registry for company-specific agriculture-climate exposure."""

from datetime import datetime

from modules.external_intelligence.agri_climate_company_exposure import AgriClimateCompanyExposure, IrrigationDependency


class AgriClimateCompanyExposureRegistry:
    def __init__(self, exposures=()):
        self._items = {}
        for exposure in exposures: self.register(exposure)

    def register(self, exposure):
        if not isinstance(exposure, AgriClimateCompanyExposure): raise ValueError("exposure must be AgriClimateCompanyExposure")
        if exposure.schema_version != 1: raise ValueError("unsupported exposure schema")
        exposure_id = self._text(exposure.exposure_id, "exposure_id")
        if exposure_id in self._items: raise ValueError("exposure_id already registered")
        if not exposure.public_information_only: raise ValueError("company exposure must use public information only")
        crops = self._texts(exposure.crop_ids, "crop_ids"); states = self._texts(exposure.state_ids, "state_ids")
        districts = self._texts(exposure.district_ids, "district_ids"); products = self._texts(exposure.product_ids, "product_ids")
        customers = self._texts(exposure.customer_types, "customer_types"); sources = self._texts(exposure.public_source_ids, "public_source_ids")
        if not sources: raise ValueError("public_source_ids must not be empty")
        if not any((crops, states, districts, products, customers)): raise ValueError("at least one operating exposure dimension is required")
        percentage = exposure.disclosed_revenue_exposure_pct
        if percentage is not None and (isinstance(percentage, bool) or not isinstance(percentage, (int, float)) or not 0 <= percentage <= 100): raise ValueError("disclosed revenue exposure must be between 0 and 100")
        irrigation = exposure.irrigation_dependency if isinstance(exposure.irrigation_dependency, IrrigationDependency) else IrrigationDependency(exposure.irrigation_dependency)
        if not isinstance(exposure.as_of, datetime): raise ValueError("as_of must be a datetime")
        normalized = AgriClimateCompanyExposure(
            1, exposure_id, self._text(exposure.entity, "entity"), self._text(exposure.company_archetype, "company_archetype"),
            crops, states, districts, products, customers, irrigation, None if percentage is None else float(percentage),
            sources, exposure.as_of, True, self._text(exposure.uncertainty_statement, "uncertainty_statement"),
        )
        self._items[exposure_id] = normalized
        return normalized

    def for_entity(self, entity):
        entity = self._text(entity, "entity").casefold()
        return tuple(item for item in self.all() if item.entity.casefold() == entity)

    def all(self): return tuple(self._items[key] for key in sorted(self._items))

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (tuple, list)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(item, name) for item in values)
        if len(set(result)) != len(result): raise ValueError(f"{name} must be unique")
        return result


__all__ = ["AgriClimateCompanyExposureRegistry"]
