#!/usr/bin/env python3
import re
from panflute import run_filter, RawInline


def strip_code_tags(elem, doc):
    if elem.tag == 'code':
        # Remove all child elements
        elem.content = []
    return None


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
