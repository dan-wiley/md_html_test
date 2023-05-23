#!/usr/bin/env python3
from panflute import Code, RawInline, run_filter


def strip_code_tags(elem):
    if isinstance(elem, Code):
        # Remove all child elements within <code>
        elem.content = [RawInline(elem.text)]
    return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
