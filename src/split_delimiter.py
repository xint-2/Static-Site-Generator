import enum
import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from text_to_html import text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    result = []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    result.extend(nodes)
    return result    

def markdown_to_blocks(markdown):
    results = []
    lines = markdown.split("\n")

    current_block = []
    for line in lines:
        if line.strip() == "":
            if current_block:
                results.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        results.append("\n".join(current_block).strip())
    
    return results

def block_to_block_type(block):

    lines = block.split("\n")

    if block.startswith("#"):
        count = 0
        for char in block:
            if char != "#":
                break
            count += 1
        if count > 0 and count <= 6:
            if block[count] == " ":
                return "heading"

    if block.startswith("```"):
        if block.endswith("```"):
            return "code"
    
    is_quote = True
    for line in lines:
        if line and not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return "quote"

    is_unordered = True
    for line in lines:
        if line and not (line.startswith("* ") or line.startswith("- ")):
            is_unordered = False
            break
    if is_unordered:
        return "unordered_list"

    is_ordered = True
    expected_number = 1
    for line in lines:
        expected_pattern =f"{expected_number}. "
        if not line.startswith(expected_pattern):
            is_ordered = False
            break
        expected_number += 1
    if is_ordered:
        return "ordered_list"
    
    return "paragraph"

def markdown_to_html_node(markdown):
    parent = HTMLNode("div", None, [])
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
       block_type = block_to_block_type(block)
       if block_type == "paragraph": #
           paragraph_block(block, parent)
       if block_type == "code": # 
           code_block(block, parent)
       if block_type == "heading": # 
            heading_block(block, parent)
       if block_type == "ordered_list": #
           ordered_block(block, parent)
       if block_type == "quote":
           quote_block(block, parent)
       if block_type == "unordered_list": #
           unordered_block(block, parent)
    return parent

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_block(block, parent):
    paragraph_node = HTMLNode("p", None, [])
    paragraph_node.children = text_to_children(block)
    parent.children.append(paragraph_node)


def code_block(block, parent):
    pre_node = HTMLNode("pre", None, [])
    code_node = HTMLNode("code", None, [])
    code_node.children = text_to_children(block)
    pre_node.children = [code_node]
    parent.children.append(pre_node)

def heading_block(block, parent):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    heading_tag = f"h{level}"
    content = block[level:].strip()
    heading_node = HTMLNode(heading_tag, None, [])
    heading_node.children = text_to_children(content)
    parent.children.append(heading_node)

def ordered_block(block, parent):
    ordered_node = HTMLNode("ol", None, [])
    lines = block.split("\n")
    for line in lines:
        content = line.split(".", 1)[1].strip()
        list_item = HTMLNode("li", None, [])
        list_item.children = text_to_children(content)
        ordered_node.children.append(list_item)
    parent.children.append(ordered_node)


def quote_block(block, parent):
    quote_node = HTMLNode("blockquote", None, [])
    content = block.replace("> ", "")
    quote_node.children = text_to_children(content)
    parent.children.append(quote_node)


def unordered_block(block, parent):
    unordered_node = HTMLNode("ul", None, [])
    lines = block.split("\n")
    for line in lines:
        list_item = HTMLNode("li", None, [])
        content = line.replace("* ", "")
        list_item.children = text_to_children(content)
        unordered_node.children.append(list_item)
    parent.children.append(unordered_node)
