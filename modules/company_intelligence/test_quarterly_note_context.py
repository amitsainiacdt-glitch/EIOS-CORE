import unittest
from modules.company_intelligence.quarterly_note_context import note_context


class NoteContextTests(unittest.TestCase):
    def context(self, text):
        return note_context(text, basis='STANDALONE', period_end='2026-06-30')

    def test_other_basis_warns_without_excluding_note(self):
        result = self.context('Consolidated figures for 30 June 2026 may not be comparable.')
        self.assertIn('Do not transfer', result['cues'][0])
        self.assertEqual(result['status'], 'APPLICABILITY_UNCONFIRMED')

    def test_historical_charge_not_assigned_to_current_quarter(self):
        result = self.context('Impairment for the quarter ended 31 March 2026.')
        self.assertEqual(result['dateMentions'], ['2026-03-31'])
        self.assertIn('current-quarter adjustment', result['cues'][1])

    def test_same_basis_and_date_do_not_approve(self):
        result = self.context('Standalone quarter ended 30 June 2026.')
        self.assertFalse(result['creates_approved_facts'])
        self.assertIn('does not establish', result['cues'][0])

    def test_corrupt_date_not_repaired(self):
        result = self.context('31 Match 2026')
        self.assertEqual(result['dateMentions'], [])
        self.assertIn('could not be read', result['cues'][-1])

    def test_mixed_basis_remains_ambiguous(self):
        result = self.context('Standalone and consolidated financial results.')
        self.assertEqual(len(result['basisMentions']), 2)
        self.assertIn('both accounting bases', result['cues'][0])
