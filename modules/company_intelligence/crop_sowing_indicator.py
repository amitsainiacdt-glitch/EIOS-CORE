"""Convert an audited official crop-area table into the governed sowing indicator."""
from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import urlsplit

from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview


def crop_sowing_indicator_candidate(preview, *, ticker, rule):
    if not isinstance(preview, PublicCropAreaPreview):
        raise ValueError('preview must be PublicCropAreaPreview')
    if rule.get('unit') != 'percent change' or rule.get('favourable_direction') != 'UP':
        raise ValueError('crop sowing rule has incompatible measurement semantics')
    totals = [item for item in preview.records if item.crop == 'Grand Total']
    if len(totals) != 1:
        raise ValueError('crop-area release must contain one Grand Total row')
    record = totals[0]
    if record.unit != 'LAKH_HECTARE' or record.prior_year_area <= 0:
        raise ValueError('crop-area total has an invalid unit or comparison base')
    current = Decimal(str(record.current_area)); prior = Decimal(str(record.prior_year_area))
    difference = Decimal(str(record.difference_from_prior_year))
    if abs((current - prior) - difference) > Decimal('0.02'):
        raise ValueError('crop-area total does not reconcile')
    percent = ((current - prior) / prior * 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    domain = (urlsplit(record.source_url).hostname or '').casefold().rstrip('.')
    if domain != rule.get('source_domain'):
        raise ValueError('crop-area source does not match the configured authority domain')
    job_id = f"{ticker.upper()}-PRIMARY-INDICATOR-{rule['id'].upper()}"
    return {'rule_id':rule['id'],'job_id':job_id,'ticker':ticker.upper(),
            'reporting_date':preview.period_label,'value':format(percent,'f'),'unit':rule['unit'],
            'source_url':record.source_url,'source_domain':domain,'evidence_passage':record.source_row,
            'content_fingerprint':record.document_hash}


def crop_mix_summary(preview):
    """Describe published crop gaps without claiming a weather cause."""
    if not isinstance(preview, PublicCropAreaPreview): raise ValueError('preview must be PublicCropAreaPreview')
    rows = [item for item in preview.records if item.crop != 'Grand Total']
    laggards = sorted(rows, key=lambda item:item.difference_from_prior_year)[:3]
    leaders = sorted(rows, key=lambda item:item.difference_from_prior_year, reverse=True)[:3]
    return {'largest_shortfalls':[{'crop':x.crop,'gap_lakh_hectare':x.difference_from_prior_year} for x in laggards],
            'largest_increases':[{'crop':x.crop,'gap_lakh_hectare':x.difference_from_prior_year} for x in leaders],
            'causes_rainfall':False,'changes_verdict':False}


__all__=['crop_sowing_indicator_candidate','crop_mix_summary']
