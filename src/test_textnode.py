import unittest
from textnode import TextNode, TextType, text_node_to_html_node 


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_default(self):
        node = TextNode("This is a test", TextType.ITALIC)
        self.assertIsNone(node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):      
    def test_text(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode(
            "This is bold text",
            TextType.BOLD,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode(
            "This is italic text",
            TextType.ITALIC,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode(
            "print('hello')",
            TextType.CODE,
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode(
            "Click me!",
            TextType.LINK,
            "https://www.google.com",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.google.com"},
        )

    def test_image(self):
        node = TextNode(
            "Whalen logo",
            TextType.IMAGE,
            "images/logo.png",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "images/logo.png",
                "alt": "Whalen logo",
            },
        )

    def test_invalid_text_type(self):
        node = TextNode(
            "Invalid text",
            "INVALID",
        )





if __name__ == "__main__":
    unittest.main()

