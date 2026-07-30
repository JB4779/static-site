import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_directory(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    copy_directory_contents(source, destination)


def copy_directory_contents(source: str, destination: str) -> None:
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            os.mkdir(destination_path)

            copy_directory_contents(
                source_path,
                destination_path,
            )


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def generate_page(
    from_path: str,
    template_path: str,
    dest_path: str,
    basepath: str,
) -> None:
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_page = template.replace("{{ Title }}", title)
    full_page = full_page.replace("{{ Content }}", html)

    full_page = full_page.replace(
        'href="/',
        f'href="{basepath}',
    )

    full_page = full_page.replace(
        'src="/',
        f'src="{basepath}',
    )

    destination_directory = os.path.dirname(dest_path)

    if destination_directory != "":
        os.makedirs(destination_directory, exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(full_page)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str,
) -> None:
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                destination_path = os.path.splitext(destination_path)[0]
                destination_path += ".html"

                generate_page(
                    source_path,
                    template_path,
                    destination_path,
                    basepath,
                )
        else:
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath,
            )


def main() -> None:
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_directory("static", "docs")

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath,
    )


if __name__ == "__main__":
    main()