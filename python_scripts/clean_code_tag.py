#!/usr/bin/env python3
from bs4 import BeautifulSoup
from panflute import run_filter, RawInline


def strip_code_tags(elem, doc):
    if elem.tag == 'code':
        soup = BeautifulSoup(str(elem), 'html.parser')
        text = soup.get_text()
        return RawInline(text)
    return None


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
