"""Semantic schema-drift gate for structured public-source extraction."""

from dataclasses import dataclass
import hashlib,json


@dataclass(frozen=True)
class PublicSourceSchemaContract:
    contract_id: str
    source_id: str
    dataset_id: str
    required_fields: tuple[str,...]
    optional_fields: tuple[str,...]
    field_types: tuple[tuple[str,str],...]
    field_units: tuple[tuple[str,str],...]
    identity_fields: tuple[str,...]
    minimum_rows: int
    maximum_rows: int
    contract_fingerprint: str

    @classmethod
    def fingerprint(cls,**values):
        canonical={key:(list(value) if isinstance(value,tuple) else value) for key,value in values.items()}
        canonical["field_types"]=[list(x) for x in values["field_types"]]; canonical["field_units"]=[list(x) for x in values["field_units"]]
        return hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


@dataclass(frozen=True)
class ObservedPublicSourceSchema:
    source_id: str
    dataset_id: str
    fields: tuple[str,...]
    field_types: tuple[tuple[str,str],...]
    field_units: tuple[tuple[str,str],...]
    row_count: int
    duplicate_identity_count: int


@dataclass(frozen=True)
class PublicSourceSchemaDriftAssessment:
    status: str
    ingestion_allowed: bool
    reason_codes: tuple[str,...]
    added_optional_fields: tuple[str,...]
    non_authority_statement: str="Schema compatibility only; it does not validate factual accuracy or analytical meaning."


def assess_public_source_schema_drift(contract,observed):
    if not isinstance(contract,PublicSourceSchemaContract) or not isinstance(observed,ObservedPublicSourceSchema): raise ValueError("schema contract and observed schema are required")
    values={key:getattr(contract,key) for key in ("contract_id","source_id","dataset_id","required_fields","optional_fields","field_types","field_units","identity_fields","minimum_rows","maximum_rows")}
    if PublicSourceSchemaContract.fingerprint(**values)!=contract.contract_fingerprint: return PublicSourceSchemaDriftAssessment("INVALID_CONTRACT",False,("CONTRACT_FINGERPRINT_MISMATCH",),())
    reasons=[]
    if observed.source_id!=contract.source_id or observed.dataset_id!=contract.dataset_id: reasons.append("SOURCE_OR_DATASET_IDENTITY_CHANGED")
    missing=set(contract.required_fields)-set(observed.fields)
    if missing: reasons.append("REQUIRED_FIELDS_MISSING")
    expected_types=dict(contract.field_types); actual_types=dict(observed.field_types)
    if any(actual_types.get(field)!=kind for field,kind in expected_types.items() if field in contract.required_fields): reasons.append("REQUIRED_FIELD_TYPE_CHANGED")
    expected_units=dict(contract.field_units); actual_units=dict(observed.field_units)
    if any(actual_units.get(field)!=unit for field,unit in expected_units.items()): reasons.append("FIELD_UNIT_CHANGED")
    if not contract.minimum_rows<=observed.row_count<=contract.maximum_rows: reasons.append("ROW_COUNT_OUT_OF_CONTRACT")
    if observed.duplicate_identity_count>0: reasons.append("DUPLICATE_IDENTITIES_PRESENT")
    known=set(contract.required_fields)|set(contract.optional_fields); added=tuple(sorted(set(observed.fields)-known))
    breaking=bool(reasons)
    status="BREAKING_DRIFT" if breaking else "NON_BREAKING_ADDITIVE_DRIFT" if added else "SCHEMA_COMPATIBLE"
    return PublicSourceSchemaDriftAssessment(status,not breaking,tuple(reasons),added)


__all__=["PublicSourceSchemaContract","ObservedPublicSourceSchema","PublicSourceSchemaDriftAssessment","assess_public_source_schema_drift"]
