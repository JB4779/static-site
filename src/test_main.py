import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(
            extract_title(markdown),
            "Hello",
        )

    def test_extract_title_with_whitespace(self):
        markdown = "#    Hello World    "

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_extract_title_after_other_content(self):
        markdown = """
This is some introductory text.

# Tolkien Fan Club

More content here.
"""

        self.assertEqual(
            extract_title(markdown),
            "Tolkien Fan Club",
        )

    def test_h2_is_not_title(self):
        markdown = "## This is an h2"

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_title(self):
        markdown = """
This document has no h1 heading.

## Only an h2
"""

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()