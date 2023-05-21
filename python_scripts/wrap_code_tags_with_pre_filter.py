import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.Code) and (not isinstance(elem.parent, pf.RawInline) or elem.parent.text.strip().lower() != "<pre>"):
        pre_tag = pf.RawInline("<pre>")
        pre_tag.content = [elem]
        pre_tag.content.append(pf.RawInline("</pre>"))
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
