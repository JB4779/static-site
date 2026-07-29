import unittest

from splitnode import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a ",
                    TextType.TEXT,
                ),
                TextNode(
                    "code block",
                    TextType.CODE,
                ),
                TextNode(
                    " word",
                    TextType.TEXT,
                ),
            ],
        )

    def test_split_bold(self):
        node = TextNode(
            "This has a **bold phrase** inside",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode(
            "This has an _italic phrase_ inside",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode(
            "Use `print()` and `return` here",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("return", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_non_text_node_unchanged(self):
        node = TextNode(
            "Already bold",
            TextType.BOLD,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(new_nodes, [node])

    def test_missing_closing_delimiter(self):
        node = TextNode(
            "This has an `unfinished code block",
            TextType.TEXT,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )


if __name__ == "__main__":
    unittest.main()