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
                'profit_bridge':None, 'cost_attribution':None,
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
    posture, direction, bridge, cost_attribution = 'SINGLE_PERIOD_CONTEXT_ONLY', 'The quarter provides a checked starting point, but not a trend.', None, None
    if prior_comparable:
        prior_revenue = _decimal(prior_comparable.get('revenue'), 'prior revenue')
        prior_pat = _decimal(prior_comparable.get('pat'), 'prior profit')
        revenue_growth = _change(revenue, prior_revenue); profit_growth = _change(pat, prior_pat)
        prior_margin = prior_pat / prior_revenue * 100 if prior_revenue else None
        explanations.append(f'Against the comparable period, revenue changed by {_signed(revenue_growth)} and profit changed by {_signed(profit_growth)}.')
        if margin is not None and prior_margin is not None:
            explanations.append(f'Net profit margin moved from {_percent(prior_margin)} to {_percent(margin)}, a change of {_signed_points(margin-prior_margin)} percentage points.')
            expected_pat = revenue * prior_margin / 100
            bridge = {'revenue_change_crore':_plain(revenue-prior_revenue),
                      'pat_change_crore':_plain(pat-prior_pat),
                      'pat_at_prior_margin_crore':_plain(expected_pat),
                      'profit_gap_vs_prior_margin_crore':_plain(pat-expected_pat),
                      'other_income_change_crore':_plain(other-_decimal(prior_comparable.get('other_income', '0'),'prior other income')) if 'other_income' in prior_comparable else None,
                      'meaning':f'If the earlier {_percent(prior_margin)} net margin had continued, current revenue would have produced about ₹{_money(expected_pat)} crore profit. Actual profit was ₹{_money(pat)} crore, a {_gap_words(pat-expected_pat)} versus that benchmark.',
                      'not_yet_attributed':['Raw-material and traded-goods costs','Inventory movement','Employee and operating expenses','Finance and depreciation','Tax, exceptional items and accounting adjustments']}
        cost_attribution = _cost_attribution(figures, prior_comparable, revenue, prior_revenue, pat, prior_pat)
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
            'profit_bridge':bridge,
            'cost_attribution':cost_attribution,
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
def _plain(value): return format(value.quantize(Decimal('0.01')), 'f')
def _gap_words(value): return f'₹{_money(abs(value))} crore shortfall' if value < 0 else f'₹{_money(value)} crore surplus'


def _cost_attribution(current, prior, current_revenue, prior_revenue, current_pat, prior_pat):
    required=('total_expenses','pbt_before_exceptional')
    if not all(key in current and key in prior for key in required): return None
    total_current=_decimal(current['total_expenses'],'current total expenses'); total_prior=_decimal(prior['total_expenses'],'prior total expenses')
    pbt_current=_decimal(current['pbt_before_exceptional'],'current PBT'); pbt_prior=_decimal(prior['pbt_before_exceptional'],'prior PBT')
    lines=[]; explained=Decimal('0')
    labels={'raw_materials':'Raw materials','traded_goods_purchases':'Purchases of traded goods',
            'inventory_change':'Inventory movement','employee_benefits':'Employee benefits',
            'finance_costs':'Finance costs','depreciation_amortisation':'Depreciation and amortisation',
            'freight_distribution':'Freight and distribution','other_expenses':'Other expenses'}
    for key,label in labels.items():
        if key not in current or key not in prior: continue
        now=_decimal(current[key],key); before=_decimal(prior[key],key); delta=now-before; explained+=delta
        lines.append({'metric':key,'label':label,'current_crore':_plain(now),'prior_crore':_plain(before),
                      'change_crore':_plain(delta),'change_percent':_plain(_change(now,before)) if before else None,
                      'effect':'PRESSURE' if delta>0 else 'RELIEF' if delta<0 else 'NEUTRAL'})
    total_delta=total_current-total_prior; revenue_growth=_change(current_revenue,prior_revenue); expense_growth=_change(total_current,total_prior)
    below_pbt_current=pbt_current-current_pat; below_pbt_prior=pbt_prior-prior_pat
    return {'total_expenses_current_crore':_plain(total_current),'total_expenses_prior_crore':_plain(total_prior),
            'total_expense_change_crore':_plain(total_delta),'total_expense_change_percent':_plain(expense_growth),
            'revenue_change_percent':_plain(revenue_growth),'pbt_change_crore':_plain(pbt_current-pbt_prior),
            'pbt_change_percent':_plain(_change(pbt_current,pbt_prior)),
            'pbt_margin_current_percent':_plain(pbt_current/current_revenue*100),
            'pbt_margin_prior_percent':_plain(pbt_prior/prior_revenue*100),
            'comparable_lines':lines,'unallocated_expense_change_crore':_plain(total_delta-explained),
            'below_pbt_burden_change_crore':_plain(below_pbt_current-below_pbt_prior),
            'meaning':f'Total expenses rose {_percent(expense_growth)} while revenue rose {_percent(revenue_growth)}. Costs therefore grew faster than sales, compressing profit before exceptional items and tax.',
            'boundary':'The difference between PBT and PAT includes tax and may include other below-PBT effects; it is not labelled as tax alone.'}


__all__=['explain_quarterly_financials']
