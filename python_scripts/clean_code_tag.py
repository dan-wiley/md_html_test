#!/usr/bin/env python
import panflute as pf

def remove_code_attributes(elem, doc):
    if isinstance(elem, pf.Code):
        elem.classes = []
    return elem

def main(doc=None):
    return pf.run_filter(remove_code_attributes, doc=doc)

if __name__ == "__main__":
    main()
