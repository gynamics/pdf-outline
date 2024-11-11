#!/usr/bin/env python

import sys
import pymupdf


def toc_to_lisp(toc):
    lisp = ["(bookmarks"]
    last_levels = [0]
    for item in toc:
        if item is None:
            break
        level = item[0]
        title = repr(item[1])[1:-1]
        number = item[2]
        if item[0] <= last_levels[-1]:
            lisp.append(")" * (1 + last_levels.pop() - level))
        lisp.append("\n")
        lisp.append(" " * level)
        lisp.append(f'("{title}" "#{number}"')
        last_levels.append(item[0])
    lisp.append(")" * (1 + last_levels.pop()))
    return ''.join(lisp)


def main():
    with pymupdf.open(sys.argv[1]) as doc:
        print(toc_to_lisp(doc.get_toc()))

if __name__ == "__main__":
    main()
