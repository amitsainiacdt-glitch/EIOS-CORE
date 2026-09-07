import unittest
from modules.company_intelligence.quarterly_heading_partition import propose_duration_partition


class HeadingPartitionTests(unittest.TestCase):
    def columns(self):
        return [{'column_index': i, 'x_bounds': [i * 50, (i + 1) * 50]} for i in range(4)]

    def words(self):
        return [{'text': t, 'x': (a+b)/2, 'x0': a, 'x1': b, 'y': 10}
                for t,a,b in [('Quarter',50,75), ('ended',80,100), ('Year',155,170), ('ended',175,195)]]

    def test_unique_three_quarters_one_annual_proposal(self):
        spans = propose_duration_partition(self.words(), self.columns())
        self.assertEqual([(s['first_column'], s['last_column']) for s in spans], [(0,2),(3,3)])
        self.assertTrue(all(s['status'] == 'GEOMETRIC_PARTITION_PENDING_REVIEW' for s in spans))

    def test_corrupt_prefix_not_guessed(self):
        words = self.words()
        words[0]['text'] = 'Quar1er'
        self.assertEqual(propose_duration_partition(words, self.columns()), [])

    def test_misaligned_headings_not_assigned(self):
        words = self.words()
        for w in words[:2]:
            for key in ('x','x0','x1'):
                w[key] += 12
        self.assertEqual(propose_duration_partition(words, self.columns()), [])

    def test_multiple_possible_partitions_rejected(self):
        self.assertEqual(propose_duration_partition(self.words(), self.columns(), tolerance=200), [])
