#!/usr/bin/env python3
from bs4 import BeautifulSoup
from panflute import run_filter


def strip_code_tags(elem, doc):
    if elem.tag == 'code':
        # Remove all child elements within the <code> tag
        elem.content = []
        # Get the text content within the <code> tag
        text = elem.text
        # Replace the <code> tag with the extracted text
        new_elem = doc.new_inline(text)
        return new_elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
