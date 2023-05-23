from bs4 import BeautifulSoup
import panflute as pf

def strip_html_tags(elem, doc):
    if isinstance(elem, pf.RawInline) and elem.format == 'html':
        print("Processing RawInline element:", elem)
        soup = BeautifulSoup(elem.text, 'html.parser')
        code_tags = soup.find_all('code')
        print("Number of code tags found:", len(code_tags))
        for tag in code_tags:
            # Replace <code> tag with its plain text content
            tag.string.replace_with(tag.text)
        elem.text = str(soup)
        print("Modified element:", elem)
    return elem


def main(doc=None):
    return pf.run_filter(strip_html_tags, doc=doc)

if __name__ == "__main__":
    main()
