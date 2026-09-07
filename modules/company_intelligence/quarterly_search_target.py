"""Indian April-March quarter search targeting; metadata is not source approval."""
from datetime import date
import re
from urllib.parse import urlsplit


def quarterly_search_plan(company, issuer_domain, period_end):
    end = date.fromisoformat(period_end)
    if (end.month, end.day) not in {(3,31), (6,30), (9,30), (12,31)}:
        raise ValueError('Expected an Indian fiscal quarter end')
    if not re.fullmatch(r'[a-z0-9]+(?:[-.][a-z0-9]+)*\.[a-z]{2,}', issuer_domain):
        raise ValueError('Expected issuer domain only')
    quarter = {6:1, 9:2, 12:3, 3:4}[end.month]
    year = end.year if end.month == 3 else end.year + 1
    label = f'Q{quarter} FY{year}'
    return {'company':company, 'issuer_domain':issuer_domain, 'period_end':period_end,
            'quarter':quarter, 'fiscal_year_end':year, 'label':label,
            'calendar':'INDIA_APRIL_MARCH',
            'queries': [f'{company} "Q{quarter}" "FY{year % 100:02d}" financial results site:{issuer_domain}',
                        f'{company} "{end.day} {end.strftime("%B")} {end.year}" financial results site:{issuer_domain}'],
            'creates_approved_facts':False}


def assess_quarterly_search_results(results, plan):
    assessed = []
    for result in results:
        url, title = result.url, result.title
        parsed = urlsplit(url)
        host = (parsed.hostname or '').lower()
        domain = plan['issuer_domain']
        official = (parsed.scheme == 'https' and not parsed.username and not parsed.password
                    and (host == domain or host.endswith('.' + domain)))
        mentions = set()
        invalid_range = False
        # Use explicit title labels only; snippets may describe comparison periods.
        # Fiscal-year ranges mean the ending year: FY2026-27 => FY2027.
        for match in re.finditer(r'\bQ([1-4])[\s_-]*FY[\s_-]*(\d{4}|\d{2})(?:\s*[-/]\s*(\d{4}|\d{2}))?\b', title, re.I):
            year = int(match[3] or match[2])
            if year < 100:
                year += 2000
            if match[3]:
                start = int(match[2])
                if start < 100:
                    start += 2000
                if year != start + 1:
                    invalid_range = True
            mentions.add((int(match[1]),year))
        target = (plan['quarter'], plan['fiscal_year_end'])
        if not official:
            status = 'UNTRUSTED_SOURCE_LOCATION'
        elif invalid_range:
            status = 'AMBIGUOUS_PERIOD_METADATA'
        elif not mentions:
            status = 'PERIOD_UNCONFIRMED'
        elif len(mentions) > 1:
            status = 'AMBIGUOUS_PERIOD_METADATA'
        elif target not in mentions:
            status = 'DIFFERENT_QUARTER'
        else:
            status = 'TARGET_QUARTER_CANDIDATE'
        assessed.append({'title':title, 'url':url, 'status':status,
                         'title_periods':[f'Q{q} FY{y}' for q,y in sorted(mentions)],
                         'document_contents_verified':False})
    return {'target':plan['label'], 'period_end':plan['period_end'], 'results':assessed,
            'candidate_count':sum(r['status']=='TARGET_QUARTER_CANDIDATE' for r in assessed),
            'creates_approved_facts':False, 'changes_verdict':False}
