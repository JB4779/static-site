from textnode import TextNode, TextType

def main():
    node = TextNode("Hello World!", TextType.LINK, "https://whalenfurniture.com")
    print(node)


if __name__ == "__main__":
    main()