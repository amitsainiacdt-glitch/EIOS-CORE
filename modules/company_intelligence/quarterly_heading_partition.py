"""Propose uniquely centred heading spans for an unruled header; not approval."""
from itertools import combinations
import re


def propose_duration_partition(words, columns, tolerance=4):
    words = sorted(words, key=lambda w: w['x'])
    labels = []
    for left, right in zip(words, words[1:]):
        if (left['text'].lower() in ('quarter', 'year') and right['text'].lower() == 'ended'
                and abs(left['y'] - right['y']) <= 3):
            labels.append({'text': left['text'].capitalize() + ' ended',
                           'center': (left['x0'] + right['x1']) / 2,
                           'left': left['x0'], 'right': right['x1']})
    # Do not ignore an unreadable duration prefix or extra heading.
    if len(labels) < 2 or len(labels) != sum(bool(re.fullmatch('ended', w['text'], re.I)) for w in words):
        return []
    columns = sorted(columns, key=lambda c: c['x_bounds'][0])
    if len(columns) > 12 or len(labels) > 4 or len(labels) > len(columns):
        return []
    possibilities = []
    for cuts in combinations(range(1, len(columns)), len(labels) - 1):
        bounds = (0, *cuts, len(columns))
        spans = []
        for label, start, end in zip(labels, bounds, bounds[1:]):
            group = columns[start:end]
            left, right = group[0]['x_bounds'][0], group[-1]['x_bounds'][1]
            if (abs(label['center'] - (left + right) / 2) > tolerance
                    or label['left'] < left or label['right'] > right):
                break
            spans.append({'kind': 'duration', 'text': label['text'],
                          'first_column': group[0]['column_index'], 'last_column': group[-1]['column_index'],
                          'status': 'GEOMETRIC_PARTITION_PENDING_REVIEW'})
        if len(spans) == len(labels):
            possibilities.append(spans)
    return possibilities[0] if len(possibilities) == 1 else []
