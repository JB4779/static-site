import os
import shutil
from textnode import TextNode, TextType

def main() -> None:
    copy_static("static", "public")


def copy_static(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    copy_directory_contents(source, destination)


def copy_directory_contents(source: str, destination: str) -> None:
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            print(f"Creating directory: {destination_path}")
            os.mkdir(destination_path)

            copy_directory_contents(
                source_path,
                destination_path,
            )


if __name__ == "__main__":
    main()