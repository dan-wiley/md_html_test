#!/usr/bin/env python3
import re
from panflute import run_filter


def strip_code_tags(elem, doc):
    if elem.tag == 'code':
        # Remove all child elements within the <code> tag
        elem.text = re.sub(r'<.*?>', '', elem.text)
        # Remove leading and trailing whitespaces
        elem.text = elem.text.strip()
        return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
