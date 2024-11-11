# pdf-outline (mupdf branch)

I use `djvused` for editing outlines of djvu documents. It is very convenient with a lisp-style outline list, especially if you use Emacs for editing.

However, I found that surprisingly there is no corresponding tool for pdf documents! Luckily, there has already been a lot of tools that can be used for manipulating pdf documents, all I need to do is to create a parser for lisp-style outline list, and reduce it to pdf outlines.

This branch uses `mupdf` backend, which is much more efficient than original `pypdf` backend.

Here are two python scripts `mupdf-get-outline.py` and `mupdf-set-outline.py`, which reads outline from a pdf document, or creates a new pdf document with given outline and pdf document. The outline format is exactly the same as which is accepted by `djvused`, so you can simply attach one djvu outline to your pdf file if they have the same page numbering!

```sh
./mupdf-get-outline.py [PDF-INPUT]

./mupdf-set-outline.py [PDF-OUTPUT] [OUTLINE] [PDF-INPUT]

```

Requirements are specified in `requirements.txt`, installed them all with `pip install -r requirements.txt`.
