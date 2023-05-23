from panflute import run_filter, Code, CodeBlock
from bs4 import BeautifulSoup
import os


def strip_code_tags(elem, doc):
    if isinstance(elem, (Code, CodeBlock)):
        # Check if elem.text is a valid file
        if os.path.isfile(elem.text):
            # Read the file contents
            with open(elem.text, 'r') as file:
                file_contents = file.read()
            # Parse the file contents with BeautifulSoup
            soup = BeautifulSoup(file_contents, 'html.parser')
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
