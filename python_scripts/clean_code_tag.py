from panflute import run_filter, Code, CodeBlock
from bs4 import BeautifulSoup


def strip_code_tags(elem, doc):
    if isinstance(elem, (Code, CodeBlock)):
        # Parse the code text with BeautifulSoup
        soup = BeautifulSoup(elem.text, 'html.parser')
        code_tags = soup.find_all()
        for code_tag in code_tags:
            # Remove all child elements within each code tag
            code_tag.unwrap()
        # Update the code text with the modified content
        elem.text = str(soup)
        return elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
