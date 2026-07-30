from enum import Enum
from parentnode import ParentNode 
from splitnode import text_to_textnodes
from textnode import TextNode, TextType
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        stripped_block = block.strip()

        if stripped_block != "":
            blocks.append(stripped_block)

    return blocks



def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading: 1-6 # characters followed by a space
    if block.startswith("#"):
        heading_parts = block.split(" ", 1)

        if len(heading_parts) == 2:
            hashes = heading_parts[0]

            if 1 <= len(hashes) <= 6 and hashes == "#" * len(hashes):
                return BlockType.HEADING

    # Code: starts with ``` and newline, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: each line starts with the expected number
    expected_number = 1

    for line in lines:
        prefix = f"{expected_number}. "

        if not line.startswith(prefix):
            break

        expected_number += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)

    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(
            text_node_to_html_node(text_node)
        )

    return html_nodes


def heading_to_html_node(block: str) -> ParentNode:
    heading_level = 0

    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break

    text = block[heading_level + 1:]

    return ParentNode(
        f"h{heading_level}",
        text_to_children(text),
    )


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))

    return ParentNode(
        "p",
        text_to_children(text),
    )


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")

    cleaned = []

    for line in lines:
        cleaned.append(line[1:].strip())

    text = " ".join(cleaned)

    return ParentNode(
        "blockquote",
        text_to_children(text),
    )


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = []

    for line in block.split("\n"):
        text = line[2:]

        items.append(
            ParentNode(
                "li",
                text_to_children(text),
            )
        )

    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = []

    for line in block.split("\n"):
        text = line.split(". ", 1)[1]

        items.append(
            ParentNode(
                "li",
                text_to_children(text),
            )
        )

    return ParentNode("ol", items)


def code_to_html_node(block: str) -> ParentNode:
    code = block[4:-3]

    if not code.endswith("\n"):
        code += "\n"

    code_node = text_node_to_html_node(
        TextNode(
            code,
            TextType.TEXT,
        )
    )

    return ParentNode(
        "pre",
        [
            ParentNode(
                "code",
                [code_node],
            )
        ],
    )


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(
                paragraph_to_html_node(block)
            )

        elif block_type == BlockType.HEADING:
            children.append(
                heading_to_html_node(block)
            )

        elif block_type == BlockType.CODE:
            children.append(
                code_to_html_node(block)
            )

        elif block_type == BlockType.QUOTE:
            children.append(
                quote_to_html_node(block)
            )

        elif block_type == BlockType.UNORDERED_LIST:
            children.append(
                unordered_list_to_html_node(block)
            )

        elif block_type == BlockType.ORDERED_LIST:
            children.append(
                ordered_list_to_html_node(block)
            )

    return ParentNode(
        "div",
        children,
    )
