from bs4 import BeautifulSoup
from panflute import run_filter, RawInline


def strip_code_tags(elem, doc):
    if isinstance(elem, RawInline) and elem.format == 'html' and elem.text.startswith('<code>'):
        # Parse the HTML content within the RawInline element
        soup = BeautifulSoup(elem.text, 'html.parser')
        # Get the text content within the <code> tag
        text_content = soup.code.get_text()
        # Create a new RawInline element with the extracted text content
        new_elem = RawInline(text_content)
        return new_elem


def main(doc=None):
    return run_filter(strip_code_tags, doc=doc)


if __name__ == "__main__":
    main()
