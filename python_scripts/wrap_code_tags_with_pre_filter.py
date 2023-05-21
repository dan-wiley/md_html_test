import panflute as pf

def wrap_code_blocks(elem, doc):
    if isinstance(elem, pf.Code) and not any(isinstance(parent, pf.CodeBlock) for parent in elem.walk()):
        pre_tag = pf.RawBlock("<pre>", format="html")
        pre_tag.content.append(elem)
        pre_tag.content.append(pf.RawBlock("</pre>", format="html"))
        return pre_tag

if __name__ == "__main__":
    pf.run_filter(wrap_code_blocks)
