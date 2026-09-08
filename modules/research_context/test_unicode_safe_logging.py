import io
import unittest
from unittest.mock import patch

from modules.research_context.research_context import ResearchContext


class AsciiStream(io.StringIO):
    @property
    def encoding(self):
        return "ascii"

    def write(self, value):
        value.encode("ascii")
        return super().write(value)


class UnicodeSafeLoggingTests(unittest.TestCase):
    def test_unicode_title_cannot_break_publication(self):
        context = ResearchContext()
        intelligence = type("Item", (), {"title": "Official rainfall वर्षा"})()
        output = AsciiStream()
        with patch("sys.stdout", output):
            context.publish_intelligence(intelligence)
        self.assertEqual(context.intelligence_mesh.count(), 1)
        self.assertIn("Published Intelligence", output.getvalue())


if __name__ == "__main__":
    unittest.main()
