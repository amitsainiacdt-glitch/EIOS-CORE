"""Separate a successful process exit from actual document collection progress."""


def describe_document_collection(summary):
    counts = {}
    for key in ('candidates_seen', 'archived', 'unchanged', 'failed', 'extracted',
                'fact_candidates_queued', 'extraction_holds'):
        value = summary.get(key)
        if type(value) is not int or value < 0:
            return {'status': 'COLLECTION_RESULT_UNAVAILABLE',
                    'message': 'Document collection counts are missing or invalid. Progress cannot be confirmed.',
                    'new_facts_approved': False}
        counts[key] = value
    if counts['failed'] or counts['extraction_holds']:
        state = 'COLLECTION_NEEDS_ATTENTION'
        message = f"{counts['extracted']} documents extracted; {counts['failed']} failed and {counts['extraction_holds']} held for review."
    elif counts['fact_candidates_queued']:
        state = 'FACT_CANDIDATES_AWAITING_REVIEW'
        message = f"{counts['extracted']} documents extracted and {counts['fact_candidates_queued']} fact candidates queued. These are not approved facts."
    elif counts['extracted']:
        state = 'DOCUMENTS_EXTRACTED_NO_FACT_CANDIDATES'
        message = f"{counts['extracted']} documents extracted, but no new fact candidates were queued."
    elif counts['unchanged']:
        state = 'EXISTING_DOCUMENTS_UNCHANGED'
        message = f"{counts['unchanged']} known documents were unchanged; no new documents were extracted."
    else:
        state = 'NO_DOCUMENTS_EXTRACTED'
        message = 'No documents were extracted. A completed run does not prove fresh company data was obtained.'
    return {'status': state, 'message': message, 'counts': counts, 'new_facts_approved': False}
