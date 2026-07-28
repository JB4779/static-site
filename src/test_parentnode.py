import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text"
            "<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"},
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main">'
            "<span>child</span></div>",
        )

    def test_to_html_without_tag(self):
        parent_node = ParentNode(
            None,
            [LeafNode("span", "child")],
        )

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])

        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

    def test_deeply_nested_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Deep text"),
                            ],
                        ),
                    ],
                ),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>Deep text</b></p>"
            "</section></div>",
        )


if __name__ == "__main__":
    unittest.main()