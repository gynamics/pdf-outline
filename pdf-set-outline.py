#!/usr/bin/python

import sys
import ast
from lark import Lark, Transformer
from pypdf import PdfWriter

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
    with open(sys.argv[3], "rb") as input:
        writer = PdfWriter(clone_from=input)
    add_outline(writer, tree)
    #print(writer.outline)
    with open(sys.argv[1], "wb") as output:
        writer.write(output)


if __name__ == "__main__":
    main()
