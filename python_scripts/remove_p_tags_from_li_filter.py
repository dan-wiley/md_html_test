import panflute as pf

def remove_p_tags_within_li(elem):
    if isinstance(elem, (pf.OrderedList, pf.BulletList)):
        elem.content = [remove_p_tags_within_li(item) if isinstance(item, pf.ListItem) else item for item in elem.content]
    elif isinstance(elem, pf.ListItem):
        elem.content = [remove_p_tags_within_li(subelem) if isinstance(subelem, pf.Para) else subelem for subelem in elem.content]
        elem.content = [subelem for subelem in elem.content if not (isinstance(subelem, pf.Para) and has_nested_p_tags(subelem))]
    return elem

def has_nested_p_tags(elem):
    if isinstance(elem, pf.Para):
        return True
    elif isinstance(elem, (pf.Div, pf.Span, pf.Quoted, pf.Math)):
        return any(has_nested_p_tags(subelem) for subelem in elem.content)
    elif isinstance(elem, pf.Code):
        return has_nested_p_tags(elem.text)
    elif isinstance(elem, (list, tuple)):
        return any(has_nested_p_tags(sublist) for sublist in elem)
    return False

def main(doc, *args):
    return remove_p_tags_within_li(doc)

if __name__ == "__main__":
    pf.run_filter(main)
