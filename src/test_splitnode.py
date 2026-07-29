import unittest

from splitnode import split_nodes_delimiter, split_nodes_link, split_nodes_image
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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another "
            "![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "Here is an ![image](https://example.com/image.png).",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) comes first",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" comes first", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "The image comes last ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("The image comes last ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This text has no images.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_image_non_text_node(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.BOLD,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_images_from_multiple_nodes(self):
        node1 = TextNode(
            "First ![one](https://example.com/one.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Second ![two](https://example.com/two.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node1, node2])

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "one",
                    TextType.IMAGE,
                    "https://example.com/one.png",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "two",
                    TextType.IMAGE,
                    "https://example.com/two.png",
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link "
            "[to boot dev](https://www.boot.dev) "
            "and "
            "[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) today.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" today.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is useful",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" is useful", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This text has no links.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_link_non_text_node(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.ITALIC,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_links_from_multiple_nodes(self):
        node1 = TextNode(
            "First [link](https://example.com/one)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Second [link](https://example.com/two)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node1, node2])

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com/one",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com/two",
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()