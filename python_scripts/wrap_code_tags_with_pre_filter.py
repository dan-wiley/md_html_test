import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.CodeBlock):
        elem.content.insert(0, pf.RawInline("<pre>"))
        elem.content.append(pf.RawInline("</pre>"))
    return elem

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
