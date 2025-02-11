import enum
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter in node.text:
                split_text = node.text.split(delimiter)
                for i, piece in enumerate(split_text):
                    if i % 2 == 0:
                        result.append(TextNode(piece, TextType.TEXT))
                    else:
                        result.append(TextNode(piece, text_type))
        else:
            result.append(node)
    return result
            

def extract_markdown_images(text): 
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
           result.append(node)
           continue

        text = node.text
        for i, (alt_text, url) in enumerate(images):
            parts = text.split(f"![{alt_text}]({url})", 1)
            if parts[0] != "":
                result.append(TextNode(parts[0], TextType.TEXT))
    
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            text = parts[1]

        if text != "":
            result.append(TextNode(text, TextType.TEXT))

    return result
           



def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue

        text = node.text
        for i, (alt_text, url)in enumerate(links):
            parts = text.split(f"[{alt_text}]({url})", 1)
            if parts[0] != "":
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(alt_text, TextType.LINK, url))
            text = parts[1]
        
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
    
    return result