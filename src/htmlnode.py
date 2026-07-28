

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        props_string: str = ""

        for key, value in self.props.items():
            props_string += f' {key}="{value}"'

        return props_string

    def __repr__(self) -> str:
        return(f"TextNode({self.tag}, {self.value}, {self.children}, {self.props})")

     