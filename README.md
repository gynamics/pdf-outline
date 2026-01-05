# pdf-outline (mupdf branch)

I use `djvused` for editing outlines of djvu documents. It is very convenient with a lisp-style outline format, especially if you use Emacs for editing.

The outline/bookmark syntax for djvused is extremely simple, you can check it in the manual of `djvused`.

> Outline/Bookmark syntax
>
> The outline syntax is a single list of the form (bookmarks ...)
>
> The first element of the list is symbol bookmarks. The subsequent elements are lists representing the toplevel outline entries. Each outline entry is represented by a list with the following form:
>
> (title url ... )
>
> The string title is the title of the outline entry. The destination string url can be either an arbitrary percent encoded URL, or composed of the hash character ("#") followed by a page name or number, or composed of the question mark character ("?") followed by cgi-style arguments interpreted by the djvu viewer. The remaining expressions in the list describe subentries of this outline entry.

You can see corresponding BNF grammar definition in [mupdf-set-outline.py](mupdf-set-outline.py).

However, I found that surprisingly there is no corresponding tool for pdf documents! Luckily, there has already been a lot of tools that can be used for manipulating pdf documents, all I need to do is to create a parser for lisp-style outline list, and reduce it to pdf outlines.

This branch uses `mupdf` backend, which is much more efficient than original `pypdf` backend. (See [benchmark of python pdf libraries](https://github.com/py-pdf/benchmarks), the text extraction speed of `mupdf` is about 30x faster than `pypdf`)

Here are two python scripts `mupdf-get-outline.py` and `mupdf-set-outline.py`, which reads outline from a pdf document, or creates a new pdf document with given outline and pdf document. The outline format is exactly the same as which is accepted by `djvused`, so you can simply attach one djvu outline to your pdf file if they have the same page numbering!

```sh
./mupdf-get-outline.py [PDF-INPUT]

./mupdf-set-outline.py [PDF-IN-OUT] [OUTLINE]
./mupdf-set-outline.py [PDF-OUTPUT] [OUTLINE] [PDF-INPUT]
```

Python requirements are specified in `requirements.txt`, installed them all with `pip install -r requirements.txt`.
