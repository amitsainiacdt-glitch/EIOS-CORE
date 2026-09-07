"""Deterministic, non-advisory explanation of checked quarterly figures."""
from decimal import Decimal, InvalidOperation


NOTE_MEANINGS = {
    'LIMITED_REVIEW': 'The auditors performed a limited quarterly review, which is narrower than a full annual audit.',
    'COMPARABILITY': 'The company structure or accounting context changed, so a simple year-on-year comparison may mislead.',
    'BALANCING_QUARTER': 'The quarter may be derived from annual and nine-month totals rather than reported independently in the same form.',
    'IMPAIRMENT': 'An asset-value reduction may affect profit. EIOS must separate a genuine one-off charge from evidence of a weak past investment.',
    'RESTATEMENT_OR_REGROUPING': 'Earlier figures may have been revised or rearranged, so EIOS must compare like with like.',
}


def explain_quarterly_financials(assessment, reporting_notes=None, prior_comparable=None):
    figures = assessment.get('figures_for_review_inr_crore', {})
    if not assessment.get('technical_checks_passed') or not all(key in figures for key in ('revenue','other_income','total_income','pat')):
        return {'posture':'FIGURES_WITHHELD', 'headline':'The figures are not reliable enough to explain yet.',
                'summary':'At least one extraction or arithmetic check failed. EIOS is withholding interpretation rather than guessing.',
                'figure_explanations':[], 'accounting_note_explanations':[],
                'conclusion':'No business conclusion can be drawn from this packet.', 'limitations':assessment.get('not_checked', [])}
    revenue, other, total, pat = (_decimal(figures[key], key) for key in ('revenue','other_income','total_income','pat'))
    margin = pat / revenue * 100 if revenue else None
    other_share = other / total * 100 if total else None
    explanations = [
        f'Revenue from operations was ₹{_money(revenue)} crore. This shows the scale of sales for the quarter; by itself it does not show whether the business improved.',
        f'Net profit was ₹{_money(pat)} crore. The company retained about {_percent(margin)} of profit for every ₹100 of operating revenue.' if margin is not None else 'Revenue was zero, so a profit margin is not meaningful.',
        f'Other income was ₹{_money(other)} crore, about {_percent(other_share)} of total income. A low share means reported income is mostly linked to operations; it does not prove earnings quality.' if other_share is not None else 'Total income was zero, so the contribution from other income is not meaningful.',
        f'Revenue plus other income reconciles to total income of ₹{_money(total)} crore.',
    ]
    posture, direction = 'SINGLE_PERIOD_CONTEXT_ONLY', 'The quarter provides a checked starting point, but not a trend.'
    if prior_comparable:
        prior_revenue = _decimal(prior_comparable.get('revenue'), 'prior revenue')
        prior_pat = _decimal(prior_comparable.get('pat'), 'prior profit')
        revenue_growth = _change(revenue, prior_revenue); profit_growth = _change(pat, prior_pat)
        prior_margin = prior_pat / prior_revenue * 100 if prior_revenue else None
        explanations.append(f'Against the comparable period, revenue changed by {_signed(revenue_growth)} and profit changed by {_signed(profit_growth)}.')
        if margin is not None and prior_margin is not None:
            explanations.append(f'Net profit margin moved from {_percent(prior_margin)} to {_percent(margin)}, a change of {_signed_points(margin-prior_margin)} percentage points.')
        posture = 'COMPARATIVE_CONTEXT_AVAILABLE'
        direction = _direction(revenue_growth, profit_growth, margin, prior_margin)
    notes, unresolved = [], 0
    for note in (reporting_notes or {}).get('candidates', []):
        review = note.get('human_review')
        if not review or review.get('decision') == 'UNRESOLVED':
            unresolved += 1; continue
        if review.get('decision') == 'APPLIES':
            notes.append({'topic':note.get('topic','REPORTING_NOTE'), 'meaning':NOTE_MEANINGS.get(note.get('topic'), 'This reporting note affects how the selected figures should be read.'),
                          'review_rationale':review.get('rationale','')})
    if unresolved:
        notes.append({'topic':'REVIEW_INCOMPLETE', 'meaning':f'{unresolved} reporting-note passage(s) still need a conclusive human applicability decision.', 'review_rationale':''})
    return {'posture':posture, 'headline':_headline(revenue, pat, margin),
            'summary':direction, 'figure_explanations':explanations, 'accounting_note_explanations':notes,
            'conclusion':direction + ' This is financial evidence, not an investment verdict.',
            'limitations':assessment.get('not_checked', [])}


def _headline(revenue, pat, margin):
    return f'₹{_money(revenue)} crore revenue produced ₹{_money(pat)} crore profit' + (f' — a {_percent(margin)} net margin.' if margin is not None else '.')


def _direction(revenue_growth, profit_growth, margin, prior_margin):
    if revenue_growth is None or profit_growth is None: return 'The comparable base is zero, so growth percentages would be misleading.'
    if revenue_growth > 0 and profit_growth > revenue_growth: return 'Sales and profit both increased, with profit growing faster—a positive operating sign that still needs cash-flow and one-off checks.'
    if revenue_growth > 0 and profit_growth < 0: return 'Sales increased but profit fell, which points to margin pressure, higher costs or adverse one-offs requiring explanation.'
    if revenue_growth < 0 and profit_growth > 0: return 'Sales declined while profit increased, suggesting better mix, cost control or one-off support; durability is not yet proven.'
    if revenue_growth < 0 and profit_growth < 0: return 'Sales and profit both declined. EIOS should identify whether this is cyclical, company-specific or temporary before judging it.'
    return 'The movements are mixed or broadly flat; further comparable periods and cash flow are needed.'


def _decimal(value, name):
    try: result=Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc: raise ValueError(f'{name} must be numeric') from exc
    if not result.is_finite(): raise ValueError(f'{name} must be finite')
    return result
def _change(current, prior): return None if prior == 0 else (current-prior)/abs(prior)*100
def _money(value): return f'{value:,.2f}'
def _percent(value): return 'not meaningful' if value is None else f'{value:.2f}%'
def _signed(value): return 'not measurable' if value is None else f'{value:+.2f}%'
def _signed_points(value): return f'{value:+.2f}'


__all__=['explain_quarterly_financials']
