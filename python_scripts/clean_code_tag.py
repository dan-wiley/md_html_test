from panflute import run_filter, Code


def strip_code_tags(elem, doc):
    if isinstance(elem, Code):
        elem.text = ''
        return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
