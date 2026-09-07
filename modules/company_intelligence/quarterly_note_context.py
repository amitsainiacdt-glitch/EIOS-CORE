"""Explicit text mentions for reviewers; never infer note applicability."""
import re
from modules.company_intelligence.quarterly_date_comparison import parse_date_cell


def note_context(passage, *, basis, period_end):
    text = re.sub(r'\s+', ' ', passage)
    bases = sorted({value.upper() for value in re.findall(r'\b(standalone|consolidated)\b', text, re.I)})
    dates, unreadable = [], []
    for token in re.findall(r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}\s*[A-Za-z]+\s+\d{4})\b', text):
        parsed = parse_date_cell(token)
        if 'date' in parsed:
            dates.append(parsed['date'])
        else:
            unreadable.append(token)
    dates = sorted(set(dates))
    cues = []
    if bases and basis not in bases:
        cues.append('The text names ' + ' and '.join(bases).lower() + ' accounts, while the figures above are ' + basis.lower() + '. Do not transfer the note automatically.')
    elif len(bases) == 2:
        cues.append('The passage mentions both accounting bases. Check which part concerns the figures above.')
    elif bases:
        cues.append('The passage names the same accounting basis, but this alone does not establish applicability.')
    else:
        cues.append('The accounting basis is not explicit in this passage.')
    if period_end in dates:
        cues.append('The displayed period-end date is mentioned. Other dates may have a different role; confirm the note applies to this quarter.')
    elif dates:
        cues.append('Other dates are mentioned, but the displayed period-end date is not clearly identified. Do not treat this as a current-quarter adjustment without review.')
    else:
        cues.append('No complete date was recognised. Read the original passage before assigning it to a quarter.')
    if unreadable:
        cues.append('At least one date-like phrase could not be read reliably.')
    return {'basisMentions': bases, 'dateMentions': dates, 'cues': cues,
            'status': 'APPLICABILITY_UNCONFIRMED', 'creates_approved_facts': False}
