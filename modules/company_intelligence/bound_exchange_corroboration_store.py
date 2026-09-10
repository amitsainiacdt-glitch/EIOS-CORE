"""Verify and load automatically bound NSE corroborations from the review store."""
import json
from pathlib import Path
from modules.company_intelligence.exchange_ixbrl_auto_binding import apply_automatic_column_binding


def load_bound_exchange_corroborations(root: Path, ticker: str):
    base=Path(root)/ticker.upper()
    if not base.exists(): return ()
    result=[]; identities=set()
    for bound_path in sorted(base.glob('*/exchange-ixbrl-bound-corroboration.json')):
        candidate_path=bound_path.with_name('exchange-ixbrl-candidate.json')
        assessment_path=bound_path.with_name('exchange-ixbrl-auto-binding.json')
        if not candidate_path.is_file() or not assessment_path.is_file():
            raise ValueError('bound NSE corroboration lineage is incomplete')
        try:
            candidate=json.loads(candidate_path.read_text(encoding='utf-8'))
            assessment=json.loads(assessment_path.read_text(encoding='utf-8'))
            bound=json.loads(bound_path.read_text(encoding='utf-8'))
        except (OSError,UnicodeDecodeError,json.JSONDecodeError) as exc:
            raise ValueError('bound NSE corroboration is unreadable') from exc
        if apply_automatic_column_binding(candidate,assessment)!=bound:
            raise ValueError('bound NSE corroboration does not match its verified lineage')
        metadata=bound['metadata']
        if metadata.get('ticker','').upper()!=ticker.upper(): raise ValueError('bound NSE corroboration ticker mismatch')
        identity=(metadata.get('period_end'),str(metadata.get('basis','')).upper())
        if identity in identities: raise ValueError('duplicate bound NSE corroboration period and basis')
        identities.add(identity);result.append(bound)
    return tuple(result)


__all__=['load_bound_exchange_corroborations']
