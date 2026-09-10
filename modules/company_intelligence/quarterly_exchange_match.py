"""Select one exact-period NSE corroboration for an issuer PDF page."""
from datetime import datetime
from modules.company_intelligence.quarterly_date_comparison import parse_date_cell


def select_exchange_corroboration(page: dict, reports, *, ticker: str):
    context=page.get('statement_context',{}); basis=context.get('basis_candidates',[])
    if len(basis)!=1:return None
    dates=[]
    title=parse_date_cell(context.get('current_quarter_end_text'))
    if title.get('date'):dates.append(title['date'])
    for table in page.get('ruled_tables',[]):
        for column in table.get('columns',[]):
            parsed=parse_date_cell(column.get('date_header_text'))
            if parsed.get('date'):dates.append(parsed['date'])
    dates=set(dates)
    matches=[]
    for report in reports or ():
        metadata=report.get('metadata',{})
        try:end=datetime.strptime(metadata.get('period_end',''),'%d-%m-%Y').date().isoformat()
        except (TypeError,ValueError):continue
        if (report.get('status')=='EXCHANGE_CORROBORATION_CANDIDATE'
                and metadata.get('ticker','').upper()==ticker.upper()
                and metadata.get('basis','').upper()==basis[0]
                and end in dates):matches.append(report)
    if len(matches)>1:raise ValueError('multiple NSE corroborations match issuer PDF period and basis')
    return matches[0] if matches else None


__all__=['select_exchange_corroboration']
