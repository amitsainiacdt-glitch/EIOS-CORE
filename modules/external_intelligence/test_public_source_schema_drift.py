from dataclasses import replace

from modules.external_intelligence.public_source_schema_drift import ObservedPublicSourceSchema,PublicSourceSchemaContract,assess_public_source_schema_drift


def _contract():
    values=dict(contract_id="MANDI-V1",source_id="INDIA_OGD",dataset_id="MANDI_DAILY",required_fields=("date","state","market","commodity","modal_price"),optional_fields=("variety","grade"),field_types=(("date","DATE"),("state","TEXT"),("market","TEXT"),("commodity","TEXT"),("modal_price","DECIMAL")),field_units=(("modal_price","INR_PER_QUINTAL"),),identity_fields=("date","state","market","commodity","variety"),minimum_rows=1,maximum_rows=100000)
    return PublicSourceSchemaContract(**values,contract_fingerprint=PublicSourceSchemaContract.fingerprint(**values))


def main():
    contract=_contract(); observed=ObservedPublicSourceSchema("INDIA_OGD","MANDI_DAILY",("date","state","market","commodity","modal_price"),contract.field_types,contract.field_units,500,0)
    compatible=assess_public_source_schema_drift(contract,observed); assert compatible.status=="SCHEMA_COMPATIBLE" and compatible.ingestion_allowed
    additive=assess_public_source_schema_drift(contract,replace(observed,fields=observed.fields+("arrival_quantity",),field_types=observed.field_types+(("arrival_quantity","DECIMAL"),)))
    assert additive.status=="NON_BREAKING_ADDITIVE_DRIFT" and additive.ingestion_allowed and additive.added_optional_fields==("arrival_quantity",)
    unit=assess_public_source_schema_drift(contract,replace(observed,field_units=(("modal_price","INR_PER_KG"),))); assert unit.status=="BREAKING_DRIFT" and "FIELD_UNIT_CHANGED" in unit.reason_codes
    duplicate=assess_public_source_schema_drift(contract,replace(observed,duplicate_identity_count=2)); assert not duplicate.ingestion_allowed and "DUPLICATE_IDENTITIES_PRESENT" in duplicate.reason_codes
    tampered=assess_public_source_schema_drift(replace(contract,maximum_rows=999999),observed); assert tampered.status=="INVALID_CONTRACT"
    print("PUBLIC SOURCE SCHEMA DRIFT: ALL TESTS PASSED")


if __name__=="__main__": main()
