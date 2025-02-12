import unittest
from split_delimiter import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks, block_to_block_type,
    markdown_to_html_node
)
from htmlnode import HTMLNode
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
class TestExtractionRegex(unittest.TestCase):
    def test_extraction_image(self):
        text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extraction_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extraction_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev")])

    def test_extraction_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extraction_mixed(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        link_result = extract_markdown_links(text)
        image_result = extract_markdown_images(text)
        self.assertEqual(link_result, [("to boot dev", "https://www.boot.dev")])
        self.assertEqual(image_result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extraction_None(self):
        text = "This is text with no links or images"
        link_result = extract_markdown_links(text)
        image_result = extract_markdown_images(text)
        self.assertEqual(link_result, [])
        self.assertEqual(image_result, [])

    def test_text_to_TextNodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertEqual(result, expected_result)

class TestMarkdownToBlock(unittest.TestCase):  
    def test_markdown_to_block(self):
        markdown = (
        '# Heading\n\n'
        'This is a paragraph.\n\n'
        '* Bullet 1\n* Bullet 2\n* Bullet 3\n'
        )
        result = markdown_to_blocks(markdown)
        expected_result = [
        "# Heading",
        "This is a paragraph.",
        "* Bullet 1\n* Bullet 2\n* Bullet 3"
        ]
        self.assertEqual(result, expected_result)

    def test_block_to_block_type(self):
        # Testing valid types
        heading_block = "# Heading"
        paragraph_block = "This is a paragraph."
        unordered_list_block = "* Bullet 1\n* Bullet 2\n* Bullet 3"
        code_block = "``` Here is some code ```"
        quote_block = "> Here is a quote"
        ordered_list_block = "1. First Item\n2. Second Item\n3. Third Item"
        self.assertEqual(block_to_block_type(heading_block), "heading")
        self.assertEqual(block_to_block_type(paragraph_block), "paragraph")
        self.assertEqual(block_to_block_type(unordered_list_block), "unordered_list")
        self.assertEqual(block_to_block_type(code_block), "code")
        self.assertEqual(block_to_block_type(quote_block), "quote")
        self.assertEqual(block_to_block_type(ordered_list_block), "ordered_list")
        # Testing multi-level headers
        heading2_block = "## Heading level 2"
        heading6_block = "###### Heading level 6"
        self.assertEqual(block_to_block_type(heading2_block), "heading")
        self.assertEqual(block_to_block_type(heading6_block), "heading")
        # Test invalid headiing
        invalid_heading = "#NoSpace"
        self.assertEqual(block_to_block_type(invalid_heading), "paragraph")
        # Multi-Line quote
        multiline_quote = "> First\n> Second\n> Third"
        self.assertEqual(block_to_block_type(multiline_quote), "quote")
        # Multi-Line code
        multiline_code = "```\ncode here\ncode there\n```"
        self.assertEqual(block_to_block_type(multiline_code), "code")

    def test_block_to_html(self):
        # Test paragraph
        node = markdown_to_html_node("This is a paragraph text.")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "p"

        # Test unordered list
        node = markdown_to_html_node("* Item 1\n* Item 2")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "ul"
        assert len(node.children[0].children) == 2

        # Test ordered list
        node = markdown_to_html_node("1. Item one\n2. Item Two")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "ol"
        assert len(node.children[0].children) == 2

        # Test code
        node = markdown_to_html_node("``` Some code here ```")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "pre"
        assert node.children[0].children[0].tag == "code"

        # Test heading
        node = markdown_to_html_node("# Some Heading")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "h1"

        # Test quote
        node = markdown_to_html_node("> Quote Text One\n> Quote Text Two")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "blockquote"





if __name__ == "__main__":
    unittest.main()





