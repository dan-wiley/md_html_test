from panflute import run_filter, Code, RawInline


def strip_code_tags(elem, doc):
    if isinstance(elem, Code):
        # Remove all child elements within the <code> tag
        elem.content = [RawInline(text=elem.text)]
        return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
