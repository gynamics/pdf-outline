#!/usr/bin/env python

import sys
from pypdf import PdfReader


class MyPdfReader(PdfReader):
    def outline_to_lisp(self):
        def format_one_node(node, children, indent):
            parts = []
            if node is not None:
                title = repr(node.title)[1:-1]
                number = self.get_destination_page_number(node) + 1
                parts.append("    " * indent)
                parts.append(f'("{title}" "#{str(number)}"')
                if children is not None:
                    parts.append(f'\n{outline_to_lisp_r(children, indent + 1)}')
                    parts.append("    " * indent)
                parts.append(")\n")
            return ''.join(parts)

        def outline_to_lisp_r(nodes, indent):
            parts = []
            last_node = None
            for node in nodes:
                if type(node) is list:
                    parts.append(format_one_node(last_node, node, indent))
                    last_node = None
                else:
                    parts.append(format_one_node(last_node, None, indent))
                    last_node = node
            if last_node is not None:
                parts.append(format_one_node(last_node, None, indent))
            return ''.join(parts)

        return f'(bookmarks\n{outline_to_lisp_r(self.outline, 1)})'


def main():
    with MyPdfReader(sys.argv[1]) as reader:
        print(reader.outline_to_lisp())


if __name__ == "__main__":
    main()
