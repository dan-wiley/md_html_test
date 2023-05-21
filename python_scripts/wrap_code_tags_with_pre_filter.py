import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.Code) and isinstance(elem.parent, pf.RawBlock) and elem.parent.format == "html" and elem.parent.text.strip().lower() == "<pre>":
        return None

    if isinstance(elem, pf.Code):
        pre_tag = pf.Plain(pf.RawInline("<pre>"))
        pre_tag.content.append(elem)
        pre_tag.content.append(pf.RawInline("</pre>"))
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
