"""Discovery-visible integration coverage for the first controlled writer."""

import unittest

from modules.external_intelligence.test_public_factual_observation_proposal import main


class ReviewedPublicFactualControlledWriteIntegrationTests(unittest.TestCase):
    def test_reviewed_fact_commit_and_controlled_conflict_block(self):
        main()


if __name__ == "__main__":
    unittest.main()
