import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node



class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                (
                    "This is another paragraph with _italic_ text "
                    "and `code` here\n"
                    "This is the same paragraph on a new line"
                ),
                "- This is a list\n- with items",
            ],
        )

    def test_extra_blank_lines(self):
        md = """
First block



Second block




Third block
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """

   First block

Second block   

"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
            ],
        )

    def test_single_block(self):
        md = "This is one block."

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is one block.",
            ],
        )

    def test_empty_markdown(self):
        md = ""

        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_multiline_paragraph(self):
        block = (
            "This is the first line of a paragraph.\n"
            "This is still the same paragraph."
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_level_1(self):
        block = "# Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_level_6(self):
        block = "###### Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_too_many_hashes(self):
        block = "####### Not a heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_without_space(self):
        block = "##Not a heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_block_multiple_lines(self):
        block = (
            "```\n"
            "def greet():\n"
            "    print('hello')\n"
            "```"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_missing_closing_backticks(self):
        block = "```\nprint('hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_inline_code_is_paragraph(self):
        block = "This has `inline code` in it."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote(self):
        block = "> This is a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_multiline_quote(self):
        block = (
            "> This is the first line\n"
            "> This is the second line\n"
            ">This line has no space"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = (
            "> This line is a quote\n"
            "This line is not"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = (
            "- First item\n"
            "- Second item\n"
            "- Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = (
            "- First item\n"
            "Second item\n"
            "- Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list_missing_space(self):
        block = (
            "-First item\n"
            "-Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        block = (
            "2. First item\n"
            "3. Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_skips_number(self):
        block = (
            "1. First item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_repeats_number(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "2. Another second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_missing_space(self):
        block = (
            "1.First item\n"
            "2.Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )







class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# My Heading
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>My Heading</h1></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with two lines
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item one
- Item two
- Item three
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

This is a paragraph with **bold** text.

- One
- Two

> A famous quote
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>One</li><li>Two</li></ul><blockquote>A famous quote</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
