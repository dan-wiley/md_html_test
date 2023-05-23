from pandocfilters import Code, toJSONFilter


def remove_code_attributes(key, value, format_, meta):
    if key == 'Code':
        [attrs, contents] = value
        # Remove class and other attributes
        attrs = []
        return Code(attrs, contents)
    return None


if __name__ == "__main__":
    toJSONFilter(remove_code_attributes)
