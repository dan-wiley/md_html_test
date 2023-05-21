import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.Code) and (not isinstance(elem.parent, pf.RawBlock) or elem.parent.format != "html" or elem.parent.text.strip().lower() != "<pre>"):
        pre_tag = pf.RawBlock("<pre>")
        pre_tag.content.append(pf.Plain(elem))
        pre_tag.content.append(pf.RawBlock("</pre>"))
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
