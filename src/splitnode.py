from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: missing closing delimiter '{delimiter}'"
            )

        split_nodes = []

        for index, section in enumerate(sections):
            if section == "":
                continue

            if index % 2 == 0:
                split_nodes.append(
                    TextNode(section, TextType.TEXT)
                )
            else:
                split_nodes.append(
                    TextNode(section, text_type)
                )

        new_nodes.extend(split_nodes)

    return new_nodes



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)

            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(image_alt, TextType.IMAGE, image_url)
            )

            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            sections = remaining_text.split(link_markdown, 1)

            if sections[0] != "":
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(anchor_text, TextType.LINK, url)
            )

            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes
