from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node

def test_text_node_to_html():
    node = TextNode("Hello World!", TextType.TEXT)
    result = text_node_to_html_node(node)
    assert result.tag == None
    assert result.value == "Hello World!"
    assert result.props == {}

def test_bold_node_to_html():
    node = TextNode("Hello Bold!", TextType.BOLD)
    result = text_node_to_html_node(node)
    assert result.tag == "b"
    assert result.value == "Hello Bold!"
    assert result.props == {}

def test_italic_node_to_html():
    node = TextNode("Hello Italics!", TextType.ITALIC)
    result = text_node_to_html_node(node)
    assert result.tag == "i"
    assert result.value == "Hello Italics!"
    assert result.props == {}

def test_code_node_to_html():
    node = TextNode("Hello Code!", TextType.CODE)
    result = text_node_to_html_node(node)
    assert result.tag == "code"
    assert result.value == "Hello Code!"
    assert result.props == {}

def test_link_node_to_html():
    node = TextNode("Hello Link!", TextType.LINK, "https://google.com")
    result = text_node_to_html_node(node)
    assert result.tag == "a"
    assert result.value == "Hello Link!"
    assert result.props == {"href": "https://google.com"}

def test_image_node_to_html():
    node = TextNode("google", TextType.IMAGE, "https://google.com")
    result = text_node_to_html_node(node)
    assert result.tag == "img"
    assert result.value == ""
    assert result.props == {"src": "https://google.com", "alt": "google"}

def test_invalid_node_to_html():
    try:
        node = TextNode("Invalid!", "Invalid_Type")
        text_node_to_html_node(node)
        assert False, "Expected an exception"
    except Exception:
        assert True