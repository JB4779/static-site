import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        child1 = HTMLNode("b", "Bold text")
        child2 = HTMLNode("i", "Italic text")
        child3 = HTMLNode("code", "print('hello')")

        node = HTMLNode(
            "div",
            "This is repr test",
            [child1, child2, child3],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        result = repr(node)

        self.assertIn("div", result)
        self.assertIn("This is repr test", result)
        self.assertIn("Bold text", result)
        self.assertIn("Italic text", result)
        self.assertIn("print('hello')", result)
        self.assertIn("href", result)

    def test_repr_with_props_none(self):
        child1 = HTMLNode("b", "Bold text")

        node = HTMLNode(
            "div",
            "This is props_none test",
            [child1],
        )

        result = repr(node)

        self.assertIn("div", result)
        self.assertIn("props", result)
        self.assertIn("None", result)

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        result = node.props_to_html()

        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "Paragraph")

        result = node.props_to_html()

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()