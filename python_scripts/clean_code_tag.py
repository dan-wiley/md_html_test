#!/usr/bin/env python3
from bs4 import BeautifulSoup
from panflute import Code, RawInline, run_filter


def strip_code_tags(elem, doc):
    if isinstance(elem, Code):
        soup = BeautifulSoup(elem.text, 'html.parser')
        # Remove all child tags within <code>
        for tag in soup.find_all():
            tag.unwrap()
        elem.text = str(soup)
        elem.content = [RawInline(elem.text)]
    return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
