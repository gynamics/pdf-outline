#!/usr/bin/env python

import sys
import ast
import pymupdf
from lark import Lark, Transformer


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
    %ignore /;[^\\n]*/
"""


def lisp_to_toc(tree):

    def down_layer(node, level):
        if node.data == "node":
            title = ast.literal_eval(f"{node.children[0]}")
            number = int(node.children[1][2:-1])
            layer = [[level, title, number]]
            children = node.children[2:]
            if children:
                layer.extend([
                    item for child in children
                    for item in down_layer(child, level + 1)
                ])
            return layer

    if tree.data == "start":
        return [
            item for child in tree.children for item in down_layer(child, 1)
        ]


def main():
    if len(sys.argv) < 3:
        print("Usage: mupdf-set-outline.py [OUTPUT] [OUTLINE] [INPUT]")
        sys.exit(1)
    parser = Lark(grammar)
    with open(sys.argv[2]) as lisp_input:
        tree = parser.parse(lisp_input.read())
    toc = lisp_to_toc(tree)
    #print(toc)
    with pymupdf.open(sys.argv[3]) as doc:
        doc.set_toc(toc)
        doc.save(sys.argv[1])


if __name__ == "__main__":
    main()
