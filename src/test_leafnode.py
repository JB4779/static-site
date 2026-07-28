import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>",
        )

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "This is raw text")

        self.assertEqual(
            node.to_html(),
            "This is raw text",
        )

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")

        self.assertEqual(
            node.to_html(),
            "<b>Bold text</b>",
        )

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")

        self.assertEqual(
            node.to_html(),
            "<code>print('hello')</code>",
        )

    def test_leaf_without_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode(
            "a",
            "Google",
            {"href": "https://www.google.com"},
        )

        result = repr(node)

        self.assertIn("LeafNode", result)
        self.assertIn("tag=a", result)
        self.assertIn("value=Google", result)
        self.assertIn("href", result)


if __name__ == "__main__":
    unittest.main()