import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.Code) and not any(isinstance(parent, pf.CodeBlock) for parent in elem.ancestors()):
        pre_tag = pf.RawBlock("<pre>", format="html")
        pre_tag.text = elem.text
        pre_tag.text += "</pre>"
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
