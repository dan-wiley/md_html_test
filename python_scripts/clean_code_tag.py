from panflute import run_filter, Code, CodeBlock
from bs4 import BeautifulSoup


def strip_code_tags(elem, doc):
    if isinstance(elem, (Code, CodeBlock)):
        # Parse the code text with BeautifulSoup
        soup = BeautifulSoup(elem.text, 'html.parser')
        # Remove all child elements within the <code> tag
        if (code_tags:= soup.find('code')):
            for child in code_tags.find_all():
                child.extract()
            # Update the code text with the modified content
            elem.replace_text(str(soup))
        return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
