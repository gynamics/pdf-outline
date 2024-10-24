#!/usr/bin/env python

import sys
from pypdf import PdfReader


class MyPdfReader(PdfReader):
    def outline_to_lisp(self):
        def format_one_node(node, children, indent):
            lisp = ""
            if node is not None:
                title = repr(node.title).replace('"', '\\"')[1:-1]
                number = self.get_destination_page_number(node) + 1
                lisp += "    " * indent
                lisp += f'("{title}" "#{str(number)}"'
                if children is not None:
                    lisp += "\n"
                    lisp += outline_to_lisp_r(children, indent + 1)
                    lisp += "    " * indent
                lisp += ")\n"
            return lisp

        def outline_to_lisp_r(nodes, indent):
            lisp = ""
            last_node = None
            for node in nodes:
                if type(node) is list:
                    lisp += format_one_node(last_node, node, indent)
                    last_node = None
                else:
                    lisp += format_one_node(last_node, None, indent)
                    last_node = node
            if last_node is not None:
                lisp += format_one_node(last_node, None, indent)
            return lisp

        return "(bookmarks\n" + outline_to_lisp_r(self.outline, 1) + ")"


def main():
    with MyPdfReader(sys.argv[1]) as reader:
        print(reader.outline_to_lisp())


if __name__ == "__main__":
    main()
