#!/usr/bin/python

import sys
import ast
from lark import Lark, Transformer
from pypdf import PdfReader, PdfWriter

# Define a grammar for parsing nested Lisp-like bookmarks, including double quotes for strings
grammar = """
    start: "(" "bookmarks" node* ")"
    node: "(" TITLE PAGE node* ")"

    TITLE: ESCAPED_STRING
    PAGE: "\\"#" NUMBER "\\""

    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


def add_outline(writer, tree):
    def reduce_node(node, parent):
        if node.data == "node":
            title = ast.literal_eval(f"{node.children[0]}")
            number = int(node.children[1][2:-1]) - 1
            par = writer.add_outline_item(title, number, parent=parent)
            children = node.children[2:]
            if children:
                for child in children:
                    reduce_node(child, par)

    if tree.data == "start":
        for child in tree.children:
            reduce_node(child, None)


def main():
    parser = Lark(grammar)
    with open(sys.argv[2]) as lisp_input:
        tree = parser.parse(lisp_input.read())
    writer = PdfWriter()
    with PdfReader(sys.argv[3]) as reader:
        # clone pdf without outlines
        if reader.metadata is not None:
            writer.add_metadata(reader.metadata)
            writer.append(reader, import_outline=False)

    add_outline(writer, tree)
    #print(writer.outline)
    with open(sys.argv[1], "wb") as output:
        writer.write(output)


if __name__ == "__main__":
    main()
