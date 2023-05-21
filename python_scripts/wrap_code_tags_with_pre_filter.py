import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.CodeBlock) and not isinstance(elem.parent, pf.RawBlock):
        pre_tag = pf.RawBlock("<pre>", format="html")
        pre_tag.content = [pf.RawInline("<code>", format="html"), elem, pf.RawInline("</code>", format="html")]
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
